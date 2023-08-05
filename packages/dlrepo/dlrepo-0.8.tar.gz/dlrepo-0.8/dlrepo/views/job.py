# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

from aiohttp import web
import aiohttp_jinja2

from .util import BaseView, TarResponse


# --------------------------------------------------------------------------------------
class JobArchiveView(BaseView):
    @classmethod
    def urls(cls):
        yield "/branches/{branch}/{tag}/{job}.tar"
        yield "/~{user}/branches/{branch}/{tag}/{job}.tar"

    def _get_job(self):
        match = self.request.match_info
        if match["tag"] in ("latest", "stable") and self.request.method != "GET":
            raise web.HTTPMethodNotAllowed(self.request.method, ["GET"])
        try:
            return (
                self.repo()
                .get_branch(match["branch"])
                .get_tag(match["tag"])
                .get_job(match["job"])
            )
        except FileNotFoundError as e:
            raise web.HTTPNotFound() from e

    def _digests(self, job):
        digests = {}
        for fmt in job.get_formats():
            if self.access_granted(fmt.url()):
                for f, digest in fmt.get_digests().items():
                    digests[f"{fmt.name}/{f}"] = digest
        return digests

    async def get(self):
        job = self._get_job()
        url = job.url().rstrip("/") + ".tar"
        if url != self.request.path:
            raise web.HTTPFound(url)
        return TarResponse(self._digests(job), job.path(), job.archive_name())


# --------------------------------------------------------------------------------------
class JobView(JobArchiveView):
    @classmethod
    def urls(cls):
        yield "/branches/{branch}/{tag}/{job}"
        yield "/branches/{branch}/{tag}/{job}/"
        yield "/~{user}/branches/{branch}/{tag}/{job}"
        yield "/~{user}/branches/{branch}/{tag}/{job}/"

    async def get(self):
        """
        Get info about a job including metadata and artifact formats.
        """
        job = self._get_job()
        if not job.exists():
            raise web.HTTPNotFound()
        if job.url() != self.request.path:
            raise web.HTTPFound(job.url())
        html = "html" in self.request.headers.get("Accept", "json")
        data = {"job": job.get_metadata()}
        formats = []
        for f in job.get_formats():
            if self.access_granted(f.url()):
                if html:
                    formats.append({"name": f.name, "internal": f.is_internal()})
                else:
                    formats.append(f.name)
        data["job"]["artifact_formats"] = formats
        if html:
            return aiohttp_jinja2.render_template("job.html", self.request, data)
        return web.json_response(data)

    async def put(self):
        try:
            locked = (await self.json_body())["job"]["locked"]
            if not isinstance(locked, bool):
                raise TypeError()
        except (TypeError, KeyError) as e:
            raise web.HTTPBadRequest(reason="Invalid parameters") from e
        try:
            self._get_job().set_locked(locked)
        except FileNotFoundError as e:
            raise web.HTTPNotFound() from e
        return web.Response()

    async def patch(self):
        """
        Update the metadata of a job.
        """
        try:
            data = (await self.json_body())["job"]
            if not isinstance(data, dict):
                raise TypeError()
        except (TypeError, KeyError) as e:
            raise web.HTTPBadRequest(reason="Invalid parameters") from e
        try:
            self._get_job().add_metadata(data)
        except FileExistsError as e:
            raise web.HTTPBadRequest(reason=str(e)) from e
        return web.Response()

    async def delete(self):
        """
        Delete a job and all its contents.
        """
        try:
            job = self._get_job()
            job.delete()
        except FileNotFoundError as e:
            raise web.HTTPNotFound() from e
        except OSError as e:
            raise web.HTTPBadRequest(reason=str(e)) from e
        return web.Response()
