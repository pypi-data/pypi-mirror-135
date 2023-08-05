# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

import asyncio
import hashlib
import logging
import os
import pathlib
import re
import shlex
import signal
from typing import Callable, Dict, FrozenSet, List, Optional, Tuple

from aiohttp import hdrs, web
from aiohttp.helpers import BasicAuth
import bonsai
import cachetools

from . import errors


LOG = logging.getLogger(__name__)


# --------------------------------------------------------------------------------------
@web.middleware
async def middleware(
    request: web.Request, handler: Callable[[web.Request], web.Response]
) -> web.Response:
    backend = request.app[AuthBackend.KEY]
    await backend.check(request)
    return await handler(request)


# --------------------------------------------------------------------------------------
class AuthBackend:

    KEY = "dlrepo_auth_backend"
    AUTH_DISABLED = os.getenv("DLREPO_AUTH_DISABLED", "0") == "1"
    IGNORE_PASSWORDS = os.getenv("DLREPO_IGNORE_PASSWORDS", "0") == "1"
    LDAP_URL = os.getenv("DLREPO_LDAP_URL", "")
    LDAP_USER_DN = os.getenv("DLREPO_LDAP_USER_DN", "")
    LDAP_BASE_DN = os.getenv("DLREPO_LDAP_BASE_DN", "")
    LDAP_GROUPS_FILTER = os.getenv("DLREPO_LDAP_GROUPS_FILTER", "")
    TIMEOUT = int(os.getenv("DLREPO_LDAP_TIMEOUT", "10"))
    MAX_CONNECTIONS = int(os.getenv("DLREPO_LDAP_MAX_CONNECTIONS", "4"))
    CACHE_SIZE = int(os.getenv("DLREPO_AUTH_CACHE_SIZE", "4096"))
    CACHE_TTL = int(os.getenv("DLREPO_AUTH_CACHE_TTL", "600"))

    def __init__(self):
        self.seed = os.urandom(32)
        self.semaphore = None  # created in init() to ensure it uses the running loop
        self.flush_caches()

    def flush_caches(self) -> None:
        self.group_acls = parse_group_acls()
        self.user_groups = parse_auth_file(self.seed)
        self.acls_cache = cachetools.TTLCache(self.CACHE_SIZE, self.CACHE_TTL)
        self.access_cache = cachetools.TTLCache(self.CACHE_SIZE, self.CACHE_TTL)

    async def init(self, app: web.Application) -> None:
        if self.AUTH_DISABLED:
            for line in BANNED_AUTH_DISABLED.strip().splitlines():
                LOG.critical("%s", line)
        elif self.IGNORE_PASSWORDS:
            for line in BANNED_IGNORED_PASSWORDS.strip().splitlines():
                LOG.critical("%s", line)
        asyncio.get_running_loop().add_signal_handler(signal.SIGHUP, self.flush_caches)
        self.semaphore = asyncio.Semaphore(self.MAX_CONNECTIONS)

    async def get_user_groups_from_ldap(self, login: str, password: str) -> List[str]:
        client = bonsai.LDAPClient(self.LDAP_URL, tls=True)

        if not self.IGNORE_PASSWORDS:
            if not login or not password:
                raise PermissionError()
            dn = self.LDAP_USER_DN % bonsai.escape_attribute_value(login)
            client.set_credentials("SIMPLE", user=dn, password=password)

        groups = []
        try:
            LOG.debug("checking credentials for %s on %s", login, self.LDAP_URL)
            filter_exp = self.LDAP_GROUPS_FILTER % bonsai.escape_attribute_value(login)
            async with client.connect(is_async=True, timeout=self.TIMEOUT) as conn:
                search_results = await conn.search(
                    base=self.LDAP_BASE_DN,
                    scope=bonsai.LDAPSearchScope.SUBTREE,
                    filter_exp=filter_exp,
                    attrlist=["cn"],
                    timeout=self.TIMEOUT,
                )
                for group in search_results:
                    groups.append(group["cn"][0])
        except bonsai.AuthenticationError as e:
            LOG.debug("authentication failed for %s: %s", login, e)
            raise PermissionError() from e

        return groups

    async def get_user_groups_from_file(self, login: str, password: str) -> List[str]:
        if self.user_groups:
            auth = login
            if not self.IGNORE_PASSWORDS:
                auth += f":{password}"
            auth_key = hashlib.sha256(self.seed + auth.encode("utf-8")).digest()
            groups = self.user_groups.get(auth_key, None)
            if groups is not None:
                return groups

        raise PermissionError()

    async def get_user_acls(self, login: str, password: str) -> FrozenSet["ACL"]:
        """
        Authenticate (or identify) the user against the LDAP server and fetch their
        groups. Return all ACLs associated with the user's groups.
        """
        groups = []

        if self.LDAP_URL:
            # use a semaphore to limit the number of concurrent ldap connections
            async with self.semaphore:
                groups = await self.get_user_groups_from_ldap(login, password)
        else:
            groups = await self.get_user_groups_from_file(login, password)

        if not groups:
            LOG.debug("user %s does not exist or is not in any group", login)
            raise PermissionError()

        LOG.debug("user %s authenticated", login)

        # determine authenticated user acls from their groups
        acls = []
        for g in groups:
            for acl in self.group_acls.get(g, []):
                acls.append(acl.expand_user(login))

        return frozenset(acls)

    def auth_error(self, request: web.Request) -> web.HTTPError:
        if request.path.startswith("/v2/"):
            # docker registry errors must be JSON and must have specific HTTP headers
            return errors.Unauthorized()
        return errors.AuthenticationRequired()

    async def check(self, request: web.Request) -> None:
        if self.AUTH_DISABLED:
            return
        is_write = request.method not in ("GET", "HEAD")
        if not is_write:
            if request.path.startswith("/static/") or request.path == "/favicon.ico":
                # no need for authentication for these
                return

        try:
            auth_header = request.headers.get(hdrs.AUTHORIZATION, "")
            auth = BasicAuth.decode(auth_header, encoding="utf-8")
            if not auth.login:
                auth = None
        except ValueError:
            auth = None

        # store the username for display in the access log
        request["dlrepo_user"] = auth.login if auth else "ANONYMOUS"

        if auth is None and (is_write or request.path == "/v2/"):
            # anonymous write access is always denied
            # the docker registry API states that anonymous GET requests to /v2/
            # must receive a 401 unauthorized error
            # https://docs.docker.com/registry/spec/api/#api-version-check
            raise self.auth_error(request)

        # prepend basic auth with random seed before hash to use as safe cache key
        auth_key = hashlib.sha256(self.seed + auth_header.encode("utf-8")).digest()
        if auth_key in self.acls_cache:
            acls = self.acls_cache[auth_key]
        elif auth is None:
            acls = self.group_acls.get("ANONYMOUS", frozenset())
            self.acls_cache[auth_key] = acls
        else:
            try:
                acls = await self.get_user_acls(auth.login, auth.password)
                self.acls_cache[auth_key] = acls
            except (PermissionError, FileNotFoundError) as e:
                raise self.auth_error(request) from e

        # store user acls for reuse in views to filter out non-accessible elements
        request["dlrepo_user_acls"] = acls

        if not self.access_granted(
            acls, is_write, request.path, request["dlrepo_user"]
        ):
            raise self.auth_error(request)

    def access_granted(
        self,
        acls: FrozenSet["ACL"],
        is_write: bool,
        url: str,
        username: Optional[str] = None,
    ) -> bool:
        """
        Check if the provided ACLs give write and/or read access to the specified URL.
        """
        access_key = (acls, is_write, url)
        granted = self.access_cache.get(access_key)
        if granted is not None:
            return granted
        granted = False
        for acl in acls:
            if acl.access_granted(is_write, url):
                if username is not None:
                    LOG.debug("access granted to %s by ACL %s", username, acl)
                granted = True
                break
        self.access_cache[access_key] = granted
        return granted


