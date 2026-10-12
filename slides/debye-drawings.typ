// Deck-only drawings for chapter 4 (Debye shielding).
#import "@preview/cetz:0.5.2": canvas, draw
#import "theme.typ": ink, muted, rule, plot-blue, plot-orange

// Rigid charge-separation sphere: all electrons removed from r < R, ions
// (orange +) remain; outside, the plasma stays neutral (+ and - pairs). The
// last electron at the surface is moved out to infinity.
#let sphere-picture() = canvas(length: 13mm, {
  import draw: *
  let R = 2.2
  // neutral surroundings on a jittered grid, skipping the sphere
  for i in range(-4, 5) {
    for j in range(-3, 4) {
      let x = i * 0.95 + calc.rem(j, 2) * 0.45
      let y = j * 0.95
      let on-arrow = x > 0 and y > 0 and calc.abs(x - y) < 0.9
      if calc.sqrt(x * x + y * y) > R + 0.45 and calc.abs(x) < 4.2 and not on-arrow {
        content((x - 0.17, y), text(fill: plot-orange, size: 13pt)[$+$])
        content((x + 0.2, y - 0.05), text(fill: plot-blue, size: 13pt)[$-$])
      }
    }
  }
  circle((0, 0), radius: R, fill: rgb("#B5500014"), stroke: 0.9pt + plot-orange)
  for (x, y) in ((-1.2, 0.9), (0.1, 1.4), (1.1, 0.5), (-0.6, -0.1),
                 (-1.4, -0.8), (-0.3, -1.5), (1.6, -0.2), (-0.3, 0.6)) {
    content((x, y), text(fill: plot-orange, size: 15pt)[$+$])
  }
  line((0, 0), (R * 0.71, -R * 0.71), stroke: 0.7pt + ink)
  content((R * 0.5, -R * 0.24), [$R$])
  // the last electron leaves
  circle((R * 0.71, R * 0.71), radius: 0.13, fill: plot-blue, stroke: none)
  line((R * 0.71 + 0.2, R * 0.71 + 0.2), (R * 0.71 + 1.3, R * 0.71 + 1.3),
    mark: (end: "stealth"), stroke: 1pt + plot-blue, fill: plot-blue)
  content((R * 0.71 + 1.3, R * 0.71 + 1.45), anchor: "south",
    text(fill: plot-blue)[last electron])
})
