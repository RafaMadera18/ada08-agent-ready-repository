"""Protected-path guardrail.

Fails when files that need human approval were modified, or when forbidden files
(secrets, keys) were created. Changes are measured against PROTECTED_BASE_REF
(default HEAD, which covers staged, unstaged and untracked work in progress).

Set HUMAN_APPROVED_PROTECTED_CHANGE=1 only after a human approved the change.
Exit code 0 prints PROTECTED_PATHS: PASS, exit code 1 prints PROTECTED_PATHS: FAIL.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent

# Existing files here must not be modified or deleted. Adding them is fine.
PROTECTED = ("REQUIREMENTS.md", "generated/", ".github/workflows/")
# Files of these kinds must never be created or changed.
FORBIDDEN_NAMES = (".env", "id_rsa", "id_ed25519")
FORBIDDEN_SUFFIXES = (".pem", ".key")


def is_protected(path: str) -> bool:
    return any(path == p or (p.endswith("/") and path.startswith(p)) for p in PROTECTED)


def is_forbidden(path: str) -> bool:
    name = PurePosixPath(path).name
    if name.endswith(".example"):
        return False
    return name in FORBIDDEN_NAMES or name.startswith(".env.") or name.endswith(FORBIDDEN_SUFFIXES)


def find_violations(changes: list[tuple[str, str]]) -> list[str]:
    """changes: (status, path) with status A, M, D or ? (untracked)."""
    violations = []
    for status, path in changes:
        if is_forbidden(path):
            violations.append(f"Forbidden file {path} ({status})")
        elif is_protected(path) and status in ("M", "D", "T"):
            violations.append(f"Protected path modified: {path} ({status})")
    return violations


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def collect_changes(base: str) -> list[tuple[str, str]]:
    changes = []
    for line in git("diff", "--name-status", "--no-renames", base).splitlines():
        status, _, path = line.partition("\t")
        changes.append((status[:1], path))
    for path in git("ls-files", "--others", "--exclude-standard").splitlines():
        changes.append(("?", path))
    return changes


def main() -> int:
    base = os.environ.get("PROTECTED_BASE_REF", "HEAD")
    try:
        changes = collect_changes(base)
    except FileNotFoundError:
        print("PROTECTED_PATHS: SKIP (git is not available)")
        return 0
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip().splitlines()[-1:] or ["git failed"]
        if "not a git repository" in (exc.stderr or ""):
            print("PROTECTED_PATHS: SKIP (not a git work tree)")
            return 0
        print(f"PROTECTED_PATHS: FAIL (cannot compare with {base}: {detail[0]})")
        return 1
    violations = find_violations(changes)
    if violations and os.environ.get("HUMAN_APPROVED_PROTECTED_CHANGE") == "1":
        print("PROTECTED_PATHS: PASS (human approval override)")
        for violation in violations:
            print(f"  - approved: {violation}")
        return 0
    if violations:
        print("PROTECTED_PATHS: FAIL")
        for violation in violations:
            print(f"  - {violation}")
        print("Stop and ask a human. See Stop Conditions in AGENTS.md.")
        return 1
    print("PROTECTED_PATHS: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
