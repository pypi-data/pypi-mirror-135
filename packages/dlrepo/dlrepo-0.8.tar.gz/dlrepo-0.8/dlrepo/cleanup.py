# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

"""
Automatically cleanup old tags according to the branch cleanup policy.
"""

import argparse
import os
import pathlib
import re
import sys
import time

from dlrepo.fs import ArtifactRepository
from dlrepo.fs.tag import Tag


# --------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-q",
        "--quiet",
        default=False,
        action="store_true",
        help="""
        Only display errors.
        """,
    )
    parser.add_argument(
        "-p",
        "--root-path",
        type=local_dir,
        default=default_root_path(),
        help="""
        The root path of the repository. Default to DLREPO_ROOT_DIR from the
        environment or from /etc/default/dlrepo.
        """,
    )
    args = parser.parse_args()
    try:
        cleanup(args)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------------------
def cleanup(args):
    repo = ArtifactRepository(args.root_path)
    start = time.time()
    deleted = 0

    for branch in repo.get_branches():
        released_tags = []
        daily_tags = []

        for tag in branch.get_tags():
            if tag.is_locked():
                continue
            if tag.is_released():
                released_tags.append(tag)
            else:
                daily_tags.append(tag)

        released_tags.sort(key=Tag.creation_date, reverse=True)
        daily_tags.sort(key=Tag.creation_date, reverse=True)

        policy = branch.get_cleanup_policy()
        max_daily = policy.get("max_daily_tags", 0)
        if isinstance(max_daily, int) and max_daily > 0:
            for tag in daily_tags[max_daily:]:
                if not args.quiet:
                    print(f"Deleting daily tag {branch.name}/{tag.name} ...")
                tag.delete(cleanup_orphans=False)
                deleted += 1

        max_released = policy.get("max_released_tags", 0)
        if isinstance(max_released, int) and max_released > 0:
            for tag in released_tags[max_released:]:
                if not args.quiet:
                    print(f"Deleting released tag {branch.name}/{tag.name} ...")
                tag.delete(force=True, cleanup_orphans=False)
                deleted += 1

    repo.cleanup_orphan_blobs()

    for user_repo in repo.get_user_repos():
        user_repo.disk_usage_refresh()
        user_repo.disk_usage_save()

    if not args.quiet and deleted > 0:
        print(f"Deleted {deleted} tags in {time.time() - start:.1f}s")


# --------------------------------------------------------------------------------------
def local_dir(value):
    value = pathlib.Path(value)
    if not value.is_dir():
        raise argparse.ArgumentTypeError(f"{value}: No such directory")
    return value


# --------------------------------------------------------------------------------------
def default_root_path():
    if "DLREPO_ROOT_DIR" in os.environ:
        return pathlib.Path(os.environ["DLREPO_ROOT_DIR"])

    default_file = pathlib.Path("/etc/default/dlrepo")
    if default_file.is_file():
        match = re.search(
            r"DLREPO_ROOT_DIR=(.*)", default_file.read_text(encoding="utf-8")
        )
        if match:
            return pathlib.Path(match.group(1).strip().strip("\"'"))

    return pathlib.Path(".")


# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
