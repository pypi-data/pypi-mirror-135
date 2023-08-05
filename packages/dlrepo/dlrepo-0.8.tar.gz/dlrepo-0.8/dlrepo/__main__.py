# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

import logging.config
import os
import socket
import sys

from aiohttp import web

from . import views
from .fs import ArtifactRepository
from .views import auth


# --------------------------------------------------------------------------------------
class AccessLogger(web.AbstractAccessLogger):
    def log(self, request: web.BaseRequest, response: web.Response, time: float):
        self.logger.info(
            "%s@%s - %s %s %s %r",
            request.get("dlrepo_user"),
            request.headers.get("X-Forwarded-For", request.remote),
            response.status,
            request.method,
            request.path_qs,
            request.headers.get("User-Agent"),
        )


# --------------------------------------------------------------------------------------
def main():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "format": "%(levelname)s: %(message)s",
                },
                "syslog": {
                    "format": "dlrepo: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "console",
                },
                "syslog": {
                    "class": "logging.handlers.SysLogHandler",
                    "address": "/dev/log",
                    "formatter": "syslog",
                },
            },
            "root": {
                "level": os.getenv("DLREPO_LOG_LEVEL", "WARNING"),
                "handlers": [
                    os.getenv(
                        "DLREPO_LOG_OUTPUT",
                        "console" if sys.stdin.isatty() else "syslog",
                    ),
                ],
            },
        }
    )
    app = web.Application(middlewares=[auth.middleware])
    app[auth.AuthBackend.KEY] = auth.AuthBackend()
    app.on_startup.append(app[auth.AuthBackend.KEY].init)

    repo = ArtifactRepository(os.getenv("DLREPO_ROOT_DIR", "/var/lib/dlrepo"))
    app["dlrepo_artifact_repository"] = repo

    views.add_routes(app)

    kwargs = {"access_log_class": AccessLogger}

    # try inherit from systemd socket
    listen_fds = int(os.getenv("LISTEN_FDS", "0"))
    listen_pid = int(os.environ.get("LISTEN_PID", "0"))
    if listen_fds == 1 and listen_pid == os.getpid():
        kwargs["sock"] = socket.fromfd(3, socket.AF_UNIX, socket.SOCK_STREAM)
        kwargs["sock"].setblocking(False)
    else:
        # no systemd provided socket, listen on localhost by default
        kwargs["host"] = os.getenv("DLREPO_LISTEN_ADDRESS", "127.0.0.1")
        kwargs["port"] = int(os.getenv("DLREPO_LISTEN_PORT", "1337"))

    web.run_app(app, **kwargs)


if __name__ == "__main__":
    sys.exit(main())
