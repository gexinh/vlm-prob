#!/usr/bin/env python3
"""Fast-forward the personal and lab main branches to one reviewed commit."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], check=check, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def synchronize(repo: Path, remotes: tuple[str, str], branch: str, push: bool) -> str:
    git(repo, "check-ref-format", "--branch", branch)
    if remotes[0] == remotes[1]:
        raise ValueError("Choose two different remote names.")
    current = git(repo, "symbolic-ref", "--quiet", "--short", "HEAD").stdout.strip()
    if current != branch:
        raise ValueError(f"Check out {branch} before synchronizing it (current: {current}).")
    if push and git(repo, "status", "--porcelain").stdout.strip():
        raise ValueError("Commit or set aside local changes before publishing.")
    target = git(repo, "rev-parse", f"refs/heads/{branch}").stdout.strip()
    for remote in remotes:
        git(repo, "remote", "get-url", remote)
        # Explicit refspec avoids a stale tracking ref or unrelated branch.
        git(repo, "fetch", remote, f"refs/heads/{branch}:refs/remotes/{remote}/{branch}")
    heads = {remote: git(repo, "rev-parse", f"refs/remotes/{remote}/{branch}").stdout.strip()
             for remote in remotes}
    # Complete BOTH ancestry checks before writing to either remote.
    for remote, head in heads.items():
        if git(repo, "merge-base", "--is-ancestor", head, target, check=False).returncode:
            raise ValueError(f"{remote}/{branch} contains changes absent from local {branch}. "
                             "Merge those changes locally, review, and retry. Nothing was pushed.")
    print(f"Local {branch}: {target}")
    for remote, head in heads.items():
        print(f"{remote}/{branch}: {head}" + (" (synchronized)" if head == target else " (can fast-forward)"))
    if not push:
        print("Check only. Add --push to update both remotes.")
        return target
    for remote, head in heads.items():
        if head != target:
            # Pin the verified commit; never force or delete remote refs.
            git(repo, "push", remote, f"{target}:refs/heads/{branch}")
    mismatches = []
    for remote in remotes:
        line = git(repo, "ls-remote", remote, f"refs/heads/{branch}").stdout.strip()
        if not line or line.split()[0] != target:
            mismatches.append(remote)
    if mismatches:
        raise ValueError("Remote verification failed for " + ", ".join(mismatches) +
                         ". A concurrent update may have occurred; inspect both remotes before retrying.")
    print(f"Verified: both remotes point to {target}")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Local Git checkout (default: current directory)")
    parser.add_argument("--personal", default="personal", help="Personal remote name")
    parser.add_argument("--lab", default="lab", help="Laboratory remote name")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--push", action="store_true", help="Publish after checking both histories; default is check-only")
    args = parser.parse_args()
    try:
        synchronize(args.repo, (args.personal, args.lab), args.branch, args.push)
    except (ValueError, subprocess.CalledProcessError) as error:
        detail = error.stderr.strip() if isinstance(error, subprocess.CalledProcessError) else str(error)
        parser.exit(1, detail + "\n")


if __name__ == "__main__":
    main()
