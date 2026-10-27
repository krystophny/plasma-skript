// Deck-only drawings for chapter 5 (single-particle motion).
#import "@preview/cetz:0.5.2": canvas, draw
#import "theme.typ": ink, muted, rule, plot-blue, plot-orange
#import "@preview/physica:0.9.8": grad

#let b-purple = rgb("#A0457E")

// B out of the page (dot in circle) and into the page (cross in circle).
#let b-out(pos, r: 0.13, paint: b-purple) = {
  import draw: *
  circle(pos, radius: r, stroke: 0.6pt + paint)
  circle(pos, radius: r * 0.28, fill: paint, stroke: none)
}
#let b-in(pos, r: 0.13, paint: b-purple) = {
  import draw: *
  circle(pos, radius: r, stroke: 0.6pt + paint)
  let d = r * 0.62
  line((pos.at(0) - d, pos.at(1) - d), (pos.at(0) + d, pos.at(1) + d), stroke: 0.6pt + paint)
  line((pos.at(0) - d, pos.at(1) + d), (pos.at(0) + d, pos.at(1) - d), stroke: 0.6pt + paint)
}
#let arrow(a, b, paint: ink, w: 0.9pt) = draw.line(a, b, mark: (end: "stealth"),
  stroke: w + paint, fill: paint)
#let polyline(points, paint, w: 1.1pt, dash: none) = draw.line(..points,
  stroke: (paint: paint, thickness: w, dash: dash))
// Sampled curve t -> (x, y) for t in [a, b].
#let curve(f, a, b, n: 160) = range(n + 1).map(k => f(a + (b - a) * k / n))
// Label on a white patch, so that field symbols underneath do not cut it.
#let tag(body) = box(fill: white, inset: 3pt, body)

// Side view of an ion helix about a base curve, base(s) = (point, unit
// tangent, unit normal). Ions turn left-handed about b, so the depth towards
// the viewer is -rho sin(2 pi s/pitch); the front half is solid, the back
// half faint. A slight oblique shift of the depth along the tangent
// (slant rho 2 pi/pitch = 0.3) hints at the turns without cusps or loops.
#let helix(base, s0, s1, rho, pitch, paint: plot-orange, n: 900) = {
  import draw: *
  let slant = 0.3 * pitch / (2 * calc.pi * rho)
  let pts = range(n + 1).map(k => {
    let s = s0 + (s1 - s0) * k / n
    let (p, t, nn) = base(s)
    let th = 2 * calc.pi * (s - s0) / pitch
    let depth = -rho * calc.sin(th)
    let y = rho * calc.cos(th)
    ((p.at(0) + y * nn.at(0) + slant * depth * t.at(0),
      p.at(1) + y * nn.at(1) + slant * depth * t.at(1)), depth >= 0)
  })
  let runs = ()
  let cur = (pts.at(0).at(0),)
  let front = pts.at(0).at(1)
  for k in range(1, pts.len()) {
    let (q, f) = pts.at(k)
    cur.push(q)
    if f != front {
      runs.push((front, cur))
      cur = (q,)
      front = f
    }
  }
  runs.push((front, cur))
  for (f, r) in runs {
    if f { line(..r, stroke: 1.3pt + paint) } else {
      line(..r, stroke: (paint: paint.transparentize(55%), thickness: 0.8pt))
    }
  }
}

