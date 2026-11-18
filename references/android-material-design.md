# Android / Material Design - working notes

Sources: https://m3.material.io/ , https://developer.android.com/design , https://developer.android.com/design/ui/mobile/guides/layout-and-content/adapt-layout
Research date: 2026-11-18.

## What was and was not read
- **Read (search excerpts):** Android "Tier 2 - Adaptive optimized" quality guidelines (https://developer.android.com/docs/quality-guidelines/adaptive-app-quality/tier-2) and a third-party summary of M3 layout basics (SAP Fiori Android design system, https://www.sap.com/design-system/fiori-design-android/v25-4/foundations/adaptive-layout/layout-basics, secondary source).
- **NOT read:** m3.material.io component pages, M3 Expressive pages, developer.android.com/design pages. Verify before presenting as official.

## Official guidance (from what was read)
- Touch targets are at least 48dp (Android quality guidelines).
- Layouts should be responsive/adaptive, driven by window size classes.
- Navigation rails replace navigation bars on large screens; navigation drawers become expanded rails; buttons are not full width on large screens; text fields do not stretch to full width on large screens.
- Grids scale their number of columns with window size.
- Keyboard navigation (Tab, arrows) should work and focus must be visible.

## From the secondary source (verify in m3.material.io)
- Typical screen margins 16dp or 24dp depending on window size; 48x48dp targets with about 8dp between targets.

## Implementation recommendations (author's)
- Treat 1dp as 1 CSS px for a 1:1 look in a phone frame. Typical frame: about 412x915 CSS px (estimated; verify).
- Navigation: bottom navigation bar (3-5 destinations) on compact widths; rail from medium/expanded.
- Components: use M3 shapes (rounded corners, pill buttons), tonal surfaces, state layers (hover/focus/pressed as translucent overlays), ripple optional.
- Typography: Roboto / Google Sans family if supplied; otherwise `system-ui` and document it.
- Do not apply Apple conventions (large titles, SF fonts, edge-swipe visuals) to Android designs, or the reverse.
- Device simulation: punch-hole camera, status bar, gesture navigation pill. It is a web simulation, not Android rendering.
