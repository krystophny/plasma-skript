// Deck-only drawings for chapter 4 (plasma oscillations).
#import "@preview/cetz:0.5.2": canvas, draw
#import "theme.typ": ink, muted, rule, plot-blue, plot-orange

// Fixed ion slab (orange) and the electron slab (blue) displaced by xi:
// uncovered ions on the left (+sigma), excess electrons on the right
// (-sigma), the field E between them, and the restoring force on electrons.
#let slab-picture() = canvas(length: 12mm, {
  import draw: *
  let L = 14.0
  let H = 4.0
  let d = 1.3
  // ions: fixed background
  rect((0, 0), (L, H), fill: rgb("#B5500014"), stroke: 0.8pt + plot-orange)
  // electrons: displaced to the right
  rect((d, 0.35), (L + d, H - 0.35), fill: rgb("#0072B21C"), stroke: (paint: plot-blue, thickness: 0.9pt, dash: "dashed"))
  for j in range(4) {
    content((0.62, 0.65 + j * 0.9), text(fill: plot-orange, size: 20pt)[$+$])
    content((L + d * 0.55, 0.65 + j * 0.9), text(fill: plot-blue, size: 20pt)[$-$])
  }
  content((L / 2 + d / 2, H / 2), text(fill: muted)[neutral overlap])
  // displacement
  line((0, -0.6), (d, -0.6), mark: (start: "|", end: "stealth"), stroke: 0.8pt + ink, fill: ink)
  content((d / 2, -1.15), [$xi$])
  // field and force
  line((3.6, H + 0.75), (8.2, H + 0.75), mark: (end: "stealth"), stroke: 1.2pt + ink, fill: ink)
  content((5.9, H + 1.3), [$E = (e n_0 xi)/epsilon_0$])
  line((12.0, H + 0.75), (9.6, H + 0.75), mark: (end: "stealth"), stroke: 1.2pt + plot-blue, fill: plot-blue)
  content((10.8, H + 1.3), text(fill: plot-blue)[$F_e = -e E$])
  content((0, H + 0.3), anchor: "south-west", text(fill: plot-orange)[$+sigma$])
  content((L + d, H + 0.3), anchor: "south-east", text(fill: plot-blue)[$-sigma$])
  line((0, -1.9), (L, -1.9), mark: (start: "|", end: "|"), stroke: 0.6pt + muted)
  content((L / 2, -2.35), text(fill: muted)[$L$])
})
