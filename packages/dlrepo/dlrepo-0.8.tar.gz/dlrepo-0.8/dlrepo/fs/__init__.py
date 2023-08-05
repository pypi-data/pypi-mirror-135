# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

import asyncio
import logging
import os
from pathlib import Path
import shutil
import time
from typing import Awaitable, Callable, Iterator, Optional

from cachetools import LFUCache

from .branch import Branch
from .container import ContainerRegistry
from .product import Product
from .util import CHUNK_SIZE, file_digest, human_readable, parse_digest


LOG = logging.getLogger(__name__)


# --------------------------------------------------------------------------------------
class AbstractRepository:
    def __init__(self, path: str):
        self._path = Path(path)
        self.parent = None
        self.container_registry = ContainerRegistry(self)

    def get_branches(self) -> Iterator[Branch]:
        yield from Branch.all(self)

    def get_branch(self, name: str) -> Branch:
        return Branch(self, name)

    def get_products(self) -> Iterator[Product]:
        yield from Product.all(self)

    def get_product(self, name: str) -> Product:
        return Product(self, name)

    def path(self) -> Path:
        return self._path

    def create(self):
        self._path.mkdir(mode=0o755, parents=True, exist_ok=True)

    def url_bit(self) -> Optional[str]:
        raise NotImplementedError()

    def cleanup_orphan_blobs(self):
        raise NotImplementedError()

    def next_upload(self) -> str:
        raise NotImplementedError()

    def blob_path(self, digest: str, parent: Optional[Path] = None) -> Path:
        raise NotImplementedError()

    def rmtree(self, path: Path):
        raise NotImplementedError()

    async def update_upload(
        self, uuid: str, stream: Callable[[int], Awaitable[bytes]]
    ) -> int:
        raise NotImplementedError()

    def cancel_upload(self, uuid: str):
        raise NotImplementedError()

    async def finalize_upload(self, uuid: str, digest: str) -> Path:
        raise NotImplementedError()

    def link_blob(self, digest: str, target: Path):
        raise NotImplementedError()

    def link_blob_ignore_quota(self, digest: str, target: Path):
        raise NotImplementedError()


# --------------------------------------------------------------------------------------
class ArtifactRepository(AbstractRepository):
    def __init__(self, path: str):
        super().__init__(path)
        self.blobs = self._path / ".blobs"
        self.uploads = self._path / ".uploads"
        self.user_repos = LFUCache(maxsize=512)

    def get_user_repo(self, user: str) -> "UserRepository":
        user = user.lower()
        repo = self.user_repos.get(user)
        if repo is None:
            repo = self.user_repos[user] = UserRepository(self, user)
        return repo

    def get_user_repos(self) -> Iterator["UserRepository"]:
        yield from UserRepository.all(self)

    def url_bit(self) -> Optional[str]:
        return None

    def url(self) -> str:
        return "/"

    def cleanup_orphan_blobs(self):
        # TODO: call blocking stuff (open, stat, unlink) in a thread?
        for folder in (self.blobs, self.uploads):
            _cleanup_orphans(folder)

    def next_upload(self) -> str:
        self.uploads.mkdir(mode=0o755, parents=True, exist_ok=True)
        while True:
            try:
                path = self.uploads / os.urandom(16).hex()
                path.touch(mode=0o600, exist_ok=False)
                return path.name
            except FileExistsError:
                continue

    def upload_path(self, uuid: str):
        if "/" in uuid or ".." in uuid:
            raise FileNotFoundError(uuid)
        path = self.uploads / uuid
        if not path.is_file():
            raise FileNotFoundError(uuid)
        return path

    def blob_path(self, digest: str, parent: Optional[Path] = None) -> Path:
        if not digest:
            raise ValueError(f"invalid digest: {digest}")
        if parent is None:
            parent = self.blobs
        algo, digest = parse_digest(digest.lower())
        path = parent / f"{algo}/{digest[:2]}/{digest}"
        if path.is_file():
            path.touch()
        return path

    def rmtree(self, path: Path):
        shutil.rmtree(path, onerror=_rmtree_error_cb)

    async def update_upload(
        self, uuid: str, stream: Callable[[int], Awaitable[bytes]]
    ) -> int:
        return await _stream_to_file(stream, self.upload_path(uuid))

    def cancel_upload(self, uuid: str):
        self.upload_path(uuid).unlink()

    async def finalize_upload(self, uuid: str, digest: str) -> Path:
        return await _check_and_move(
            self.upload_path(uuid), self.blob_path(digest), digest
        )

    def link_blob(self, digest: str, target: Path):
        _hardlink(self.blob_path(digest), target)

    def link_blob_ignore_quota(self, digest: str, target: Path):
        _hardlink(self.blob_path(digest), target)


