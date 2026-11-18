# Apple Human Interface Guidelines - working notes

Primary source: https://developer.apple.com/design/human-interface-guidelines/
Research date: 2026-11-18.

## What was and was not read
- **Read (excerpts via search):** "Liquid Glass" and "Adopting Liquid Glass" technology overviews (see `liquid-glass-guidelines.md`).
- **NOT read in this build:** the HIG pages themselves (layout, navigation, typography, materials, color, accessibility). Everything under "Implementation recommendations" is general knowledge and must be verified against the HIG before being presented as Apple guidance.

## Official guidance (from pages read)
- Apple describes Liquid Glass as a material that forms a distinct functional layer for controls and navigation, adapting to content overlap and focus to bring attention to the underlying content.
- Design principles listed on Apple's overview: define a layout and navigation structure that puts the most important content in focus; be judicious with color in controls and navigation so they stay legible and let content show through; make interface elements fit software and hardware design across devices.

## Implementation recommendations (author's, verify)
- Typography: Apple platforms use San Francisco. Do not ship Apple's font on a public site unless licensing allows it; use `-apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif` so Apple devices render the system font, and document the fallback elsewhere.
- Touch targets: about 44x44 pt minimum (verify in HIG "Accessibility"/"Layout").
- Safe areas: use `env(safe-area-inset-*)`; top about 47-59 pt and bottom 34 pt are typical on notch/Dynamic Island iPhones (estimated; verify per device).
- Navigation patterns: tab bar (bottom, 3-5 items), navigation bar with large/inline title, sheets, swipe-back. Reproduce what the design shows; do not add patterns.
- Dark mode: support `prefers-color-scheme` only if the design provides dark variants.
- Never claim the web output is native iOS rendering.
