// Deck-only drawings for chapter 1 (introduction).
#import "@preview/cetz:0.5.2": canvas, draw
#import "@preview/fletcher:0.5.8" as fletcher: node, edge
#import "theme.typ": ink, muted, rule, plot-blue, plot-orange, body-size

// Particles as points in the (x, v) plane; one cell of size Δx Δv is
// highlighted and its points counted: f Δx Δv = number of particles.
#let phase-cells() = canvas(length: 13.5mm, {
  import draw: *
  let W = 10.0
  let H = 6.4
  // Maxwellian-like velocity spread with a density bump in x.
  let s = 11
  let pts = ()
  for _ in range(260) {
    s = calc.rem(s * 1103515245 + 12345, 2147483648)
    let u1 = (s + 1) / 2147483649
    s = calc.rem(s * 1103515245 + 12345, 2147483648)
    let u2 = s / 2147483648
    s = calc.rem(s * 1103515245 + 12345, 2147483648)
    let x = W * s / 2147483648
    let v = H / 2 + 1.05 * calc.sqrt(-2 * calc.ln(u1)) * calc.cos(2 * calc.pi * u2) * (0.8 + 0.25 * calc.sin(x / W * 2 * calc.pi))
    if v > 0.15 and v < H - 0.15 { pts.push((x, v)) }
  }
  for i in range(1, 10) { line((i, 0), (i, H), stroke: 0.3pt + rule) }
  for j in range(1, 7) { line((0, j * H / 6.4), (W, j * H / 6.4), stroke: 0.3pt + rule) }
  let (cx, cy) = (6.0, 3.0)
  rect((cx, cy), (cx + 1, cy + 1), fill: rgb("#B5500022"), stroke: 1.1pt + plot-orange)
  for p in pts { circle(p, radius: 0.055, fill: plot-blue, stroke: none) }
  line((0, 0), (W + 0.4, 0), mark: (end: "stealth"), stroke: 0.7pt + ink, fill: ink)
  line((0, 0), (0, H + 0.4), mark: (end: "stealth"), stroke: 0.7pt + ink, fill: ink)
  content((W + 0.4, -0.5), [$x$])
  content((-0.45, H + 0.4), [$v$])
  content((cx + 0.5, cy + 1.2), anchor: "south", text(fill: plot-orange)[$f thin Delta x thin Delta v$])
})

// Vertical model ladder as a grid: boxes, labelled arrows, and what each
// level keeps in the right column.
#let ladder() = {
  let box-w = 62mm
  let level(body) = box(width: box-w, height: 15mm, stroke: 0.6pt + ink, radius: 1.5mm,
    align(center + horizon, body))
  let step(label) = box(width: box-w, height: 13mm, {
    place(center + horizon, line(start: (0mm, -5mm), end: (0mm, 5mm), stroke: 0.7pt + ink))
    place(center + bottom, dy: -1mm, polygon(fill: ink, (-1.6mm, -3.2mm), (1.6mm, -3.2mm), (0mm, 0mm)))
    place(left + horizon, dx: box-w / 2 + 5mm, text(fill: muted, label))
  })
  let keeps(body) = align(left + horizon, text(fill: muted, body))
  grid(columns: (box-w, 14mm, auto), row-gutter: 0mm,
    level[$N$ particles], [], keeps[$6 N tilde.op 10^21$ numbers],
    step($chevron.l dot chevron.r$), [], [],
    level[$f_s (bold(x), bold(v), t)$], [], keeps[one function of 6 variables],
    step($integral bold(v)^k f_s dif^3 v$), [], [],
    level[moments], [], keeps[$n_s, bold(u)_s, p_s$ in 3D],
    step[closure], [], [],
    level[two fluids], [], keeps[electrons and ions],
    step($sum_s$), [], [],
    level[MHD], [], keeps[one conducting fluid],
  )
}
