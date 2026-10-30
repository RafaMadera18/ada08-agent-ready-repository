"""Tests for the repository checks in scripts/."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contract = load("check_repo_contract")
protected = load("check_protected_paths")


def write(root, rel, text="x"):
    path = Path(root) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_valid_tree(root):
    for rel in contract.REQUIRED_FILES:
        write(root, rel)
    (Path(root) / "results").mkdir()
    sections = "\n".join(contract.AGENTS_SECTIONS)
    mentions = " ".join(contract.AGENTS_MUST_MENTION)
    write(root, "AGENTS.md", f"{sections}\n{mentions}\n")
    write(root, "REQUIREMENTS.md", "REQ-001 REQ-002")
    write(root, "SPEC.md", "REQ-001 REQ-002")


class TestRepoContract(unittest.TestCase):
    def test_valid_tree_has_no_problems(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_valid_tree(tmp)
            self.assertEqual(contract.run_all(Path(tmp)), [])

    def test_missing_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_valid_tree(tmp)
            (Path(tmp) / "docs" / "REPO_MAP.md").unlink()
            problems = contract.check_required_files(Path(tmp))
            self.assertEqual(problems, ["Missing file: docs/REPO_MAP.md"])

    def test_agents_without_stop_conditions_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_valid_tree(tmp)
            text = (Path(tmp) / "AGENTS.md").read_text(encoding="utf-8")
            write(tmp, "AGENTS.md", text.replace("## Stop Conditions", ""))
            problems = contract.check_agents_contract(Path(tmp))
            self.assertEqual(problems, ["AGENTS.md lacks section: ## Stop Conditions"])

    def test_requirement_without_spec_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_valid_tree(tmp)
            write(tmp, "REQUIREMENTS.md", "REQ-001 REQ-002 REQ-003")
            problems = contract.check_traceability(Path(tmp))
            self.assertEqual(len(problems), 1)
            self.assertIn("REQ-003", problems[0])

    def test_doc_pointing_to_missing_path_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_valid_tree(tmp)
            write(tmp, "docs/REPO_MAP.md", "See `docs/missing.md` and `SPEC.md`.")
            problems = contract.check_doc_paths(Path(tmp), ["docs/REPO_MAP.md"])
            self.assertEqual(len(problems), 1)
            self.assertIn("docs/missing.md", problems[0])

    def test_secret_pattern_is_detected(self):
        fake_token = "gh" + "p_" + "A" * 36
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "notes.txt", f"token = {fake_token}")
            problems = contract.check_secrets(Path(tmp))
            self.assertEqual(len(problems), 1)
            self.assertIn("notes.txt", problems[0])

    def test_env_file_is_detected_but_example_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, ".env")
            write(tmp, ".env.example")
            problems = contract.check_secrets(Path(tmp))
            self.assertEqual(problems, ["Sensitive file is versioned: .env"])


class TestProtectedPaths(unittest.TestCase):
    def test_modifying_requirements_is_a_violation(self):
        self.assertEqual(len(protected.find_violations([("M", "REQUIREMENTS.md")])), 1)

    def test_adding_a_protected_file_is_allowed(self):
        self.assertEqual(protected.find_violations([("A", "REQUIREMENTS.md")]), [])

    def test_workflow_change_is_a_violation(self):
        changes = [("M", ".github/workflows/verify.yml")]
        self.assertEqual(len(protected.find_violations(changes)), 1)

    def test_untracked_env_file_is_a_violation(self):
        self.assertEqual(len(protected.find_violations([("?", ".env")])), 1)

    def test_env_example_is_allowed(self):
        self.assertEqual(protected.find_violations([("?", ".env.example")]), [])

    def test_normal_source_change_is_allowed(self):
        changes = [("M", "src/calculator.py"), ("M", "tests/test_calculator.py"), ("M", "SPEC.md")]
        self.assertEqual(protected.find_violations(changes), [])


if __name__ == "__main__":
    unittest.main()
