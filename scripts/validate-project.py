#!/usr/bin/env python3
"""
Project: ui-to-web project validator
Developed by: Mohamed Ahmed Abbas
Role: Front-End Development

Copyright (c) 2026 Mohamed Ahmed Abbas.
All rights reserved.

Usage: validate-project.py <project-dir> [--json]

Static checks only (no browser): HTML structure, CSS brace balance, JS syntax
(via `node --check` when node exists, otherwise a bracket-balance heuristic),
local reference targets, attribution headers, framework use, basic a11y markers.
Exit code 1 when errors are found. Warnings do not fail.
"""
import json
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
SKIP_DIRS = {".git", "node_modules"}
AUTHOR = "Mohamed Ahmed Abbas"
FRAMEWORK_PATTERNS = [
    (r"react(\.production|-dom)?(\.min)?\.js|from\s+['\"]react['\"]", "React"),
    (r"vue(\.global|\.runtime)?(\.min)?\.js|from\s+['\"]vue['\"]", "Vue"),
    (r"angular(\.min)?\.js|@angular/", "Angular"),
    (r"bootstrap(\.min)?\.(css|js)|bootstrap@", "Bootstrap"),
    (r"cdn\.tailwindcss\.com|tailwindcss", "Tailwind"),
    (r"jquery(\.min)?\.js", "jQuery"),
]


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, where, msg):
        self.items.append({"level": level, "file": where, "message": msg})

    def count(self, level):
        return sum(1 for i in self.items if i["level"] == level)


class Checker(HTMLParser):
    def __init__(self, rel, rep):
        super().__init__(convert_charrefs=True)
        self.rel, self.rep = rel, rep
        self.stack = []
        self.refs = []
        self.has_doctype = False
        self.has_lang = False
        self.has_viewport = False
        self.has_title = False
        self.h1 = 0
        self.in_title = False

    def handle_decl(self, decl):
        if decl.lower().startswith("doctype"):
            self.has_doctype = True

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag == "html" and a.get("lang"):
            self.has_lang = True
        if tag == "meta" and (a.get("name") or "").lower() == "viewport":
            self.has_viewport = True
        if tag == "title":
            self.has_title, self.in_title = True, True
        if tag == "h1":
            self.h1 += 1
        if tag == "img" and "alt" not in a:
            self.rep.add("warning", self.rel, f"line {line}: <img> without alt")
        if tag == "a" and a.get("target") == "_blank" and "noopener" not in (a.get("rel") or ""):
            self.rep.add("warning", self.rel, f"line {line}: target=_blank without rel=noopener")
        if tag in ("button",) and a.get("type") is None:
            pass
        for attr in ("href", "src", "poster", "data-src"):
            if a.get(attr):
                self.refs.append((attr, a[attr], line))
        if a.get("srcset"):
            for part in a["srcset"].split(","):
                u = part.strip().split(" ")[0]
                if u:
                    self.refs.append(("srcset", u, line))
        if a.get("id"):
            self.ids = getattr(self, "ids", set()) | {a["id"]}
        if tag not in VOID:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag, attrs):
        # self-closing syntax: process attrs, do not push
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        line = self.getpos()[0]
        if tag == "title":
            self.in_title = False
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for t, l in self.stack[i + 1:]:
                    if t not in ("p", "li", "dd", "dt", "tr", "td", "th", "option", "thead", "tbody", "tfoot"):
                        self.rep.add("error", self.rel, f"line {l}: <{t}> was not closed before </{tag}> at line {line}")
                del self.stack[i:]
                return
        self.rep.add("error", self.rel, f"line {line}: stray </{tag}>")


