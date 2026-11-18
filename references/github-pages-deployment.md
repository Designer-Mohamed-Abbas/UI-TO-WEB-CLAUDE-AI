# GitHub Pages deployment

Status: general knowledge, **not verified against current GitHub docs in this build.** Verify at https://docs.github.com/en/pages before publishing. Recorded 2026-11-18.

## Requirements
- Static files only; `index.html` at the publish root. No server-side code.
- Relative paths everywhere (`css/style.css`, not `/css/style.css`) so project sites under `/<repo>/` work.
- Case-sensitive file names: `Logo.png` and `logo.png` are different. Avoid spaces.
- Add an empty `.nojekyll` file if any folder starts with `_`.
- Optional `404.html`.

## Steps (branch deploy)
1. Create a repository on GitHub and push the project folder.
2. Repository Settings, Pages: Source "Deploy from a branch", branch `main`, folder `/ (root)`.
3. Wait for the build; the site URL appears at the top of the Pages settings.
4. Re-push to update.

## Local run
```
cd <project>
python3 -m http.server 8000
# open http://localhost:8000
```
ES modules and `fetch` need http, not `file://`.
