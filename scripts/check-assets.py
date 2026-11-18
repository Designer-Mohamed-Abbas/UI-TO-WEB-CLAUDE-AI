#!/usr/bin/env python3
"""
Project: ui-to-web asset checker
Developed by: Mohamed Ahmed Abbas
Role: Front-End Development

Copyright (c) 2026 Mohamed Ahmed Abbas.
All rights reserved.

Usage: check-assets.py <project-dir>

Finds broken local references in HTML/CSS/JS, case mismatches (GitHub Pages is
case-sensitive), spaces in file names, oversized files and unused files inside
assets/. Exit code 1 if any reference is broken.
"""
import re
import sys
from pathlib import Path

SKIP = {".git", "node_modules"}
REF_RE = re.compile(r"""(?:src|href|poster|data-src)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+)["']?\s*\)|@import\s+["']([^"']+)["']""", re.I)
JS_RE = re.compile(r"""["']((?:\.{0,2}/)?[\w./-]+\.(?:png|jpe?g|gif|webp|avif|svg|woff2?|ttf|otf|mp4|webm|mp3|json|js|css))["']""", re.I)
BIG = 1_000_000


def exact_case_exists(base, rel):
    cur = base
    for part in Path(rel).parts:
        if part in (".", ""):
            continue
        if part == "..":
            cur = cur.parent
            continue
        try:
            names = [p.name for p in cur.iterdir()]
        except OSError:
            return False, False
        if part in names:
            cur = cur / part
        else:
            lower = [n for n in names if n.lower() == part.lower()]
            return False, bool(lower)
    return True, True


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1]).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 2
    files = [p for p in root.rglob("*") if p.is_file() and not (set(p.relative_to(root).parts) & SKIP)]
    broken, case, used = [], [], set()
    for p in files:
        ext = p.suffix.lower()
        if ext not in (".html", ".htm", ".css", ".js", ".mjs"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        refs = []
        for m in REF_RE.finditer(text):
            refs.append(next(g for g in m.groups() if g))
        if ext in (".js", ".mjs"):
            refs += [m.group(1) for m in JS_RE.finditer(text)]
        for ref in refs:
            ref = ref.strip()
            if not ref or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", ref, re.I):
                continue
            clean = ref.split("#")[0].split("?")[0]
            if not clean or clean.startswith("/"):
                continue
            ok, ci = exact_case_exists(p.parent, clean)
            if ok:
                used.add((p.parent / clean).resolve())
            elif ci:
                case.append((str(p.relative_to(root)), ref))
            elif ext != ".js":
                broken.append((str(p.relative_to(root)), ref))
    spaces = [str(p.relative_to(root)) for p in files if " " in p.name]
    big = [(str(p.relative_to(root)), p.stat().st_size) for p in files if p.stat().st_size > BIG]
    assets = root / "assets"
    unused = []
    if assets.is_dir():
        unused = [str(p.relative_to(root)) for p in assets.rglob("*") if p.is_file() and p.resolve() not in used and p.name != ".gitkeep"]
    print(f"Asset check for {root}")
    for f, r in broken:
        print(f"[ERROR] {f}: missing '{r}'")
    for f, r in case:
        print(f"[ERROR] {f}: '{r}' differs only by letter case (breaks on GitHub Pages)")
    for s in spaces:
        print(f"[WARN] space in file name: {s}")
    for f, n in big:
        print(f"[WARN] {f}: {n/1e6:.1f} MB")
    for u in unused:
        print(f"[INFO] unused asset: {u}")
    print(f"\nResult: {len(broken)+len(case)} broken, {len(spaces)+len(big)} warning(s), {len(unused)} unused asset(s)")
    return 1 if (broken or case) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