// Gyration in B out of the page: the ion orbit (clockwise) with v_perp, the
// magnetic force and rho_L; optionally the electron orbit (counterclockwise)
// and the x-y axes of the component solution.
#let gyration-picture(electron: true, force: true, axes: false, unit: 11mm) = canvas(length: unit, {
  import draw: *
  let R = 2.4
  let ce = (5.2, 0.0)
  let re = 0.6
  // Regular field grid everywhere (B is uniform); labels sit on white patches.
  for i in range(-3, if electron { 8 } else { 5 }) {
    for j in range(-3, 4) { b-out((i * 1.0 - 0.5, j * 1.0 + 0.5), r: 0.1) }
  }
  b-out((-3.3, -3.3), r: 0.16)
  content((-3.0, -3.3), anchor: "west", text(fill: b-purple)[$bold(B)$])
  if axes {
    arrow((-3.2, 0), (3.4, 0), paint: muted, w: 0.6pt)
    arrow((0, -3.0), (0, 3.2), paint: muted, w: 0.6pt)
    content((3.5, 0), anchor: "west", text(fill: muted)[$x$])
    content((0, 3.3), anchor: "south", text(fill: muted)[$y$])
  }
  // ion: clockwise
  circle((0, 0), radius: R, stroke: 1.1pt + plot-orange)
  arc((R + 0.35, 0), start: 0deg, stop: -40deg, radius: R + 0.35, anchor: "start",
    stroke: 0.8pt + plot-orange, mark: (end: "stealth", fill: plot-orange))
  circle((0, 0), radius: 0.06, fill: ink, stroke: none)
  line((0, 0), (-R * 0.707, -R * 0.707), stroke: 0.7pt + ink)
  content((-1.5, -0.5), tag[$rho_L$])
  circle((0, R), radius: 0.12, fill: plot-orange, stroke: none)
  arrow((0.15, R), (1.6, R), w: 1.1pt)
  content((1.7, R), anchor: "west", tag[$bold(v)_perp$])
  if force {
    arrow((0, R - 0.15), (0, R - 1.3), paint: plot-orange, w: 1.1pt)
    content((0, R - 1.45), anchor: "north", tag(text(fill: plot-orange)[$q_alpha bold(v) times bold(B)$]))
  }
  content((0, -R - 0.5), tag(text(fill: plot-orange)[ion]))
  if electron {
    circle(ce, radius: re, stroke: 1.1pt + plot-blue)
    arc((ce.at(0) + re + 0.3, ce.at(1)), start: 0deg, stop: 60deg, radius: re + 0.3,
      anchor: "start", stroke: 0.8pt + plot-blue, mark: (end: "stealth", fill: plot-blue))
    circle(ce, radius: 0.05, fill: ink, stroke: none)
    circle((ce.at(0), ce.at(1) + re), radius: 0.1, fill: plot-blue, stroke: none)
    content((ce.at(0), ce.at(1) - re - 0.45), tag(text(fill: plot-blue)[electron]))
  }
})

// Trochoid of a gyrating particle drifting with u along x: sign +1 ion
// (clockwise for B out of the page), -1 electron. `shrink` makes the radius
// smaller at the top (grad-B).
#let drift-orbit(x0, y0, r, u, sign, turns: 3, shrink: 0.0) = curve(t => {
  let rr = r * (1 - shrink * sign * calc.cos(t))
  (x0 + u * t + rr * calc.sin(t), y0 + sign * rr * calc.cos(t))
}, 0, turns * 2 * calc.pi)

// E x B: E up, B out of the page; ion and electron drift to the right.
#let exb-picture(unit: 12mm) = canvas(length: unit, {
  import draw: *
  for i in range(0, 9) { for j in (-2.1, 2.1) { b-out((i * 1.2 - 0.3, j), r: 0.1) } }
  arrow((-1.0, -1.6), (-1.0, 1.6), paint: plot-orange, w: 1.3pt)
  content((-1.2, 0), anchor: "east", [$bold(E)$])
  polyline(drift-orbit(0.6, 0.6, 1.0, 0.33, 1), plot-orange)
  polyline(drift-orbit(0.6, -1.0, 0.25, 0.11, -1, turns: 9), plot-blue)
  content((7.5, 0.6), anchor: "west", text(fill: plot-orange)[ion])
  content((7.5, -1.0), anchor: "west", text(fill: plot-blue)[electron])
  arrow((3.2, -2.9), (5.2, -2.9), w: 1.1pt)
  content((5.3, -2.9), anchor: "west", [$bold(v)_D$])
  b-out((0.0, -2.9), r: 0.15)
  content((0.3, -2.9), anchor: "west", text(fill: b-purple)[$bold(B)$])
})

// grad-B: B out of the page, stronger at the top (larger symbols); the ion
// orbit is tighter there, so the ion drifts to the left, the electron right.
#let gradb-picture(unit: 11mm) = canvas(length: unit, {
  import draw: *
  for i in range(0, 9) {
    b-out((i * 1.0, 2.4), r: 0.16)
    b-out((i * 1.0, -2.4), r: 0.08)
  }
  content((4.0, -2.75), anchor: "north", text(fill: b-purple)[weaker $B$])
  arrow((-1.0, -1.4), (-1.0, 1.4), w: 1.2pt)
  content((-1.2, 0), anchor: "east", [$grad B$])
  polyline(drift-orbit(6.2, 0.5, 0.9, -0.28, 1, shrink: 0.3), plot-orange)
  polyline(drift-orbit(1.2, -1.2, 0.3, 0.093, -1, turns: 9, shrink: 0.3), plot-blue)
  content((7.5, 0.5), anchor: "west", text(fill: plot-orange)[ion])
  content((7.5, -1.2), anchor: "west", text(fill: plot-blue)[electron])
  arrow((4.6, 1.8), (2.2, 1.8), paint: plot-orange, w: 1.4pt)
  content((2.0, 1.8), anchor: "east", text(fill: plot-orange)[$bold(v)_D$])
  b-out((-1.6, -2.4), r: 0.16)
  content((-1.3, -2.4), anchor: "west", text(fill: b-purple)[$bold(B)$])
})

