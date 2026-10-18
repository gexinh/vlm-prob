"""Exercise README rendering and actual remote writes in disposable Git repos."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.sync_repositories import changed_paths, is_ancestor, readme_at, render_readme, synchronize


PERSONAL_README = '''# vlmprobe
[Project page](https://gexinh.github.io/vlm-probing/)
[Code](https://github.com/gexinh/vlm-probing)
![Icon](https://raw.githubusercontent.com/gexinh/vlm-probing/main/icon.svg)
Install: git+https://github.com/gexinh/vlm-probing.git
[Report source](https://github.com/gexinh/vlm-probing-report)
[External](https://github.com/another/library)
'''


class RepositorySyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "checkout"
        self.run_git(self.root, "init", "--initial-branch=main", str(self.repo))
        self.configure_identity(self.repo)
        (self.repo / "README.md").write_text(PERSONAL_README)
        (self.repo / "version.py").write_text('__version__ = "0.3.0"\n')
        (self.repo / "report.pdf").write_bytes(b"%PDF-test\x00\xff\n")
        self.commit("base")
        for remote in ("personal", "lab"):
            bare = self.root / remote
            self.run_git(self.root, "init", "--bare", "--initial-branch=main", str(bare))
            self.run_git(self.repo, "remote", "add", remote, str(bare))
            self.run_git(self.repo, "push", remote, "main")

    @staticmethod
    def run_git(repo, *args):
        return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE, text=True).strip()

    def configure_identity(self, repo):
        self.run_git(repo, "config", "user.name", "Sync test")
        self.run_git(repo, "config", "user.email", "sync@example.invalid")

    def commit(self, text):
        (self.repo / "file").write_text(text)
        self.run_git(self.repo, "add", "--all")
        self.run_git(self.repo, "commit", "-m", text)
        return self.run_git(self.repo, "rev-parse", "HEAD")

    def head(self, remote):
        return self.run_git(self.repo, "ls-remote", remote, "refs/heads/main").split()[0]

    def assert_matching_trees(self, personal, lab, personal_readme=PERSONAL_README):
        self.assertEqual(changed_paths(self.repo, personal, lab), {"README.md"})
        self.assertEqual(readme_at(self.repo, personal), personal_readme)
        expected = render_readme(personal_readme, "ubc-tea/vlm-probe")
        self.assertEqual(readme_at(self.repo, lab), expected)
        self.assertEqual(expected.count("https://ubc-tea.github.io/vlm-probe/"), 1)
        self.assertNotIn("https://gexinh.github.io/vlm-probing", expected)
        self.assertIn("https://github.com/gexinh/vlm-probing-report", expected)

    def test_rendering_retargets_only_own_urls_and_preserves_readme_structure(self):
        expected = (PERSONAL_README.replace("https://gexinh.github.io/vlm-probing/",
                                           "https://ubc-tea.github.io/vlm-probe/")
                    .replace("https://github.com/gexinh/vlm-probing)",
                             "https://github.com/ubc-tea/vlm-probe)")
                    .replace("https://github.com/gexinh/vlm-probing.git",
                             "https://github.com/ubc-tea/vlm-probe.git")
                    .replace("https://raw.githubusercontent.com/gexinh/vlm-probing/",
                             "https://raw.githubusercontent.com/ubc-tea/vlm-probe/"))
        self.assertEqual(render_readme(PERSONAL_README, "ubc-tea/vlm-probe"), expected)
        self.assertEqual(render_readme(expected, "ubc-tea/vlm-probe"), expected)
        self.assertEqual(render_readme(expected, "gexinh/vlm-probing"), PERSONAL_README)
        crlf = PERSONAL_README.replace("\n", "\r\n")
        self.assertEqual(render_readme(crlf, "ubc-tea/vlm-probe"), expected.replace("\n", "\r\n"))

    def test_check_does_not_push_and_push_only_changes_lab_readme(self):
        previous = self.head("personal")
        target = self.commit("next")
        # A status check normally refreshes cached timestamps in the index.
        # The synchronizer must leave even that metadata untouched.
        path = self.repo / "file"
        stat = path.stat()
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 2_000_000_000))
        index_before = (self.repo / ".git" / "index").read_bytes()
        synchronize(self.repo, ("personal", "lab"), "main", False)
        self.assertEqual(self.head("personal"), previous)
        self.assertEqual(self.head("lab"), previous)
        synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("personal"), target)
        self.assert_matching_trees(target, self.head("lab"))
        self.assertTrue(is_ancestor(self.repo, target, self.head("lab")))
        self.assertEqual(self.run_git(self.repo, "rev-parse", "HEAD"), target)
        self.assertEqual((self.repo / "README.md").read_text(), PERSONAL_README)
        self.assertEqual((self.repo / "file").read_text(), "next")
        self.assertEqual((self.repo / ".git" / "index").read_bytes(), index_before)
        self.assertEqual(self.run_git(self.repo, "status", "--porcelain"), "")

    def test_repeated_updates_preserve_lab_history_and_unchanged_sync_is_noop(self):
        self.commit("first")
        synchronize(self.repo, ("personal", "lab"), "main", True)
        old_lab = self.head("lab")
        updated_readme = PERSONAL_README + "\nUpdated usage documentation\n"
        (self.repo / "README.md").write_text(updated_readme)
        target = self.commit("second")
        synchronize(self.repo, ("personal", "lab"), "main", True)
        new_lab = self.head("lab")
        self.assertTrue(is_ancestor(self.repo, old_lab, new_lab))
        self.assertTrue(is_ancestor(self.repo, target, new_lab))
        self.assert_matching_trees(target, new_lab, updated_readme)
        parents = self.run_git(self.repo, "show", "-s", "--format=%P", new_lab).split()
        self.assertEqual(parents, [old_lab, target])
        synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("personal"), target)
        self.assertEqual(self.head("lab"), new_lab)

    def test_lab_checkout_cannot_publish_lab_links_to_personal_readme(self):
        self.commit("first")
        synchronize(self.repo, ("personal", "lab"), "main", True)
        personal, lab = self.head("personal"), self.head("lab")
        self.run_git(self.repo, "reset", "--hard", lab)
        self.commit("edit-from-lab-checkout")
        with self.assertRaisesRegex(ValueError, "must use the personal repository URLs"):
            synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("personal"), personal)
        self.assertEqual(self.head("lab"), lab)

    def test_lab_library_divergence_prevents_writes_to_both_remotes(self):
        previous = self.head("personal")
        lab_only = self.commit("lab-only")
        self.run_git(self.repo, "push", "lab", "main")
        self.run_git(self.repo, "reset", "--hard", previous)
        self.commit("local-only")
        with self.assertRaisesRegex(ValueError, "Nothing was pushed"):
            synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("personal"), previous)
        self.assertEqual(self.head("lab"), lab_only)

    def test_personal_divergence_prevents_writes_to_both_remotes(self):
        previous = self.head("lab")
        personal_only = self.commit("personal-only")
        self.run_git(self.repo, "push", "personal", "main")
        self.run_git(self.repo, "reset", "--hard", previous)
        self.commit("local-only")
        with self.assertRaisesRegex(ValueError, "Nothing was pushed"):
            synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("personal"), personal_only)
        self.assertEqual(self.head("lab"), previous)

    def test_unexpected_lab_readme_edits_are_not_silently_overwritten(self):
        self.commit("first")
        synchronize(self.repo, ("personal", "lab"), "main", True)
        previous_personal = self.head("personal")
        other = self.root / "collaborator"
        self.run_git(self.root, "clone", str(self.root / "lab"), str(other))
        self.configure_identity(other)
        with (other / "README.md").open("a") as stream:
            stream.write("\nImportant collaborator edit\n")
        self.run_git(other, "add", "README.md")
        self.run_git(other, "commit", "-m", "Edit README")
        self.run_git(other, "push", "origin", "main")
        edited_lab = self.head("lab")
        self.commit("second")
        with self.assertRaisesRegex(ValueError, "unexpected README edits.*Nothing was pushed"):
            synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("personal"), previous_personal)
        self.assertEqual(self.head("lab"), edited_lab)

    def test_dirty_tree_is_not_published(self):
        previous = self.head("lab")
        (self.repo / "file").write_text("unreviewed")
        with self.assertRaisesRegex(ValueError, "local changes"):
            synchronize(self.repo, ("personal", "lab"), "main", True)
        self.assertEqual(self.head("lab"), previous)


if __name__ == "__main__":
    unittest.main()
