"""Deterministic repository readiness contract.

Checks that the files, links and rules an agent depends on actually exist.
Exit code 0 prints REPO_CONTRACT: PASS, exit code 1 prints REPO_CONTRACT: FAIL.

Usage: python scripts/check_repo_contract.py [--full]
--full also requires the ADA-08 delivery files (audit, AI usage log, results).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "REQUIREMENTS.md",
    "SPEC.md",
    "ARCHITECTURE.md",
    "TASKS.md",
    "docs/REPO_MAP.md",
    "scripts/verify_repo.sh",
    "src/calculator.py",
    "tests/test_calculator.py",
]
REQUIRED_DIRS = ["results"]
FULL_ONLY_FILES = [
    "REPOSITORY_READINESS_AUDIT.md",
    "AI_USAGE_LOG.md",
    "results/before-agent-run.md",
    "results/after-agent-run.md",
    "results/implicit-knowledge.md",
    "results/readiness-improvement-report.md",
]
AGENTS_SECTIONS = [
    "## Read First",
    "## Sources of Truth",
    "## Standard Commands",
    "## Change Rules",
    "## Stop Conditions",
    "## Definition of Done",
]
AGENTS_MUST_MENTION = ["scripts/verify_repo.sh", "python -m unittest discover tests"]
DOCS_WITH_PATHS = ["AGENTS.md", "docs/REPO_MAP.md"]
PATH_EXTENSIONS = (".md", ".py", ".sh", ".yml")
REQ_ID = re.compile(r"\bREQ-\d{3}\b")

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9]{32,}"),
]
FORBIDDEN_NAMES = (".env", "id_rsa", "id_ed25519")
FORBIDDEN_SUFFIXES = (".pem", ".key")
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="replace")


def check_required_files(root: Path, full: bool = False) -> list[str]:
    problems = []
    files = REQUIRED_FILES + (FULL_ONLY_FILES if full else [])
    for rel in files:
        if not (root / rel).is_file():
            problems.append(f"Missing file: {rel}")
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            problems.append(f"Missing directory: {rel}/")
    return problems


def check_agents_contract(root: Path) -> list[str]:
    if not (root / "AGENTS.md").is_file():
        return []
    text = read(root, "AGENTS.md")
    problems = [f"AGENTS.md lacks section: {s}" for s in AGENTS_SECTIONS if s not in text]
    problems += [f"AGENTS.md does not mention: {m}" for m in AGENTS_MUST_MENTION if m not in text]
    return problems


def check_traceability(root: Path) -> list[str]:
    if not (root / "REQUIREMENTS.md").is_file() or not (root / "SPEC.md").is_file():
        return []
    defined = set(REQ_ID.findall(read(root, "REQUIREMENTS.md")))
    referenced = set(REQ_ID.findall(read(root, "SPEC.md")))
    problems = [f"{r} is in REQUIREMENTS.md but has no section in SPEC.md" for r in sorted(defined - referenced)]
    problems += [f"{r} is in SPEC.md but is not defined in REQUIREMENTS.md" for r in sorted(referenced - defined)]
    return problems


def check_doc_paths(root: Path, docs: list[str] = None) -> list[str]:
    """Backticked file paths in the navigation docs must exist."""
    problems = []
    for doc in docs or DOCS_WITH_PATHS:
        if not (root / doc).is_file():
            continue
        for token in re.findall(r"`([^`\n]+)`", read(root, doc)):
            token = token.strip()
            if " " in token or "*" in token or "<" in token:
                continue
            if token.startswith("./"):
                token = token[2:]
            if token.endswith(PATH_EXTENSIONS) and not (root / token).exists():
                problems.append(f"{doc} points to a path that does not exist: {token}")
    return problems


def tracked_or_all_files(root: Path) -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
        ).stdout.splitlines()
        return [root / line for line in out if (root / line).is_file()]
    except (OSError, subprocess.CalledProcessError):
        return [
            p for p in root.rglob("*")
            if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS)
        ]


def check_secrets(root: Path) -> list[str]:
    problems = []
    for path in tracked_or_all_files(root):
        rel = path.relative_to(root).as_posix()
        name = path.name
        is_example = name.endswith(".example")
        if not is_example and (
            name in FORBIDDEN_NAMES
            or name.startswith(".env.")
            or name.endswith(FORBIDDEN_SUFFIXES)
        ):
            problems.append(f"Sensitive file is versioned: {rel}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                problems.append(f"Possible secret in {rel} (pattern {pattern.pattern[:12]}...)")
    return problems


def run_all(root: Path, full: bool = False) -> list[str]:
    problems = []
    problems += check_required_files(root, full)
    problems += check_agents_contract(root)
    problems += check_traceability(root)
    problems += check_doc_paths(root)
    problems += check_secrets(root)
    return problems


def main(argv: list[str]) -> int:
    problems = run_all(ROOT, full="--full" in argv)
    if problems:
        print("REPO_CONTRACT: FAIL")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("REPO_CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