// Curvature: a field line bent about its centre of curvature, the unit
// tangent b and the curvature vector kappa = -e_R/R_c at one point, and the
// drift e_R x b: into the page for the ion, out of it for the electron.
#let curvature-picture(unit: 12mm) = canvas(length: unit, {
  import draw: *
  let R = 4.0
  arc((0, 0), start: 160deg, stop: 20deg, radius: R, anchor: "origin",
    stroke: 1.1pt + b-purple, mark: (end: "stealth", fill: b-purple))
  content((R * calc.cos(20deg) + 0.25, R * calc.sin(20deg)), anchor: "west", text(fill: b-purple)[$bold(B)$])
  circle((0, 0), radius: 0.07, fill: ink, stroke: none)
  arrow((0, 0), (0, R - 0.08), w: 0.8pt)
  content((0.15, R * 0.5), anchor: "west", [$R_c bold(e)_R$])
  let th = 128deg
  let p = (R * calc.cos(th), R * calc.sin(th))
  arrow(p, (p.at(0) + 1.5 * calc.sin(th), p.at(1) - 1.5 * calc.cos(th)), paint: b-purple, w: 1.2pt)
  content((p.at(0) + 0.9 * calc.sin(th) - 0.15, p.at(1) - 0.9 * calc.cos(th) + 0.2), anchor: "south-east", text(fill: b-purple)[$bold(b)$])
  arrow(p, (p.at(0) - 1.3 * calc.cos(th), p.at(1) - 1.3 * calc.sin(th)), paint: plot-blue, w: 1.4pt)
  content((p.at(0) - 1.1 * calc.cos(th) + 0.2, p.at(1) - 1.1 * calc.sin(th)), anchor: "west", text(fill: plot-blue)[$bold(kappa)$])
  b-in((-3.2, 0.45), r: 0.2, paint: plot-orange)
  content((-2.9, 0.45), anchor: "west", text(fill: plot-orange)[$bold(v)_D$ ion])
  b-out((0.9, 0.45), r: 0.2, paint: plot-blue)
  content((1.2, 0.45), anchor: "west", text(fill: plot-blue)[$bold(v)_D$ electron])
})


// Magnetic mirror: field lines pinched at both ends, B_0 at the midplane.
#let mirror-picture(unit: 12mm) = canvas(length: unit, {
  import draw: *
  let L = 5.0
  for s in (0.5, 1.0, 1.5) {
    for sgn in (1, -1) {
      polyline(curve(x => (x, sgn * s * (0.45 + 0.55 * calc.pow(calc.cos(calc.pi * x / (2 * L)), 2))), -L, L), b-purple, w: 0.8pt)
    }
  }
  for x in (-L, L) {
    rect((x - 0.25, 1.75), (x + 0.25, 2.25), fill: rgb("#526175"), stroke: none)
    rect((x - 0.25, -2.25), (x + 0.25, -1.75), fill: rgb("#526175"), stroke: none)
  }
  // bouncing particle: helix projected, reflected before the throats
  polyline(curve(t => (3.6 * calc.sin(t / 7.0), 0.45 * calc.cos(t) * (1 - 0.35 * calc.pow(calc.sin(t / 7.0), 2))), 0, 7 * calc.pi * 2, n: 600), plot-orange, w: 0.9pt)
  content((0, -2.25), [$B_0$])
  content((L, -2.75), [$B_max$])
  content((-L, -2.75), [$B_max$])
  arrow((-2.0, 2.6), (2.0, 2.6), paint: muted, w: 0.6pt)
  content((2.1, 2.6), anchor: "west", text(fill: muted)[$s$])
})

