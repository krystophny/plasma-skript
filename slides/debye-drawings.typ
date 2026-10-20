// Deck-only drawings for chapter 4 (Debye shielding).
#import "@preview/cetz:0.5.2": canvas, draw
#import "theme.typ": ink, muted, rule, plot-blue, plot-orange

// Rigid charge-separation sphere: all electrons removed from r < r_0, ions
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
  content((R * 0.5, -R * 0.24), [$r_0$])
  // the last electron leaves
  circle((R * 0.71, R * 0.71), radius: 0.13, fill: plot-blue, stroke: none)
  line((R * 0.71 + 0.2, R * 0.71 + 0.2), (R * 0.71 + 1.3, R * 0.71 + 1.3),
    mark: (end: "stealth"), stroke: 1pt + plot-blue, fill: plot-blue)
  content((R * 0.71 + 1.3, R * 0.71 + 1.45), anchor: "south",
    text(fill: plot-blue)[last electron])
})

// Launch frame of the coupling-test-particle animation (same electrons, launch
// point and Debye radii; scripts/export-coupling-still.py): the drawn frozen
// electrons of the slab 0 < z < a, blue within lambda_D of the test electron
// and grey outside, on the faint +e n_0 background. Lengths in units of a.
#let coupling-data = json("/slides/coupling-still.json")
#let coupling-still(index, width) = {
  let d = coupling-data
  let (x-min, x-max, y-min, y-max) = d.window
  let u = width / (x-max - x-min)
  let panel = d.panels.at(index)
  let lam = panel.lambda
  let pos(x, y) = ((x - x-min) * u, (y-max - y) * u)
  let dot(x, y, r, fill, stroke: none) = {
    let (px, py) = pos(x, y)
    place(dx: px - r, dy: py - r, circle(radius: r, fill: fill, stroke: stroke))
  }
  let (cx, cy) = d.centre
  let theta = panel.angle * 1deg
  let (ux, uy) = (calc.cos(theta), calc.sin(theta))
  let reach = lam + 0.36 * (calc.abs(ux) + calc.abs(uy)) + 0.08
  let (lx, ly) = pos(cx + reach * ux, cy + reach * uy)
  let (px, py) = pos(cx, cy)
  block(width: width, height: (y-max - y-min) * u, clip: true,
    fill: plot-orange.transparentize(92%), stroke: 0.6pt + rgb("#9AA5B1"))[
    #for (p, hit) in d.points.zip(panel.inside) {
      dot(..p, 0.1 * u, if hit { plot-blue } else { rgb("#C8CED6") })
    }
    #place(dx: px - lam * u, dy: py - lam * u, circle(radius: lam * u, stroke: 0.9pt + ink))
    #place(dx: px, dy: py, line(end: (lam * u * ux, -lam * u * uy), stroke: 0.6pt + ink))
    #place(dx: (cx - 1.35 - x-min) * u, dy: py, line(length: 1.1 * u - 1.5mm, stroke: 0.7pt + muted))
    #place(dx: px - 0.25 * u - 1.6mm, dy: py - 1mm, polygon(fill: muted, stroke: none,
      (0mm, 0mm), (1.6mm, 1mm), (0mm, 2mm)))
    #dot(cx, cy, 0.165 * u, plot-blue, stroke: 0.6pt + ink)
    #place(dx: lx - 5mm, dy: ly - 5mm, box(width: 10mm, height: 10mm,
      align(center + horizon, $lambda_D$)))
  ]
}

// Heading of a coupling panel: Gamma_e, lambda_D in units of a, regime.
#let coupling-heading(index, name) = {
  let panel = coupling-data.panels.at(index)
  let n = calc.round(panel.lambda)
  let length = if n == 1 { $a$ } else { $#n a$ }
  [$Gamma_e = #str(panel.gamma), #h(0.3em) lambda_D approx #length$ #h(5mm) #text(fill: muted, name)]
}

// Scale bar of length a at the coupling-still scale.
#let coupling-bar(width) = {
  let (x-min, x-max, ..) = coupling-data.window
  let u = width / (x-max - x-min)
  let tick(x) = place(dx: x, dy: 0mm, line(start: (0mm, 0mm), end: (0mm, 2.4mm), stroke: 0.6pt + ink))
  box(width: u, height: 2.4mm, {
    place(dy: 1.2mm, line(length: u, stroke: 1.2pt + ink))
    tick(0mm)
    tick(u)
  })
  h(3mm)
  $a$
}
