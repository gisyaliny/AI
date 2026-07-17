#!/usr/bin/env python3
"""Strip leading numeric prefixes from titles in .md and .ipynb files.

Usage: python scripts\strip_titles.py [--root PATH] [--dry-run] [--backup]

This script scans the repository for Markdown and Jupyter notebook files,
removes leading numbering from top-level titles (YAML front-matter `title:`
or first-level `# ` headings / first markdown cell), and writes changes
in-place by default.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
from pathlib import Path
from typing import Tuple


EXCLUDE_DIRS = {".git", "_build", "_output", "node_modules", ".venv", "venv", ".ipynb_checkpoints"}


def strip_leading_numbers(s: str) -> str:
    # Remove repeated leading numeric tokens with punctuation and whitespace.
    return re.sub(r'^(?:\s*)(?:\d+[.\-–—\):]*\s*)+(.*)$', r"\1", s).strip()


def fix_markdown_file(path: Path) -> Tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    orig = text

    # Handle YAML front-matter title
    if text.startswith("---"):
        parts = text.split("\n")
        # find end of front matter
        try:
            end = parts.index("---", 1)
        except ValueError:
            end = None

        if end:
            fm_lines = parts[1:end]
            changed = False
            for i, line in enumerate(fm_lines):
                m = re.match(r'^(title\s*:\s*)(["\']?)(.*)$', line)
                if m:
                    key, quote, val = m.groups()
                    stripped = strip_leading_numbers(val.strip().strip('"\''))
                    newval = f'{key}{quote}{stripped}{quote}'
                    if newval != line:
                        fm_lines[i] = newval
                        changed = True
            if changed:
                parts[1:end] = fm_lines
                text = "\n".join(parts)
    # If not changed by front matter, look for first-level heading
    if text == orig:
        lines = text.splitlines(True)
        changed = False
        for idx, line in enumerate(lines):
            m = re.match(r'^(\s*#{1,6}\s+)(.*)$', line)
            if m:
                prefix, rest = m.groups()
                new_rest = strip_leading_numbers(rest)
                if new_rest != rest.strip():
                    lines[idx] = prefix + new_rest + ("\n" if line.endswith("\n") else "")
                    changed = True
        if changed:
            text = "".join(lines)

    if text != orig:
        return True, text
    return False, text


def fix_ipynb_file(path: Path) -> Tuple[bool, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    orig = json.dumps(data, ensure_ascii=False)
    changed = False
    cells = data.get("cells", [])
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        src = cell.get("source", [])
        if not src:
            continue
        # normalize to list of lines for processing
        if isinstance(src, list):
            lines = src
            as_list = True
        else:
            lines = src.splitlines(True)
            as_list = False
        cell_changed = False
        for i, line in enumerate(lines):
            m = re.match(r'^(\s*#{1,6}\s+)(.*)$', line)
            if m:
                prefix, rest = m.groups()
                new_rest = strip_leading_numbers(rest)
                if new_rest != rest.strip():
                    lines[i] = prefix + new_rest + ("\n" if line.endswith("\n") else "")
                    cell_changed = True
        if cell_changed:
            if as_list:
                cell["source"] = lines
            else:
                cell["source"] = "".join(lines)
            changed = True
    if changed:
        return True, json.dumps(data, ensure_ascii=False, indent=1)
    return False, orig


def should_skip(dirpath: Path) -> bool:
    parts = {p for p in dirpath.parts}
    return bool(parts & EXCLUDE_DIRS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Root directory to scan")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup", action="store_true", help="Create .bak backup files")
    args = parser.parse_args()

    root = Path(args.root)
    modified = []
    for dirpath, dirnames, filenames in os.walk(root):
        pdir = Path(dirpath)
        if should_skip(pdir):
            dirnames[:] = []
            continue
        for fn in filenames:
            path = pdir / fn
            if path.suffix.lower() == ".md":
                ok, new = fix_markdown_file(path)
                if ok:
                    modified.append(str(path))
                    if not args.dry_run:
                        if args.backup:
                            bak = path.with_suffix(path.suffix + ".bak")
                            bak.write_bytes(path.read_bytes())
                        path.write_text(new, encoding="utf-8")
            elif path.suffix.lower() == ".ipynb":
                ok, new = fix_ipynb_file(path)
                if ok:
                    modified.append(str(path))
                    if not args.dry_run:
                        if args.backup:
                            bak = path.with_suffix(path.suffix + ".bak")
                            bak.write_bytes(path.read_bytes())
                        path.write_text(new, encoding="utf-8")

    if modified:
        print("Modified files:")
        for m in modified:
            print(" -", m)
        return 0
    print("No changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