# --------------------------------------------------------------------------------------
class UserRepository(AbstractRepository):
    def __init__(self, base: ArtifactRepository, user: str):
        self.base = base
        self.user = user
        super().__init__(base.path() / "users" / user)
        self.disk_usage = self._parse_disk_usage_file()
        self.disk_usage_dirty = False

    @classmethod
    def all(cls, base: ArtifactRepository) -> Iterator["UserRepository"]:
        path = base.path() / "users"
        if not path.is_dir():
            return
        for d in path.iterdir():
            if not d.is_dir():
                continue
            yield cls(base, d.name)

    def _parse_disk_usage_file(self) -> int:
        du_path = self.path() / ".disk_usage"
        if du_path.is_file():
            try:
                return int(du_path.read_text(encoding="utf-8"))
            except ValueError:
                pass
        return 0

    def disk_usage_refresh(self):
        self.disk_usage = 0
        for root, _, files in os.walk(self.path()):
            for f in files:
                self.disk_usage += Path(root, f).stat().st_size
        self.disk_usage_dirty = True

    def disk_usage_save(self):
        if not self.disk_usage_dirty:
            return
        self.create()
        du_path = self.path() / ".disk_usage"
        du_path.write_text(str(self.disk_usage), encoding="utf-8")
        self.disk_usage_dirty = False

    # 10G max usage per user
    QUOTA = int(os.getenv("DLREPO_USER_QUOTA", str(10 * (1024 ** 3))))

    def disk_usage_add(self, usage: int):
        new_usage = self.disk_usage + usage
        if new_usage > self.QUOTA:
            usage = f"{human_readable(self.disk_usage)}/{human_readable(self.QUOTA)}"
            raise PermissionError(
                f"User {self.user} quota exceeded ({usage}). Please make some ménage."
            )
        self.disk_usage = new_usage
        self.disk_usage_dirty = True

    def disk_usage_rm(self, usage: int):
        self.disk_usage = max(0, self.disk_usage - usage)
        self.disk_usage_dirty = True

    def url_bit(self) -> Optional[str]:
        return f"~{self.user}"

    def url(self) -> str:
        return f"/~{self.user}/"

    def cleanup_orphan_blobs(self):
        self.base.cleanup_orphan_blobs()

    def next_upload(self) -> str:
        return self.base.next_upload()

    def cancel_upload(self, uuid: str):
        self.disk_usage_rm(self.base.upload_path(uuid).stat().st_size)
        try:
            self.base.cancel_upload(uuid)
        finally:
            self.disk_usage_save()

    def rmtree(self, path: Path):
        removed = 0
        for root, _, files in os.walk(path):
            for f in files:
                removed += Path(root, f).stat().st_size
        self.disk_usage_rm(removed)
        try:
            self.base.rmtree(path)
        finally:
            self.disk_usage_save()

    async def update_upload(
        self, uuid: str, stream: Callable[[int], Awaitable[bytes]]
    ) -> int:
        try:
            return await _stream_to_file(stream, self.base.upload_path(uuid), self)
        finally:
            self.disk_usage_save()

    async def finalize_upload(self, uuid: str, digest: str) -> Path:
        try:
            return await _check_and_move(
                self.base.upload_path(uuid), self.base.blob_path(digest), digest, self
            )
        finally:
            self.disk_usage_save()

    def blob_path(self, digest: str, parent: Optional[Path] = None) -> Path:
        return self.base.blob_path(digest, parent=parent)

    def link_blob(self, digest: str, target: Path):
        try:
            _hardlink(self.base.blob_path(digest), target, self)
        finally:
            self.disk_usage_save()

    def link_blob_ignore_quota(self, digest: str, target: Path):
        _hardlink(self.base.blob_path(digest), target)


# --------------------------------------------------------------------------------------
def _rmtree_error_cb(func, path, exc_info):
    # nothing much we can do here, simply log a message
    LOG.error("%s(%r) failed:", func, path, exc_info=exc_info)


async def _stream_to_file(
    stream: Callable[[int], Awaitable[bytes]],
    path: Path,
    user_repo: Optional[UserRepository] = None,
) -> int:
    # TODO: call blocking stuff (open, write, unlink) in a thread?
    try:
        with path.open("ab") as f:
            while True:
                chunk = await stream(CHUNK_SIZE)
                if not chunk:
                    break
                if user_repo is not None:
                    user_repo.disk_usage_add(len(chunk))
                f.write(chunk)
    except:
        if user_repo is not None:
            user_repo.disk_usage_rm(path.stat().st_size)
        path.unlink()
        raise
    return path.stat().st_size


# --------------------------------------------------------------------------------------
def _hardlink(src: Path, dst: Path, user_repo: Optional[UserRepository] = None):
    if not src.is_file():
        raise FileNotFoundError()
    dst.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
    if dst.is_file():
        if user_repo is not None:
            user_repo.disk_usage_rm(dst.stat().st_size)
        dst.unlink()
    if user_repo is not None:
        user_repo.disk_usage_add(src.stat().st_size)
    os.link(src, dst)


# --------------------------------------------------------------------------------------
async def _check_and_move(
    src: Path, dst: Path, digest: str, user_repo: Optional[UserRepository] = None
):
    algo, dig = parse_digest(digest.lower())
    loop = asyncio.get_running_loop()
    if await loop.run_in_executor(None, file_digest, algo, src) != dig:
        if user_repo is not None:
            user_repo.disk_usage_rm(src.stat().st_size)
        src.unlink()
        try:
            os.removedirs(src.parent)
        except OSError:
            pass
        raise ValueError(f"Received data does not match digest: {digest}")
    dst.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
    src.rename(dst)
    dst.chmod(0o644)
    return dst


# --------------------------------------------------------------------------------------
ORPHAN_BLOB_LIFETIME = int(os.getenv("DLREPO_ORPHAN_BLOB_LIFETIME", "600"))


def _cleanup_orphans(folder: Path):
    if not folder.is_dir():
        return
    now = time.time()
    for root, _, files in os.walk(folder):
        for f in files:
            f = Path(root, f)
            if not f.is_file():
                continue
            stat = f.stat()
            if stat.st_nlink > 1:
                continue
            if now - stat.st_mtime < ORPHAN_BLOB_LIFETIME:
                continue
            f.unlink()
