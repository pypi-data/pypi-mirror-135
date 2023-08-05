# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

import asyncio
import logging
import os
from pathlib import Path
import socket
from typing import Iterator, Optional

import aiohttp

from .fmt import ArtifactFormat
from .job import Job
from .util import SubDir


LOG = logging.getLogger(__name__)


# --------------------------------------------------------------------------------------
class Tag(SubDir):
    """
    TODO
    """

    def create(self):
        super().create()
        stamp = self._path / ".stamp"
        if not stamp.exists():
            stamp.touch()

    @classmethod
    def creation_date(cls, t):
        stamp = t.path() / ".stamp"
        if stamp.is_file():
            # prefer mtime over ctime
            # on UNIX, ctime is "the time of most recent metadata change" whereas
            # mtime is "most recent content modification"
            return stamp.stat().st_mtime
        return 0

    @property
    def timestamp(self) -> int:
        return Tag.creation_date(self)

    def get_jobs(self) -> Iterator[Job]:
        yield from Job.all(self)

    def get_job(self, name: str) -> Job:
        return Job(self, name)

    def _publish_status_path(self) -> Path:
        return self._path / ".publish-status"

    def publish_status(self) -> Optional[str]:
        try:
            return self._publish_status_path().read_text().strip()
        except FileNotFoundError:
            return None

    def _released_path(self) -> Path:
        return self._path / ".released"

    def is_released(self) -> bool:
        return self._released_path().is_file()

    def set_released(self, released: bool):
        if not self._path.is_dir():
            raise FileNotFoundError()
        loop = asyncio.get_running_loop()
        task = loop.create_task(self.do_release(released))
        task.add_done_callback(self.done_cb)

    def done_cb(self, task):
        if task.cancelled():
            return
        exc = task.exception()
        if exc:
            LOG.error("while changing released flag on tag %s", self.name, exc_info=exc)
            self._publish_status_path().write_text(f"error: {exc}\n")

    PUBLISH_URL = os.getenv("DLREPO_PUBLISH_URL")
    PUBLISH_AUTH = os.getenv("DLREPO_PUBLISH_AUTH")
    USER_AGENT = f"dlrepo-server/{socket.gethostname()}"

    def _publish_session(self) -> aiohttp.ClientSession:
        with open(self.PUBLISH_AUTH, "r", encoding="utf-8") as f:
            buf = f.read().strip()
        if ":" not in buf:
            raise ValueError("invalid DLREPO_PUBLISH_AUTH file")
        login, password = buf.split(":", 1)
        auth = aiohttp.BasicAuth(login, password, "utf-8")
        return aiohttp.ClientSession(
            self.PUBLISH_URL,
            auth=auth,
            raise_for_status=True,
            headers={"User-Agent": self.USER_AGENT},
        )

    async def do_release(self, released: bool):
        if self.PUBLISH_URL and self.PUBLISH_AUTH:
            self._publish_status_path().write_text("in progress\n")
            async with self._publish_session() as sess:
                if released:
                    LOG.info(
                        "publishing tag %s/%s to %s",
                        self.parent.name,
                        self.name,
                        self.PUBLISH_URL,
                    )
                    await self._publish(sess)
                else:
                    LOG.info(
                        "deleting tag %s/%s from %s",
                        self.parent.name,
                        self.name,
                        self.PUBLISH_URL,
                    )
                    await sess.delete(self.url(), params={"force": "true"})
        path = self._released_path()
        if released:
            path.touch()
        elif path.is_file():
            path.unlink()

    async def _publish(self, sess: aiohttp.ClientSession):
        for job in self.get_jobs():
            self._publish_status_path().write_text(f"uploading {job.name}\n")
            for fmt in job.get_formats():
                await self._publish_fmt(fmt, sess)
            metadata = job.get_metadata()
            del metadata["name"]
            del metadata["locked"]
            job_url = job.url()
            LOG.debug("publishing job metadata %s", job_url)
            await sess.patch(job_url, json={"job": metadata})
        self._publish_status_path().write_text(f"published to {self.PUBLISH_URL}\n")

    async def _publish_fmt(self, fmt: ArtifactFormat, sess: aiohttp.ClientSession):
        fmt_url = fmt.url()

        for file, digest in fmt.get_digests().items():
            file_url = fmt_url + file
            headers = {"Digest": digest}

            resp = await sess.head(file_url, headers=headers, raise_for_status=False)
            if resp.status == 200:
                LOG.debug("publishing file %s (deduplicated)", file_url)
                # file digest already present on the server, do not upload
                # the data again
                headers["X-Dlrepo-Link"] = digest
                await sess.put(file_url, data=None, headers=headers)

            else:
                LOG.debug("publishing file %s", file_url)
                # file digest not on server, proceed with upload
                with open(fmt.path() / file, "rb") as f:
                    await sess.put(file_url, data=f, headers=headers)

        if fmt.is_internal():
            LOG.debug("publishing internal format %s", fmt_url)
            await sess.put(fmt_url, json={"artifact_format": {"internal": True}})

        # clear the dirty flag
        await sess.patch(fmt_url)

    def _locked_path(self) -> Path:
        return self._path / ".locked"

    def is_locked(self) -> bool:
        return self._locked_path().is_file()

    def set_locked(self, locked: bool):
        path = self._locked_path()
        if locked:
            path.touch()
        elif path.is_file():
            path.unlink()

    def delete(self, *, force: bool = False, cleanup_orphans: bool = True):
        if not self.exists():
            raise FileNotFoundError()
        if self.is_locked():
            raise OSError(f"Tag {self.name} is locked")
        if not force and self.is_released():
            raise OSError(f"Tag {self.name} is released, use force")
        for j in self.get_jobs():
            j.delete(cleanup_orphans=False)
        self.root().rmtree(self._path)
        if cleanup_orphans:
            self.root().cleanup_orphan_blobs()
