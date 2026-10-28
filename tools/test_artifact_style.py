"""Artifact-style failure controls in isolated temporary repositories."""
import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest

from check_artifact_style import check


class ArtifactStyleTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git('init', '-q')

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args],
                              capture_output=True, check=True)

    def track(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        self.git('add', '--', name)

    def run_check(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = check(self.root)
        return result, output.getvalue()

    def test_clean_text_and_untracked_files(self):
        self.track('README.md', 'Clear text.\n')
        (self.root/'scratch.md').write_text(chr(0x2014), encoding='utf-8')
        result, output = self.run_check()
        self.assertEqual(result, 0)
        self.assertIn('1 tracked text files', output)

    def test_all_three_rules_report_the_file_and_line(self):
        for marker, label in ((chr(0x2014), 'em dash'),
                              (chr(0x2026), 'Unicode ellipsis'),
                              ('.'*3, 'three-dot ellipsis')):
            with self.subTest(rule=label):
                self.track('README.md', 'First line.\nSecond '+marker+' line.\n')
                result, output = self.run_check()
                self.assertEqual(result, 1)
                self.assertIn('README.md:2: '+label, output)

    def test_checks_each_tracked_text_artifact_type(self):
        names = ('README.md', 'collections.json', 'queue.csv', 'queue.tsv', 'tools/check.py',
                 '.github/workflows/check.yml', 'workflow.yaml', 'notes.txt',
                 'settings.toml', 'check.sh', '.gitignore', '.gitattributes', '.editorconfig')
        for name in names:
            self.track(name, chr(0x2014)+'\n')
        result, output = self.run_check()
        self.assertEqual(result, 1)
        for name in names:
            self.assertIn(name+':1: em dash', output)

    def test_reads_unstaged_edits_and_fails_on_missing_tracked_files(self):
        self.track('README.md', 'Clean.\n')
        (self.root/'README.md').write_text(chr(0x2026), encoding='utf-8')
        self.assertEqual(self.run_check()[0], 1)
        (self.root/'README.md').unlink()
        with self.assertRaises(FileNotFoundError):
            self.run_check()

    def test_binary_files_are_outside_the_text_scope(self):
        path = self.root/'image.png'
        path.write_bytes(b'\x89PNG\x00\xff')
        self.git('add', '--', path.name)
        self.assertEqual(self.run_check()[0], 0)


if __name__ == '__main__':
    unittest.main()