# --------------------------------------------------------------------------------------
BANNED_AUTH_DISABLED = r"""
########################################
#                /!\                   #
# NO AUTHENTICATION! ANYONE CAN WRITE! #
########################################
"""
BANNED_IGNORED_PASSWORDS = r"""
#####################################
#                /!\                #
# PASSWORD AUTHENTICATION BYPASSED! #
#####################################
"""
AUTH_FILE_RE = re.compile(
    r"""
    ^
    (?P<user>[^:]+):
    (?P<password>.+):
    (?P<groups>[\w\s-]+)
    $
    """,
    re.MULTILINE | re.VERBOSE,
)


# --------------------------------------------------------------------------------------
def parse_auth_file(seed: bytes) -> Dict[bytes, List[str]]:
    user_groups = {}

    try:
        auth_file = os.getenv("DLREPO_AUTH_FILE", "/etc/dlrepo/auth")
        buf = pathlib.Path(auth_file).read_text(encoding="utf-8")
        for match in AUTH_FILE_RE.finditer(buf):
            groups = match.group("groups").strip().split()
            if not groups:
                continue
            auth = match.group("user")
            if not AuthBackend.IGNORE_PASSWORDS:
                auth += ":" + match.group("password")
            auth_key = hashlib.sha256(seed + auth.encode("utf-8")).digest()
            user_groups[auth_key] = groups

    except FileNotFoundError as e:
        if not AuthBackend.LDAP_URL and not AuthBackend.AUTH_DISABLED:
            LOG.error("DLREPO_AUTH_FILE: %s", e)

    return user_groups


