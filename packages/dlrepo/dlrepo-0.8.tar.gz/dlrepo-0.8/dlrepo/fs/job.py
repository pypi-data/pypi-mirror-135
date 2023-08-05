# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

import errno
import json
import logging
import os
from typing import Dict, Iterator

from .fmt import ArtifactFormat
from .product import Version
from .util import SubDir


LOG = logging.getLogger(__name__)


# --------------------------------------------------------------------------------------
class Job(SubDir):
    """
    TODO
    """

    def get_formats(self) -> Iterator[ArtifactFormat]:
        yield from ArtifactFormat.all(self)

    def get_format(self, name: str) -> ArtifactFormat:
        return ArtifactFormat(self, name)

    def archive_name(self) -> str:
        data = self.get_metadata()
        if {"product", "product_variant", "version"} <= set(data):
            return f"{data['product']}-{data['product_variant']}-v{data['version']}"
        return f"{self.name}-{self.parent.name}"

    def _metadata_path(self):
        return self._path / ".metadata"

    def _product_link_path(self):
        return self._path / ".product"

    @staticmethod
    def update_symlink(dst, link):
        if link.exists():
            if link.is_symlink():
                link.unlink()
            else:
                raise OSError(errno.ENOTEMPTY, f"{link} exists and is not a symlink")
        link.symlink_to(os.path.relpath(dst, link.parent))

    def _link_to_product(self, version: Version):
        """
        Link the job to its product, according to the job metadata.
        Create the product fs if needed.
        The links are created in both ways:

        - From the job to its product version:
            $ROOT/branches/<branch>/<tag>/<job>/.product ->
                $ROOT/products/<product>/<variant>/<branch>/<version>

        - From the product version to the job(s), for each format:
            $ROOT/products/<product>/<variant>/<branch>/<version>/<format> ->
                $ROOT/branches/<branch>/<tag>/<job>/<format>

        The formats in a product version are not necessarily linked to the same job.
        """
        version.create()
        self.update_symlink(version.path(), self._product_link_path())
        for fmt in self.get_formats():
            self.update_symlink(fmt.path(), version.path() / fmt.name)
        container = self.path() / "container"
        if container.is_dir():
            self.update_symlink(container, version.path() / "container")

    def _cleanup_product_tree(self):
        link = self._product_link_path()
        if not link.is_symlink():
            return
        if not link.is_dir():
            link.unlink()
            return
        product = link.resolve()
        for d in product.iterdir():
            if not d.is_symlink():
                continue
            if not d.is_dir():
                continue
            try:
                if d.resolve().samefile(self.path() / d.name):
                    d.unlink()
            except FileNotFoundError:
                # same product, different jobs (e.g. doc + binaries)
                pass
        try:
            if os.listdir(product) == [".stamp"]:
                (product / ".stamp").unlink()
            # cleanup empty dirs
            os.removedirs(product)
        except OSError:
            # directory not empty, abort
            pass
        link.unlink()

    def get_metadata(self) -> Dict:
        try:
            data = json.loads(self._metadata_path().read_text())
        except (OSError, ValueError):
            data = {}
        data["locked"] = self.is_locked()
        data["name"] = self.name
        return data

    def _lock_path(self):
        return self.path() / ".locked"

    def is_locked(self) -> bool:
        return self._lock_path().is_file()

    def set_locked(self, locked: bool):
        if not self.exists():
            raise FileNotFoundError()
        path = self._lock_path()
        if locked:
            path.touch()
        elif path.is_file():
            path.unlink()

    def add_metadata(self, new_data: Dict):
        if self.is_locked():
            raise FileExistsError("Job is locked")
        self._cleanup_product_tree()
        metadata_path = self._metadata_path()
        try:
            data = json.loads(metadata_path.read_text())
        except (OSError, ValueError):
            data = {}
        for k, v in new_data.items():
            if isinstance(v, str):
                v = v.lower()
            if v == "":
                data.pop(k, None)
            else:
                data[k] = v
        self.create()
        metadata_path.write_text(json.dumps(data))
        if {"product", "version", "product_branch", "product_variant"} <= set(data):
            self._link_to_product(
                self.root()
                .get_product(str(data["product"]))
                .get_variant(str(data["product_variant"]))
                .get_branch(str(data["product_branch"]))
                .get_version(str(data["version"]))
            )

    def delete(self, *, cleanup_orphans: bool = True):
        if not self.exists():
            raise FileNotFoundError()
        self._cleanup_product_tree()
        self.root().rmtree(self._path)
        if cleanup_orphans:
            self.root().cleanup_orphan_blobs()
