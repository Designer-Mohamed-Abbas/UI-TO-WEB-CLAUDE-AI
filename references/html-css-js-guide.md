# HTML / CSS / JavaScript implementation guide

Status: implementation recommendations written by the skill author (not copied from any site). Verify browser-support claims against MDN / caniuse when compatibility matters.

## Contents
1. Markup  2. CSS architecture  3. Layout  4. JavaScript  5. Performance  6. Fidelity checklist

## 1. Markup
- One `<h1>` per page. Use `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `button`, `a`, `form`, `label`.
- `<button>` for actions, `<a href>` for navigation. Never a clickable `div`.
- Every `img` has `alt` (empty `alt=""` for decorative). Give `width`/`height` to avoid layout shift.
- `<html lang="..">` and `dir="rtl"` for Arabic designs. Use logical properties (`margin-inline-start`, `padding-inline`) so RTL works.
- `<meta name="viewport" content="width=device-width, initial-scale=1">`; add `viewport-fit=cover` only for edge-to-edge mobile designs that use safe-area insets.

## 2. CSS architecture
- Tokens first, in `:root`: colors, font families, type scale, spacing scale, radii, shadows, z-index layers, durations.
- Component classes (BEM-like: `.card`, `.card__title`, `.card--active`). Avoid ids for styling and avoid `!important`.
- File split only when size justifies it: `style.css` (tokens, base, layout), `components.css`, `responsive.css`, `animations.css`.
- Mark a token as measured / inferred / estimated in a comment when the source gives no exact value.
- `box-sizing: border-box` globally.
- Fonts: use supplied font files with `@font-face` and `font-display: swap`. If a font is missing, use a close system stack and document it. Do not swap silently.

## 3. Layout
- Flexbox for one-dimensional rows/columns, Grid for two-dimensional structure.
- Preserve proportions: `aspect-ratio` for images/cards, `object-fit` to match the original crop.
- Keep the design's fixed values at the reference width, then make containers fluid (`max-width`, `clamp()`, `min()`) instead of rewriting the design.
- Safe areas: `padding-top: env(safe-area-inset-top, 0px)` and the same for the other edges.

## 4. JavaScript
- ES modules (`<script type="module">`) work on GitHub Pages but need http(s), not `file://`. If the project must open from `file://`, use classic scripts.
- Event delegation for lists; `data-*` attributes to wire behavior; no inline handlers.
- Render by toggling classes/attributes (`aria-expanded`, `hidden`, `data-state`).
- Persist only harmless UI state (theme, last tab) in `localStorage`, wrapped in try/catch.
- Forms: native validation attributes first, then the Constraint Validation API. Never pretend to submit to a server that does not exist; state the limitation.
- Respect `prefers-reduced-motion`.

## 5. Performance (without visual change)
- Serve images at the size the design needs; keep originals, add compressed copies only if the user accepts it.
- `loading="lazy"` below the fold, `decoding="async"`.
- Animate `transform`/`opacity`; limit the area of `backdrop-filter` (expensive).

## 6. Fidelity checklist
Colors match samples - font sizes/weights match - spacing consistent - radii/shadows match - image crops match - icons are the supplied ones - every screen reproduced - all text preserved.
