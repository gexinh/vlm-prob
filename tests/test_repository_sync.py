"""Exercise actual Git history and remote writes using disposable local repos."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.sync_repositories import synchronize


class RepositorySyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "checkout"
        self.run_git(self.root, "init", "--initial-branch=main", str(self.repo))
        self.run_git(self.repo, "config", "user.name", "Sync test")
        self.run_git(self.repo, "config", "user.email", "sync@example.invalid")
        self.commit("base")
        for remote in ("personal", "lab"):
            bare = self.root / remote
            self.run_git(self.root, "init", "--bare", "--initial-branch=main", str(bare))
            self.run_git(self.repo, "remote", "add", remote, str(bare))
            self.run_git(self.repo, "push", remote, "main")

    @staticmethod
    def run_git(repo, *args):
        return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE, text=True).strip()

    def commit(self, text):
        (self.repo / "file").write_text(text)
        self.run_git(self.repo, "add", "file")
        self.run_git(self.repo, "commit", "-m", text)
        return self.run_git(self.repo, "rev-parse", "HEAD")

    def head(self, remote):
        return self.run_git(self.repo, "ls-remote", remote, "refs/heads/main").split()[0]

    def test_check_does_not_push_and_push_updates_both(self):
        previous = self.head("personal")
        target = self.commit("next")
        synchronize(self.repo, ("personal", "lab"), "main", False)
        self.assertEqual(self.head("personal"), previous)
        self.assertEqual(self.head("lab"), previous)
        synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("personal"), target)
        self.assertEqual(self.head("lab"), target)

    def test_remote_ahead_prevents_writes_to_other_remote(self):
        previous = self.head("personal")
        self.commit("lab-only")
        self.run_git(self.repo, "push", "lab", "main")
        self.run_git(self.repo, "reset", "--hard", previous)
        self.commit("local-only")
        with self.assertRaisesRegex(ValueError, "Nothing was pushed"):
            synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("personal"), previous)

    def test_dirty_tree_is_not_published(self):
        previous = self.head("lab")
        (self.repo / "file").write_text("unreviewed")
        with self.assertRaisesRegex(ValueError, "local changes"):
            synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("lab"), previous)


if __name__ == "__main__":
    unittest.main()
