// Deck-only drawings for chapter 2 (temperature, entropy, thermal ionization).
// Schematic pictures, drawn at slide scale with CeTZ; the quantitative plots
// remain the script's derived figures.
#import "@preview/cetz:0.5.2": canvas, draw
#import "theme.typ": ink, muted, rule, plot-blue, plot-orange

#let dot-fill = plot-blue
#let ion-fill = plot-orange

// Deterministic pseudo-random points in a w × h box (units of the canvas).
#let scatter(n, w, h, seed) = {
  let s = seed
  let pts = ()
  for _ in range(n) {
    s = calc.rem(s * 1103515245 + 12345, 2147483648)
    let x = 0.15 * w + 0.7 * w * s / 2147483648
    s = calc.rem(s * 1103515245 + 12345, 2147483648)
    let y = 0.15 * h + 0.7 * h * s / 2147483648
    pts.push((x, y))
  }
  pts
}

// Two boxes that exchange energy through a shared wall.
#let exchange-boxes() = canvas(length: 11.5mm, {
  import draw: *
  let w = 4.4
  let h = 3.4
  rect((0, 0), (w, h), stroke: 0.9pt + ink)
  rect((w + 1.6, 0), (2 * w + 1.6, h), stroke: 0.9pt + ink)
  for p in scatter(9, w, h, 7) { circle(p, radius: 0.11, fill: dot-fill, stroke: none) }
  for p in scatter(14, w, h, 29) {
    circle((p.at(0) + w + 1.6, p.at(1)), radius: 0.11, fill: dot-fill, stroke: none)
  }
  content((w / 2, h + 0.55), [$A$])
  content((w + 1.6 + w / 2, h + 0.55), [$B$])
  line((w + 0.2, h / 2), (w + 1.4, h / 2), mark: (start: "stealth", end: "stealth"),
    stroke: 1.1pt + plot-orange, fill: plot-orange)
  content((w + 0.8, h / 2 - 0.6), text(fill: plot-orange)[$dif E$])
  content((w / 2, -0.6), text(fill: muted)[$E_A, S_A$])
  content((w + 1.6 + w / 2, -0.6), text(fill: muted)[$E_B, S_B$])
})

// S_A(E_A), S_B(E - E_A) and their sum; the sum peaks where the slopes match.
#let entropy-maximum() = canvas(length: 10mm, {
  import draw: *
  let W = 9.0
  let H = 5.0
  let E = 10.0
  let sa(x) = 3.0 * calc.ln(x)
  let sb(x) = 5.0 * calc.ln(E - x)
  let n = 60
  let xs = range(n + 1).map(i => 0.6 + (E - 1.2) * i / n)
  let ymin = 0.0
  let ymax = 15.0
  let px(x) = W * (x - 0.6) / (E - 1.2)
  let py(y) = H * (y - ymin) / (ymax - ymin)
  line((0, 0), (W + 0.4, 0), mark: (end: "stealth"), stroke: 0.7pt + ink, fill: ink)
  line((0, 0), (0, H + 0.4), mark: (end: "stealth"), stroke: 0.7pt + ink, fill: ink)
  content((W + 0.4, -0.5), [$E_A$])
  content((-0.5, H + 0.4), [$S$])
  let curve(f, style) = line(..xs.map(x => (px(x), py(calc.max(ymin, f(x))))), stroke: style)
  curve(sa, 1.2pt + plot-blue)
  curve(sb, (paint: plot-blue, thickness: 1.2pt, dash: "dashed"))
  curve(x => sa(x) + sb(x), 1.8pt + plot-orange)
  // maximum of sa + sb at 3/x = 5/(E-x), x = 3E/8
  let xm = 3.0 * E / 8.0
  line((px(xm), 0), (px(xm), H), stroke: (paint: muted, thickness: 0.6pt, dash: "dotted"))
  content((px(xm), -0.55), text(fill: muted)[$T_A = T_B$])
  content((px(8.4), py(sa(8.4)) - 0.2), anchor: "north-west", text(fill: plot-blue)[$S_A$])
  content((px(1.0), py(sb(1.0)) + 0.15), anchor: "south-west", text(fill: plot-blue)[$S_B$])
  content((px(6.6), py(sa(6.6) + sb(6.6)) + 0.2), anchor: "south-west",
    text(fill: plot-orange)[$S_A + S_B$])
})

// A small system inside a large reservoir.
#let reservoir() = canvas(length: 12mm, {
  import draw: *
  rect((0, 0), (9, 6), radius: 0.5, stroke: 0.9pt + ink)
  for p in scatter(46, 9, 6, 3) {
    if not (p.at(0) > 2.4 and p.at(0) < 4.8 and p.at(1) > 1.8 and p.at(1) < 4.2) {
      circle(p, radius: 0.09, fill: rule, stroke: none)
    }
  }
  rect((2.6, 2.0), (4.6, 4.0), stroke: 1.1pt + plot-orange)
  content((3.6, 3.0), text(fill: plot-orange)[$A$])
  content((3.6, 1.45), text(fill: plot-orange)[$E_a$])
  content((4.5, -0.55), [reservoir #h(0.6em) #text(fill: muted)[$E_"tot" - E_a$]])
})

// Atom (bound electron) → ion + free electron, the reservoir pays chi.
#let ionization-picture() = canvas(length: 13mm, {
  import draw: *
  let nucleus(c) = {
    circle(c, radius: 0.42, fill: ion-fill, stroke: none)
    content(c, text(fill: white, size: 15pt)[$+$])
  }
  let electron(c) = circle(c, radius: 0.18, fill: dot-fill, stroke: none)
  nucleus((0, 0))
  circle((0, 0), radius: 1.25, stroke: (paint: muted, thickness: 0.6pt, dash: "dashed"))
  electron((0.88, 0.88))
  content((0, -1.95), [neutral $n$])
  line((2.2, 0), (4.6, 0), mark: (end: "stealth"), stroke: 1.1pt + ink, fill: ink)
  content((3.4, 0.55), [$chi$])
  nucleus((6.1, 0))
  content((6.1, -1.95), [ion $i$])
  electron((8.6, 0.6))
  line((8.75, 0.68), (9.9, 1.25), mark: (end: "stealth"), stroke: 0.9pt + dot-fill, fill: dot-fill)
  content((8.9, -1.95), [free electron $e$])
})
