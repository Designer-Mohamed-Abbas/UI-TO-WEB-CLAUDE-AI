# Liquid Glass - web approximation guidelines

Sources (read 2026-11-18, via search excerpts, not the full pages):
- https://developer.apple.com/documentation/technologyoverviews/liquid-glass
- https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
- WWDC25 "Meet Liquid Glass": https://developer.apple.com/videos/play/wwdc2025/219/ (only fragments seen; transcript NOT read)

## Official guidance (from what was read)
- Liquid Glass is a dynamic material combining optical properties of glass with fluidity. It forms a functional layer for controls and navigation, and adapts to factors such as element overlap and focus state.
- Standard system components (bars, sheets, popovers, controls) pick it up automatically; custom backgrounds in bars/toolbars can interfere with it.
- Avoid overusing it: if applied to custom controls, do so sparingly.
- People can choose a preferred look and enable reduce-transparency or reduce-motion settings; those remove or modify effects. Test with them.
- Be judicious with color in controls and navigation so content shows through.

## What the browser cannot do
Native Liquid Glass uses real-time lensing/refraction. CSS cannot replicate it. Everything below is a **visual simulation** and the README must say so.

## Implementation recommendations (author's)
```css
.glass {
  background: linear-gradient(135deg, rgb(255 255 255 / .28), rgb(255 255 255 / .08));
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgb(255 255 255 / .35);
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .5), 0 8px 30px rgb(0 0 0 / .12);
}
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass { background: rgb(246 246 248 / .94); }
}
@media (prefers-reduced-transparency: reduce) { .glass { background: Canvas; backdrop-filter: none; } }
@media (prefers-contrast: more) { .glass { background: Canvas; border-color: CanvasText; } }
```
- Use on: navigation bar, floating tab bar, floating buttons, toolbars, sheets' grabber area. Never on body text containers or cards of content.
- Layering: content below, glass above; add a subtle specular highlight (inset top border) and a soft shadow; keep radius generous (pill/capsule for floating bars).
- Interaction: scale 0.97 on press, 150-250 ms ease; disable under `prefers-reduced-motion`.
- Legibility: ensure text on glass reaches 4.5:1 against the worst-case background behind it; add a tint if not.
- Light and dark: define separate token sets for tint, border and shadow.
- Performance: keep blurred area small; avoid stacking multiple blurred layers.
- Match the design: if the supplied design is a flat iOS 15-18 style, do **not** add glass.