// Loss cone in velocity space at the midplane, drawn at theta_c = 30 deg
// (R_m = 4, as in the mirror animation and the loss-cone plot).
#let loss-cone-picture(unit: 12mm) = canvas(length: unit, {
  import draw: *
  let a = 30deg
  let r = 3.4
  line((-3.8, 0), (3.8, 0), stroke: 0.6pt + muted, mark: (end: "stealth", fill: muted))
  line((0, 0), (0, 3.6), stroke: 0.6pt + muted, mark: (end: "stealth", fill: muted))
  content((3.9, 0), anchor: "west", [$v_parallel$])
  content((0, 3.7), anchor: "south", [$v_perp$])
  for sgn in (1, -1) {
    line((0, 0), ..curve(t => (sgn * r * calc.cos(t), r * calc.sin(t)), 0deg, a, n: 40),
      close: true, fill: rgb("#0072B226"), stroke: none)
    line((0, 0), (sgn * r * calc.cos(a), r * calc.sin(a)), stroke: 0.9pt + plot-blue)
    content((sgn * 2.75 * calc.cos(a / 2), 2.75 * calc.sin(a / 2)), text(fill: plot-blue)[lost])
  }
  arc((1.3, 0), start: 0deg, stop: a, radius: 1.3, anchor: "start", stroke: 0.7pt + ink)
  content((1.62 * calc.cos(a / 2), 1.62 * calc.sin(a / 2)), [$theta.alt_c$])
  content((0.9, 2.5), text(fill: plot-orange)[trapped])
})

// Guiding centre, side view: ion helix about the field line through R
// (axis b); the particle at the top of a turn, so that rho = r - R points
// from R to the particle, perpendicular to b.
#let guiding-centre-picture(unit: 10mm) = canvas(length: unit, {
  import draw: *
  let rl = 1.6
  let pitch = 4.4
  let x1 = 22.0
  line((-0.4, 0), (x1, 0), stroke: 1.0pt + b-purple, mark: (end: "stealth", fill: b-purple))
  content((x1 + 0.2, 0), anchor: "west", text(fill: b-purple)[$bold(b)$])
  helix(s => ((s, 0.0), (1.0, 0.0), (0.0, 1.0)), 0.0, 20.6, rl, pitch)
  let s0 = 3 * pitch
  let gc = (s0, 0.0)
  let p = (s0, rl)
  let o = (s0 - 6.0, -3.6)
  arrow(o, gc, w: 1.2pt)
  arrow(o, p, paint: muted, w: 1.0pt)
  arrow(gc, p, paint: plot-orange, w: 1.4pt)
  circle(gc, radius: 0.1, fill: ink, stroke: none)
  circle(p, radius: 0.14, fill: plot-orange, stroke: none)
  content((o.at(0) - 0.15, o.at(1)), anchor: "east", text(fill: muted)[$O$])
  content((o.at(0) + 0.55 * 6.0 + 0.25, o.at(1) + 0.55 * 3.6 - 0.35), anchor: "north-west", [$bold(R)$])
  content((o.at(0) + 0.45 * 6.0 - 0.3, o.at(1) + 0.45 * (3.6 + rl) + 0.3), anchor: "south-east", text(fill: muted)[$bold(r)$])
  content((s0 + 0.2, rl / 2), anchor: "west", tag(text(fill: plot-orange)[$bold(rho)$]))
})

// Mirror force: field lines converge towards +z (B grows); on the orbit ring
// B_r points to the axis and the gyro-averaged force points back to weak B.
#let mirror-force-picture(unit: 12mm) = canvas(length: unit, {
  import draw: *
  let r(s, z) = s * calc.exp(-0.11 * z)
  for s in (0.9, 1.7, 2.5) {
    for sgn in (1, -1) {
      polyline(curve(z => (z, sgn * r(s, z)), -0.5, 7.0), b-purple, w: 0.8pt)
    }
  }
  content((7.1, r(2.5, 7.0)), anchor: "west", text(fill: b-purple)[$bold(B)$])
  arrow((-0.5, -3.1), (7.0, -3.1), paint: muted, w: 0.6pt)
  content((7.1, -3.1), anchor: "west", text(fill: muted)[$z$])
  line((-0.5, 0), (7.0, 0), stroke: (paint: muted, thickness: 0.5pt, dash: "dashed"))
  let z0 = 3.0
  let rl = r(1.7, z0)
  circle((z0, 0), radius: (0.42, rl), stroke: 1.1pt + plot-orange)
  circle((z0, rl), radius: 0.11, fill: plot-orange, stroke: none)
  arrow((z0 + 0.12, rl + 0.95), (z0 + 0.12, rl + 0.2), paint: b-purple, w: 1.1pt)
  content((z0 + 0.3, rl + 0.75), anchor: "west", text(fill: b-purple)[$B_r$])
  arrow((z0 - 0.5, 0), (z0 - 2.2, 0), paint: plot-orange, w: 1.3pt)
  content((z0 - 2.3, 0.05), anchor: "south-east", text(fill: plot-orange)[$F_parallel$])
  line((z0 + 0.6, 0), (z0 + 0.6, -rl), stroke: 0.6pt + ink)
  content((z0 + 0.7, -rl / 2), anchor: "west", [$rho_L$])
})

