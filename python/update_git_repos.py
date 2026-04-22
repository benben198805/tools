# /// script
# requires-python = ">=3.10"
# ///
"""
Recursively find Git work trees under a root path. For each repository:

1. Log directories that look like projects but have no ``.git``, and skip paths
   whose ``.git`` is not a valid work tree.
2. Print every ``git`` command before it runs (or as a dry-run preview).
3. Record the current branch (or detached HEAD SHA). If there are local
   changes, ``git stash push -u`` with a fixed message.
4. ``git fetch``, check out the target branch (default ``master``), then
   ``git pull --rebase``.
5. If a stash was created: switch back to the original branch/SHA and
   ``git stash pop`` (after a successful pull, or after a failure once the
   worktree may have moved to the target branch).
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


_STASH_MESSAGE = "update_git_repos: auto-stash before pull --rebase"

_SKIP_SUBDIRS = frozenset(
    {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        ".mypy_cache",
        ".tox",
        "target",
        "dist",
        "build",
    }
)


def _print_cmd(cwd: Path, argv: list[str]) -> None:
    cmd = ["git", *argv]
    print(f"  $ cd {cwd} && {subprocess.list2cmdline(cmd)}")


def _git(
    cwd: Path,
    argv: list[str],
    *,
    dry_run: bool,
    mutates: bool = True,
) -> subprocess.CompletedProcess[str]:
    """
    Run a git subprocess. Always prints the command line.

    If ``dry_run`` and ``mutates`` is True, only print; do not run.
    Read-only commands set ``mutates=False`` so they always execute.
    """
    _print_cmd(cwd, argv)
    cmd = ["git", *argv]
    if dry_run and mutates:
        return subprocess.CompletedProcess(cmd, 0, "", "")
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def is_git_worktree(cwd: Path, *, trace: bool = False) -> bool:
    argv = ["-C", str(cwd), "rev-parse", "--is-inside-work-tree"]
    if trace:
        print(f"  $ {subprocess.list2cmdline(['git', *argv])}")
    p = subprocess.run(
        ["git", *argv],
        text=True,
        capture_output=True,
        check=False,
    )
    return p.returncode == 0 and (p.stdout or "").strip() == "true"


def log_non_git_immediate_children(root: Path) -> None:
    """One-line hint for direct subdirs of root that have no ``.git``."""
    r = root.expanduser().resolve()
    if not r.is_dir():
        return
    for child in sorted(r.iterdir(), key=lambda p: p.name.casefold()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if (child / ".git").exists():
            continue
        print(f"Note: not a Git repository (no .git): {child}")


def find_git_worktrees(root: Path) -> list[Path]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Not a directory: {root}")
    repos: set[Path] = set()
    for dirpath, dirnames, _files in os.walk(root, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_SUBDIRS]
        here = Path(dirpath)
        if not (here / ".git").exists():
            continue
        if is_git_worktree(here, trace=False):
            repos.add(here)
        else:
            print(f"Note: skipping (has .git but not a valid work tree): {here}")
    return sorted(repos, key=lambda p: str(p).casefold())


def worktree_is_dirty(cwd: Path, *, dry_run: bool) -> bool:
    p = _git(cwd, ["status", "--porcelain"], dry_run=dry_run, mutates=False)
    if p.returncode != 0:
        return False
    return bool((p.stdout or "").strip())


def get_current_ref(cwd: Path, *, dry_run: bool) -> tuple[str, str]:
    """``('branch', name)`` or ``('detached', sha)``."""
    p = _git(cwd, ["symbolic-ref", "-q", "--short", "HEAD"], dry_run=dry_run, mutates=False)
    if p.returncode == 0:
        name = (p.stdout or "").strip()
        if name:
            return ("branch", name)
    p2 = _git(cwd, ["rev-parse", "HEAD"], dry_run=dry_run, mutates=False)
    sha = (p2.stdout or "").strip() if p2.returncode == 0 else "HEAD"
    return ("detached", sha)


def stash_worktree(cwd: Path, *, dry_run: bool) -> tuple[bool, str | None]:
    if not worktree_is_dirty(cwd, dry_run=dry_run):
        return False, None
    p = _git(cwd, ["stash", "push", "-u", "-m", _STASH_MESSAGE], dry_run=dry_run, mutates=True)
    if p.returncode != 0:
        err = (p.stderr or p.stdout or "").strip()
        return False, err or f"git stash failed with exit {p.returncode}"
    return True, None


def checkout_branch(cwd: Path, branch: str, remote: str, *, dry_run: bool) -> str | None:
    fe = _git(cwd, ["fetch", remote], dry_run=dry_run, mutates=True)
    if fe.returncode != 0:
        return (fe.stderr or fe.stdout or "").strip() or f"git fetch {remote} failed"

    for argv in (["switch", branch], ["checkout", branch]):
        sw = _git(cwd, argv, dry_run=dry_run, mutates=True)
        if sw.returncode == 0:
            return None

    track = f"{remote}/{branch}"
    sw2 = _git(
        cwd,
        ["switch", "-c", branch, "--track", track],
        dry_run=dry_run,
        mutates=True,
    )
    if sw2.returncode == 0:
        return None

    sw3 = _git(cwd, ["checkout", "-b", branch, track], dry_run=dry_run, mutates=True)
    if sw3.returncode == 0:
        return None

    tail = (sw3.stderr or sw2.stderr or "").strip()
    return tail or f"could not check out branch {branch!r} from {track!r}"


def pull_rebase(cwd: Path, remote: str, branch: str, *, dry_run: bool) -> str | None:
    pr = _git(cwd, ["pull", "--rebase", remote, branch], dry_run=dry_run, mutates=True)
    if pr.returncode != 0:
        return (pr.stderr or pr.stdout or "").strip() or "git pull --rebase failed"
    return None


def checkout_ref(cwd: Path, ref_kind: str, ref_value: str, *, dry_run: bool) -> str | None:
    """Check out original branch name or detached SHA."""
    if ref_kind == "branch":
        last: subprocess.CompletedProcess[str] | None = None
        for argv in (["switch", ref_value], ["checkout", ref_value]):
            last = _git(cwd, argv, dry_run=dry_run, mutates=True)
            if last.returncode == 0:
                return None
        tail = (
            ((last.stderr or last.stdout) if last else "") or ""
        ).strip()
        return tail or f"could not check out {ref_value!r}"
    r = _git(cwd, ["checkout", ref_value], dry_run=dry_run, mutates=True)
    if r.returncode != 0:
        return (r.stderr or r.stdout or "").strip() or f"could not checkout {ref_value!r}"
    return None


def restore_original_and_stash_pop(
    cwd: Path,
    orig: tuple[str, str],
    *,
    dry_run: bool,
) -> str | None:
    now = get_current_ref(cwd, dry_run=dry_run)
    if (now[0], now[1]) != (orig[0], orig[1]):
        err = checkout_ref(cwd, orig[0], orig[1], dry_run=dry_run)
        if err:
            return f"restore branch/sha: {err}"
    pop = _git(cwd, ["stash", "pop"], dry_run=dry_run, mutates=True)
    if pop.returncode != 0:
        return (pop.stderr or pop.stdout or "").strip() or "git stash pop failed"
    return None


@dataclass(frozen=True)
class UpdateReport:
    path: Path
    ok: bool
    stashed: bool
    error: str | None = None


def update_one_repo(
    cwd: Path,
    *,
    branch: str,
    remote: str,
    dry_run: bool,
) -> UpdateReport:
    orig = get_current_ref(cwd, dry_run=dry_run)
    stashed, err = stash_worktree(cwd, dry_run=dry_run)
    if err:
        return UpdateReport(path=cwd, ok=False, stashed=False, error=f"stash: {err}")

    def _recover_if_stashed(stage: str) -> UpdateReport | None:
        if not stashed:
            return None
        rec_err = restore_original_and_stash_pop(cwd, orig, dry_run=dry_run)
        if rec_err:
            return UpdateReport(
                path=cwd,
                ok=False,
                stashed=stashed,
                error=f"{stage}; then restore failed: {rec_err}",
            )
        return None

    err = checkout_branch(cwd, branch, remote, dry_run=dry_run)
    if err:
        bad = _recover_if_stashed(f"checkout/fetch: {err}")
        if bad:
            return bad
        return UpdateReport(path=cwd, ok=False, stashed=stashed, error=err)

    err = pull_rebase(cwd, remote, branch, dry_run=dry_run)
    if err:
        bad = _recover_if_stashed(f"pull: {err}")
        if bad:
            return bad
        return UpdateReport(path=cwd, ok=False, stashed=stashed, error=err)

    if stashed:
        rec_err = restore_original_and_stash_pop(cwd, orig, dry_run=dry_run)
        if rec_err:
            return UpdateReport(
                path=cwd,
                ok=False,
                stashed=stashed,
                error=f"pull ok, but {rec_err}",
            )

    return UpdateReport(path=cwd, ok=True, stashed=stashed, error=None)


def _display_path(cwd: Path) -> str:
    try:
        return str(cwd.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(cwd.resolve())


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Stash dirty repos, pull --rebase a branch, print all git commands, "
        "restore original branch and stash pop when a stash was created.",
    )
    ap.add_argument("root", type=Path, help="Root directory to scan recursively.")
    ap.add_argument(
        "-b",
        "--branch",
        default="master",
        help="Branch to check out and pull (default: master).",
    )
    ap.add_argument("-r", "--remote", default="origin", help="Remote name (default: origin).")
    ap.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Print git commands only; skip mutating operations (read-only git still runs).",
    )
    args = ap.parse_args()

    try:
        log_non_git_immediate_children(args.root)
        repos = find_git_worktrees(args.root)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if not repos:
        print(f"No Git repositories found under {args.root.expanduser().resolve()}")
        return 0

    print(
        f"Root: {args.root.expanduser().resolve()}\n"
        f"Repos: {len(repos)} | remote={args.remote!r} | branch={args.branch!r} | "
        f"dry_run={args.dry_run}\n"
    )

    reports: list[UpdateReport] = []
    for cwd in repos:
        label = _display_path(cwd)
        print(f"== {label}")
        rep = update_one_repo(
            cwd,
            branch=args.branch,
            remote=args.remote,
            dry_run=args.dry_run,
        )
        reports.append(rep)
        if rep.ok:
            if rep.stashed and args.dry_run:
                suffix = " (had local changes; stash + restore were dry-run only)"
            elif rep.stashed:
                suffix = " (stashed, pulled, restored branch + stash pop)"
            else:
                suffix = ""
            print(f"  OK{suffix}\n")
        else:
            print(f"  FAILED: {rep.error}\n", file=sys.stderr)

    n_ok = sum(1 for r in reports if r.ok)
    n_bad = len(reports) - n_ok
    print(f"Done: {n_ok} succeeded, {n_bad} failed, {len(reports)} total.")
    return 1 if n_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