def is_external(u):
    return bool(re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", u, re.I)) or u.startswith("#")


def check_html(path, root, rep, all_ids):
    rel = str(path.relative_to(root))
    text = path.read_text(encoding="utf-8", errors="replace")
    c = Checker(rel, rep)
    c.feed(text)
    c.close()
    for t, l in c.stack:
        if t not in ("html", "body", "head", "p", "li"):
            rep.add("error", rel, f"line {l}: <{t}> never closed")
    if not c.has_doctype:
        rep.add("error", rel, "missing <!DOCTYPE html>")
    if not c.has_lang:
        rep.add("warning", rel, "<html> has no lang attribute")
    if not c.has_viewport:
        rep.add("warning", rel, "missing viewport meta tag")
    if not c.has_title:
        rep.add("warning", rel, "missing <title>")
    if c.h1 > 1:
        rep.add("warning", rel, f"{c.h1} <h1> elements")
    if AUTHOR not in text:
        rep.add("warning", rel, "author attribution header missing")
    for attr, ref, line in c.refs:
        ref = ref.strip()
        if not ref or is_external(ref):
            if ref.startswith("#") and len(ref) > 1:
                all_ids.append((rel, ref[1:], line, getattr(c, "ids", set())))
            continue
        clean = ref.split("#")[0].split("?")[0]
        if not clean:
            continue
        if clean.startswith("/"):
            rep.add("warning", rel, f"line {line}: root-absolute path '{ref}' breaks GitHub Pages project sites; use a relative path")
            continue
        if not (path.parent / clean).exists():
            rep.add("error", rel, f"line {line}: {attr}='{ref}' not found")
    return text


def check_css(path, root, rep):
    rel = str(path.relative_to(root))
    text = path.read_text(encoding="utf-8", errors="replace")
    if AUTHOR not in text:
        rep.add("warning", rel, "author attribution header missing")
    stripped = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    if "/*" in re.sub(r"/\*.*?\*/", "", text, flags=re.S):
        rep.add("error", rel, "unclosed comment")
    stripped = re.sub(r"(['\"]).*?\1", '""', stripped)
    if stripped.count("{") != stripped.count("}"):
        rep.add("error", rel, f"unbalanced braces: {stripped.count('{')} '{{' vs {stripped.count('}')} '}}'")
    if stripped.count("(") != stripped.count(")"):
        rep.add("error", rel, "unbalanced parentheses")
    for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", text):
        u = m.group(1).strip()
        if u.startswith("data:") or is_external(u):
            continue
        clean = u.split("#")[0].split("?")[0]
        if clean.startswith("/"):
            rep.add("warning", rel, f"root-absolute url('{u}')")
        elif clean and not (path.parent / clean).exists():
            rep.add("error", rel, f"url('{u}') not found")
    for m in re.finditer(r"@import\s+(?:url\()?['\"]?([^'\");]+)", text):
        u = m.group(1)
        if not is_external(u) and not (path.parent / u).exists():
            rep.add("error", rel, f"@import '{u}' not found")
    return text


def check_js(path, root, rep):
    rel = str(path.relative_to(root))
    text = path.read_text(encoding="utf-8", errors="replace")
    if AUTHOR not in text:
        rep.add("warning", rel, "author attribution header missing")
    node = shutil.which("node")
    if node:
        r = subprocess.run([node, "--check", str(path)], capture_output=True, text=True)
        if r.returncode != 0:
            lines = [l for l in r.stderr.strip().splitlines() if l.strip()]
            rep.add("error", rel, "syntax error: " + " | ".join(lines[:4]))
        return text
    # heuristic fallback: strip comments/strings/regex-ish and compare brackets
    s = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
    s = re.sub(r"'(?:\\.|[^'\\\n])*'|\"(?:\\.|[^\"\\\n])*\"|`(?:\\.|[^`\\])*`", "''", s)
    for o, c in ("{}", "()", "[]"):
        if s.count(o) != s.count(c):
            rep.add("error", rel, f"unbalanced '{o}{c}' (heuristic check; node not available)")
    rep.add("info", rel, "node not found: syntax checked by bracket heuristic only")
    return text


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    root = Path(args[0]).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 2
    rep = Report()
    files = [p for p in root.rglob("*") if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS)]
    if not (root / "index.html").exists():
        rep.add("error", "index.html", "missing index.html at project root")
    if not (root / "LICENSE").exists():
        rep.add("warning", "LICENSE", "no LICENSE file")
    if not (root / "README.md").exists():
        rep.add("warning", "README.md", "no README.md")
    all_ids, blobs = [], []
    for p in files:
        ext = p.suffix.lower()
        if ext in (".html", ".htm"):
            blobs.append(check_html(p, root, rep, all_ids))
        elif ext == ".css":
            blobs.append(check_css(p, root, rep))
        elif ext == ".js" or ext == ".mjs":
            blobs.append(check_js(p, root, rep))
    for rel, ref, line, ids in all_ids:
        if ref and ref not in ids and ref != "top":
            rep.add("warning", rel, f"line {line}: anchor #{ref} has no matching id on the same page")
    joined = "\n".join(blobs)
    for pat, name in FRAMEWORK_PATTERNS:
        if re.search(pat, joined, re.I):
            rep.add("warning", "(project)", f"{name} detected; default stack is vanilla HTML/CSS/JS unless the user requested it")
    if as_json:
        print(json.dumps({"errors": rep.count("error"), "warnings": rep.count("warning"), "items": rep.items}, indent=2))
    else:
        print(f"Validated {root} ({len(files)} files)")
        for lvl in ("error", "warning", "info"):
            for i in rep.items:
                if i["level"] == lvl:
                    print(f"[{lvl.upper()}] {i['file']}: {i['message']}")
        print(f"\nResult: {rep.count('error')} error(s), {rep.count('warning')} warning(s)")
        print("Static checks only. No browser rendering, console or visual comparison was performed.")
    return 1 if rep.count("error") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
