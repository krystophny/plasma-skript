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

// Frozen frame of the coupling-regions animation (same electrons, colour map,
// colour limits and scale; scripts/export-coupling-still.py): net charge
// density on z = 0, red rho > 0 and blue rho < 0, smoothed at lambda_D/2, and
// the electrons of the slab |z| < a/2. Lengths in units of a.
#let coupling-data = json("/slides/coupling-regions.json")
#let coupling-still(index, width) = {
  let (x-min, x-max, y-min, y-max) = coupling-data.window
  let u = width / (x-max - x-min)
  let panel = coupling-data.panels.at(index)
  let r = 0.1 * u
  block(width: width, height: (y-max - y-min) * u, clip: true, stroke: 0.6pt + rule)[
    #place(image("/slides/coupling-regions-" + str(index) + ".png", width: width,
      height: (y-max - y-min) * u))
    #for (x, y, a) in panel.points {
      place(dx: (x - x-min) * u - r, dy: (y-max - y) * u - r,
        circle(radius: r, fill: ink.transparentize((1 - a) * 100%), stroke: none))
    }
  ]
}

// Heading of a coupling panel: T_e, Gamma_e and lambda_D in units of a.
#let coupling-heading(index) = {
  let panel = coupling-data.panels.at(index)
  let t = if panel.temperature == "T_0" { $T_0$ } else { $9 T_0$ }
  let length = if panel.lambda == 1 { $a$ } else { $#str(int(panel.lambda)) a$ }
  let g = if index == 0 { "0.08" } else { "0.009" }
  $T_e = #t, quad Gamma_e = #g, quad lambda_D = #length$
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
