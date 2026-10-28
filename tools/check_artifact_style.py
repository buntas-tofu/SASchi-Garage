#!/usr/bin/env python3
"""Check tracked Garage text artifacts; not an evidence or semantic gate."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = {'.md', '.json', '.csv', '.tsv', '.py', '.yml', '.yaml', '.txt', '.toml', '.sh'}
TEXT_NAMES = {'.gitignore', '.gitattributes', '.editorconfig'}
RULES = ((re.compile(r'\u2014'), 'em dash'),
         (re.compile(r'\u2026'), 'Unicode ellipsis'),
         (re.compile(r'\.{3}'), 'three-dot ellipsis'))


def check(root=ROOT):
    """Read working copies of tracked text files, including staged additions."""
    tracked = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'],
                             capture_output=True, check=True).stdout
    checked, violations = 0, 0
    for name in sorted(set(tracked.decode('utf-8').split('\0')) - {''}):
        path = root / name
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
            continue
        body = path.read_text(encoding='utf-8')
        checked += 1
        for pattern, label in RULES:
            for match in pattern.finditer(body):
                line = body.count('\n', 0, match.start()) + 1
                print(f'{name}:{line}: {label}')
                violations += 1
    if violations:
        print(f'FAIL: {violations} artifact-style violations in {checked} tracked text files')
        return 1
    print(f'PASS: artifact style in {checked} tracked text files')
    return 0


if __name__ == '__main__':
    raise SystemExit(check())
