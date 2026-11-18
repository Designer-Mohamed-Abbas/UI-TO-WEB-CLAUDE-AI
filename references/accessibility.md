# Accessibility checklist

Status: implementation recommendations based on WCAG 2.x practice and the platform notes below. Touch-target figure for Android (48dp) was read at https://developer.android.com/docs/quality-guidelines/adaptive-app-quality/tier-2 on 2026-11-18. Apple guidance on reduced transparency/motion read at https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass on 2026-11-18. WCAG numbers below are from general knowledge; verify at https://www.w3.org/TR/WCAG22/ if needed.

- Contrast: text 4.5:1 (large text 3:1), UI components and focus indicators 3:1.
- Touch targets: at least 48x48 dp on Android-style designs; about 44x44 pt is the common iOS guideline (verify in HIG). Keep spacing between targets.
- Focus: visible `:focus-visible` outline on every interactive element; logical tab order; never `outline:none` without a replacement.
- Keyboard: all actions reachable; Esc closes modals/menus; arrow keys in tabs/menus; focus trapped in modals and returned on close.
- Semantics first, ARIA second. Use `aria-expanded`, `aria-controls`, `aria-current`, `role="tablist"` only when the native element cannot express it.
- Forms: `label` for every input, errors linked with `aria-describedby`, not by color alone.
- Motion: honor `prefers-reduced-motion`.
- Transparency: honor `prefers-reduced-transparency` (where supported) and `prefers-contrast`; give glass surfaces a solid fallback.
- Images: meaningful `alt`; decorative `alt=""`.
- Language/direction: `lang`, `dir`.
- The audit may report accessibility problems in the *design* (e.g. low contrast). Implement the design faithfully and report the issue; do not silently fix it.