// Faraday's law over one gyration: B out of the page grows everywhere; the
// induced E circulates clockwise and does work on the clockwise ion.
#let faraday-picture(unit: 11mm) = canvas(length: unit, {
  import draw: *
  let R = 2.4
  for i in range(-4, 5) { for j in range(-4, 5) { b-out((i * 1.0, j * 1.0), r: 0.1) } }
  circle((0, 0), radius: R, stroke: 1.3pt + plot-orange)
  for k in range(4) {
    let a = 45deg + k * 90deg
    let p = (1.35 * R * calc.cos(a), 1.35 * R * calc.sin(a))
    let t = (calc.sin(a) * 0.8, -calc.cos(a) * 0.8)
    arrow((p.at(0) - t.at(0) / 2, p.at(1) - t.at(1) / 2), (p.at(0) + t.at(0) / 2, p.at(1) + t.at(1) / 2),
      paint: plot-blue, w: 1.3pt)
  }
  content((1.35 * R * 0.707 + 0.5, 1.35 * R * 0.707 + 0.1), anchor: "west", tag(text(fill: plot-blue)[$bold(E)$]))
  circle((0, R), radius: 0.13, fill: plot-orange, stroke: none)
  arrow((0.15, R), (1.5, R), w: 1.2pt)
  content((0.75, R + 0.2), anchor: "south", tag[$bold(v)_perp$])
  line((0, 0), (-R * 0.707, -R * 0.707), stroke: 0.8pt + ink)
  content((-R * 0.35 - 0.45, -R * 0.35 + 0.35), tag[$rho_L$])
  b-out((-4.0, -4.75), r: 0.16)
  content((-3.7, -4.75), anchor: "west", text(fill: b-purple)[$bold(B)(t)$])
})

// Field-line following: an ion helix centred on a curved field line; kappa
// points to the centre of curvature, the ion drift v_D^curv ~ b x kappa goes
// into the page; one pass has arc length ell.
#let field-line-picture(unit: 10mm) = canvas(length: unit, {
  import draw: *
  let x0 = 0.6
  let x1 = 18.0
  let rl = 0.75
  let c = 9.6
  let yf(x) = 1.6 * (1 - calc.pow((x - c) / 10.8, 2))
  let base(x) = {
    let d = -2 * 1.6 * (x - c) / (10.8 * 10.8)
    let n = calc.sqrt(1 + d * d)
    ((x, yf(x)), (1 / n, d / n), (-d / n, 1 / n))
  }
  polyline(curve(x => (x, yf(x)), -1.2, 19.6), b-purple, w: 1.1pt)
  arrow((19.6, yf(19.6)), (20.0, yf(20.0)), paint: b-purple, w: 1.1pt)
  content((20.1, yf(20.0)), anchor: "west", text(fill: b-purple)[$bold(b)$])
  content((19.4, yf(19.4) - 0.45), anchor: "north-east", text(fill: b-purple)[field line])
  helix(base, x0, x1, rl, (x1 - x0) / 6)
  circle((x0, yf(x0)), radius: 0.08, fill: ink, stroke: none)
  line((x0 - 0.9, yf(x0)), (x0 - 0.9, yf(x0) + rl), stroke: 0.7pt + ink, mark: (start: "stealth", end: "stealth", fill: ink, scale: 0.6))
  content((x0 - 1.05, yf(x0) + rl / 2), anchor: "east", [$rho_L$])
  arrow((c, yf(c) - 1.0), (c, yf(c) - 2.1), paint: plot-blue, w: 1.4pt)
  content((c + 0.2, yf(c) - 1.6), anchor: "west", text(fill: plot-blue)[$bold(kappa)$])
  b-in((12.6, yf(12.6) + 1.4), r: 0.2, paint: plot-orange)
  content((12.9, yf(12.6) + 1.4), anchor: "west", text(fill: plot-orange)[$bold(v)_D^"curv"$ (ion)])
  line((x0, -1.4), (x1, -1.4), stroke: 0.7pt + ink, mark: (start: "stealth", end: "stealth", fill: ink))
  content(((x0 + x1) / 2, -1.55), anchor: "north", [$ell$])
})