# --------------------------------------------------------------------------------------
def parse_group_acls() -> Dict[str, FrozenSet["ACL"]]:
    group_acls = {}

    try:
        acls_dir = os.getenv("DLREPO_ACLS_DIR", "/etc/dlrepo/acls")
        for file in pathlib.Path(acls_dir).iterdir():
            if not file.is_file():
                continue
            acls = set()
            for line in file.read_text().splitlines():
                tokens = shlex.split(line, comments=True)
                if len(tokens) < 2:
                    continue
                access, *args = tokens
                if access not in ("ro", "rw"):
                    continue
                globs = []
                for a in args:
                    if a.startswith("!"):
                        globs.append((a[1:], True))
                    else:
                        globs.append((a, False))
                acls.add(ACL(access == "rw", frozenset(globs)))
            group_acls[file.name] = frozenset(acls)

    except FileNotFoundError as e:
        if not AuthBackend.AUTH_DISABLED:
            LOG.error("DLREPO_ACLS_DIR: %s", e)

    return group_acls


# --------------------------------------------------------------------------------------
class ACL:
    def __init__(self, read_write: bool, globs: FrozenSet[Tuple[str, bool]]):
        self.read_write = read_write
        self.globs = globs
        self.can_expand_user = any("$user" in g for g, _ in self.globs)
        self.patterns = [
            (self.translate_acl_glob(glob), invert) for glob, invert in self.globs
        ]

    def expand_user(self, login: str) -> "ACL":
        if not self.can_expand_user:
            return self
        globs = []
        for glob, invert in self.globs:
            globs.append((glob.replace("$user", login), invert))
        return ACL(self.read_write, frozenset(globs))

    def access_granted(self, is_write: bool, path: str) -> bool:
        if is_write and not self.read_write:
            return False
        granted = True
        for pattern, invert in self.patterns:
            if pattern.match(path):
                if invert:
                    granted = False
                    break
            else:
                if not invert:
                    granted = False
                    break
        return granted

    @staticmethod
    def translate_acl_glob(glob: str) -> re.Pattern:
        pattern = r"^"
        i = 0
        while i < len(glob):
            c = glob[i]
            i += 1
            if c == "*":
                if i < len(glob) and glob[i] == "*":
                    i += 1
                    pattern += r".*"
                else:
                    pattern += r"[^/]*"
            elif c == "?":
                pattern += r"[^/]"
            else:
                pattern += re.escape(c)
        pattern += r"$"
        return re.compile(pattern)

    def __str__(self):
        access = "rw" if self.read_write else "ro"
        globs = []
        for glob, invert in self.globs:
            if invert:
                glob = f"!{glob}"
            globs.append(glob)
        return f"{access} {' '.join(globs)}"

    def __repr__(self):
        return f"ACL(read_write={self.read_write}, globs={self.globs})"

    def __eq__(self, other):
        if not isinstance(other, ACL):
            return False
        return other.read_write == self.read_write and other.globs == self.globs

    def __hash__(self):
        return hash((self.read_write, self.globs))
