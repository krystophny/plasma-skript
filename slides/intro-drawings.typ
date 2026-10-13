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

// The simple model hierarchy: four levels from particles to MHD. Each arrow
// names the averaging step and, below it, what that step loses.
#let hierarchy() = canvas(length: 1mm, {
  import draw: *
  let box-w = 64
  let box-h = 20
  let step = 42
  let x-text = 78
  let levels = (
    ([Particles], [$N$-body], [$bold(x)_j (t), bold(v)_j (t), quad j = 1, dots, N tilde.op 10^20$]),
    ([Kinetic], [distribution function], [$f_s (bold(x), bold(v), t)$ in 6D phase space]),
    ([Fluid], [moments], [$n_s, bold(u)_s, p_s$ in 3D, one fluid per species]),
    ([MHD], [one conducting fluid], [$rho, bold(u), p, bold(B)$ in 3D]),
  )
  let steps = (
    ([average over many particles per phase-space cell], [individual orbits; correlations survive only as collisions $C[f_s]$]),
    ([velocity moments $integral bold(v)^k f_s dif^3 v$], [velocity-space structure and resonances; a closure is needed]),
    ([sum over species, $L >> rho_i$, $omega << omega_(c i)$], [charge separation, Hall term, electron inertia]),
  )
  for (k, (name, kind, state)) in levels.enumerate() {
    let y = -k * step
    rect((0, y), (box-w, y - box-h), radius: 1.5, stroke: 0.7pt + ink, fill: white)
    content((box-w / 2, y - box-h / 2), align(center)[#text(weight: "medium", name) \ #text(fill: muted, kind)])
    content((x-text, y - box-h / 2), anchor: "west", state)
  }
  for (k, (op, lost)) in steps.enumerate() {
    let y0 = -k * step - box-h
    let y1 = y0 - (step - box-h)
    line((box-w / 2, y0 - 1), (box-w / 2, y1 - 0.6), mark: (end: "stealth"),
      stroke: 0.9pt + ink, fill: ink)
    content((box-w / 2 + 7, (y0 + y1) / 2 + 4.6), anchor: "west", op)
    content((box-w / 2 + 7, (y0 + y1) / 2 - 4.6), anchor: "west",
      text(fill: plot-orange)[lost: #lost])
  }
})
