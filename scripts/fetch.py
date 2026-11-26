#!/usr/bin/env python3
"""Check the stored third-party skills against their sources.

    python scripts/fetch.py            report which skills changed upstream
    python scripts/fetch.py --apply    also replace them and record the new commits

Only the "skills" list in sources.json is processed. External projects are
installed by each harness and are skipped. Nothing is installed or committed.
"""

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources.json"
SKILLS = ROOT / "skills"


def git(*args, cwd=None):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True)
    if result.returncode != 0:
        message = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"git {args[0]} failed: {message}")
    return result.stdout


def remove_clones(workdir):
    """Delete the temporary clones. Git marks some files read-only, which stops Windows."""
    def make_writable(function, path, _):
        try:
            os.chmod(path, stat.S_IWRITE)
            function(path)
        except OSError:
            print(f"warning: could not delete {path}", file=sys.stderr)

    shutil.rmtree(workdir, onerror=make_writable)


def upstream_files(clone, path):
    """Return {relative path: bytes} for one skill folder, exactly as stored in git."""
    listing = git("ls-tree", "-r", "-z", "HEAD", "--", f"{path}/", cwd=clone)
    files = {}
    for entry in filter(None, listing.split(b"\0")):
        info, name = entry.split(b"\t", 1)
        mode, _, blob = info.decode().split()
        relative = PurePosixPath(name.decode()).relative_to(path)
        if mode not in ("100644", "100755"):
            raise RuntimeError(f"{relative} is a link or submodule, which is not supported")
        files[relative.as_posix()] = git("cat-file", "blob", blob, cwd=clone)
    if "SKILL.md" not in files:
        raise RuntimeError(f"no SKILL.md in '{path}' upstream (was it moved?)")
    return files


def local_files(folder):
    return {
        file.relative_to(folder).as_posix(): file.read_bytes()
        for file in folder.rglob("*")
        if file.is_file()
    }


def replace_folder(folder, files):
    """Write the new copy next to the old one first, then swap them."""
    SKILLS.mkdir(exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".fetch-", dir=SKILLS))
    try:
        for relative, content in files.items():
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        if folder.exists():
            shutil.rmtree(folder)
        staging.rename(folder)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def process(skill, clones, workdir, apply):
    """Handle one skill. Return True if it differs from upstream."""
    name = skill["name"]
    # The name becomes a folder that --apply deletes, so it must stay inside skills/.
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", name):
        raise RuntimeError("invalid skill name")

    key = (skill["repo"], skill["ref"])
    if key not in clones:
        clone = Path(workdir) / str(len(clones))
        git("clone", "--quiet", "--filter=blob:none", "--no-checkout",
            "--single-branch", "--branch", skill["ref"], "--", skill["repo"], str(clone))
        clones[key] = clone
    clone = clones[key]

    path = skill["path"].strip("/")
    new = upstream_files(clone, path)
    folder = SKILLS / name
    old = local_files(folder)

    if old == new:
        print(f"{name}: up to date")
        return False

    commit = git("log", "-1", "--format=%H", "HEAD", "--", path, cwd=clone).decode().strip()
    print(f"{name}: differs from upstream ({skill['commit'][:7]} -> {commit[:7]})")
    for relative in sorted(old.keys() | new.keys()):
        if relative not in old:
            print(f"  added    {relative}")
        elif relative not in new:
            print(f"  removed  {relative}")
        elif old[relative] != new[relative]:
            print(f"  changed  {relative}")

    if apply:
        replace_folder(folder, new)
        skill["commit"] = commit
        print("  updated")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true",
                        help="replace changed skills and update sources.json")
    args = parser.parse_args()

    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    clones = {}
    changed = failed = 0

    workdir = tempfile.mkdtemp(prefix="fetch-skills-")
    try:
        for skill in sources["skills"]:
            try:
                changed += process(skill, clones, workdir, args.apply)
            except (RuntimeError, OSError) as error:
                failed += 1
                print(f"{skill['name']}: ERROR: {error}", file=sys.stderr)
    finally:
        remove_clones(workdir)

    if changed and args.apply:
        with SOURCES.open("w", encoding="utf-8", newline="\n") as file:
            file.write(json.dumps(sources, indent=2) + "\n")
        print("\nReview 'git diff', then update VERSION and CHANGELOG.md and commit.")
    elif changed:
        print("\nRun again with --apply to update.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
