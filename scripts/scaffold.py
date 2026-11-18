#!/usr/bin/env python3
"""
Project: ui-to-web skill scaffolder
Developed by: Mohamed Ahmed Abbas
Role: Front-End Development

Copyright (c) 2026 Mohamed Ahmed Abbas.
All rights reserved.

Usage:
  scaffold.py new <project-name> --out <dir> [--title "Title"] [--year 2026] [--preview] [--author "Name"]
  scaffold.py header {html|css|js} --project "Name" [--year 2026]

Creates a new project from templates/project-template, fills placeholders and
never overwrites an existing directory.
"""
import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_DIR / "templates"
DEFAULT_AUTHOR = "Mohamed Ahmed Abbas"
TEXT_EXT = {".html", ".css", ".js", ".md", ".txt", ".json", ".svg"}


def fill(text, values):
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", val)
    return text


def slugify(name):
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip()).strip("-").lower()
    return slug or "project"


def copy_tree(src, dst, values):
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() in TEXT_EXT or path.name == "LICENSE":
            target.write_text(fill(path.read_text(encoding="utf-8"), values), encoding="utf-8")
        else:
            shutil.copy2(path, target)


def cmd_new(args):
    year = str(args.year or datetime.date.today().year)
    slug = slugify(args.name)
    out = Path(args.out).expanduser().resolve()
    dest = out / slug
    if dest.exists():
        print(f"ERROR: {dest} already exists. Refusing to overwrite. Choose another name.", file=sys.stderr)
        return 2
    values = {
        "PROJECT_NAME": args.name,
        "TITLE": args.title or args.name,
        "YEAR": year,
        "AUTHOR": args.author,
        "DATE": datetime.date.today().isoformat(),
    }
    out.mkdir(parents=True, exist_ok=True)
    copy_tree(TEMPLATES / "project-template", dest, values)
    (dest / "assets").mkdir(exist_ok=True)  # add images/ icons/ fonts/ only as needed
    # report templates -> docs/
    docs = dest / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "ui-ux-audit.md").write_text(fill((TEMPLATES / "audit-report-template.md").read_text(encoding="utf-8"), values), encoding="utf-8")
    (docs / "design-analysis.md").write_text(fill((TEMPLATES / "design-analysis-template.md").read_text(encoding="utf-8"), values), encoding="utf-8")
    if args.preview:
        copy_tree(TEMPLATES / "preview-switcher", dest / "preview", values)
    print(f"Created {dest}")
    for p in sorted(dest.rglob("*")):
        if p.is_file():
            print("  " + str(p.relative_to(dest)))
    return 0


def cmd_header(args):
    ext = args.kind
    tpl = TEMPLATES / "copyright-headers" / f"header.{ext}.txt"
    values = {"PROJECT_NAME": args.project, "YEAR": str(args.year or datetime.date.today().year)}
    sys.stdout.write(fill(tpl.read_text(encoding="utf-8"), values))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("name")
    n.add_argument("--out", required=True)
    n.add_argument("--title")
    n.add_argument("--year", type=int)
    n.add_argument("--author", default=DEFAULT_AUTHOR)
    n.add_argument("--preview", action="store_true", help="include preview switcher (Responsive / iPhone / Android)")
    n.set_defaults(func=cmd_new)
    h = sub.add_parser("header")
    h.add_argument("kind", choices=["html", "css", "js"])
    h.add_argument("--project", required=True)
    h.add_argument("--year", type=int)
    h.set_defaults(func=cmd_header)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
