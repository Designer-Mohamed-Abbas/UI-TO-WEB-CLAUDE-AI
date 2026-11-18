# Responsive design

Status: implementation recommendations. Android window-size-class guidance below comes from Android's adaptive quality guidelines (https://developer.android.com/docs/quality-guidelines/adaptive-app-quality/tier-2), read 2026-11-18.

## Principles
- Mobile-first CSS (`min-width` queries), unless the design is desktop-first and fidelity is easier that way.
- Breakpoints come from content: widen the viewport until the layout looks wrong, add a breakpoint there. Do not use a fixed list "because devices".
- Typical window-size-class boundaries used by Android (compact < 600dp, medium 600-839dp, expanded >= 840dp) are a useful *starting point* for app-like designs; confirm against the actual content.
- Preserve visual hierarchy: same order of importance, same palette and components; change columns, nav pattern and spacing only.

## Techniques
- Fluid type/spacing: `clamp(min, preferred, max)`.
- Grids: `repeat(auto-fit, minmax(min(100%, 16rem), 1fr))`.
- Containers: `max-width` + `margin-inline: auto` + `padding-inline`.
- Images: `max-width:100%; height:auto`; `srcset`/`sizes` when multiple files exist; `aspect-ratio` to hold crop.
- Navigation: bottom bar or hamburger on compact; rail or top nav on larger widths (Android guidance: navigation rails replace navigation bars on large screens; text fields and buttons should not stretch full width on large screens).
- Tables: wrap in `overflow-x:auto` instead of shrinking text.
- Test widths: 360, 390, 430, 600, 768, 820, 1024, 1280, 1440, 1920. Check landscape phone.
- Mobile app designs: Mode A (responsive site) adapts the app to wide screens; Mode B (device frame) shows the unmodified mobile layout. They share one codebase.
