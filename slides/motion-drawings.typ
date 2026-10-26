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

// Gyration in B out of the page: the ion orbit (clockwise) with v_perp, the
// magnetic force and rho_L; optionally the electron orbit (counterclockwise)
// and the x-y axes of the component solution.
#let gyration-picture(electron: true, force: true, axes: false, unit: 11mm) = canvas(length: unit, {
  import draw: *
  let R = 2.4
  let ce = (5.2, 0.0)
  let re = 0.6
  for i in range(-3, 8) {
    for j in range(-3, 4) {
      let p = (i * 1.0 - 0.5, j * 1.0 + 0.5)
      let di = calc.sqrt(p.at(0) * p.at(0) + p.at(1) * p.at(1))
      let de = calc.sqrt(calc.pow(p.at(0) - ce.at(0), 2) + calc.pow(p.at(1) - ce.at(1), 2))
      let skip = di < R + 1.25 or (electron and de < re + 1.0) or (not electron and p.at(0) > 3.6)
      if not skip { b-out(p, r: 0.1) }
    }
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
  content((-R * 0.35 - 0.4, -R * 0.35 + 0.4), [$rho_L$])
  circle((0, R), radius: 0.12, fill: plot-orange, stroke: none)
  arrow((0.15, R), (1.6, R), w: 1.1pt)
  content((1.7, R), anchor: "west", [$bold(v)_perp$])
  if force {
    arrow((0, R - 0.15), (0, R - 1.3), paint: plot-orange, w: 1.1pt)
    content((0, R - 1.45), anchor: "north", text(fill: plot-orange)[$q_alpha bold(v) times bold(B)$])
  }
  content((0, -R - 0.5), text(fill: plot-orange)[ion])
  if electron {
    circle(ce, radius: re, stroke: 1.1pt + plot-blue)
    arc((ce.at(0) + re + 0.3, ce.at(1)), start: 0deg, stop: 60deg, radius: re + 0.3,
      anchor: "start", stroke: 0.8pt + plot-blue, mark: (end: "stealth", fill: plot-blue))
    circle(ce, radius: 0.05, fill: ink, stroke: none)
    circle((ce.at(0), ce.at(1) + re), radius: 0.1, fill: plot-blue, stroke: none)
    content((ce.at(0), ce.at(1) - re - 0.45), text(fill: plot-blue)[electron])
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

// grad-B: B out of the page, stronger at the top; smaller orbits there.
#let gradb-picture() = canvas(length: 11mm, {
  import draw: *
  for i in range(0, 9) {
    b-out((i * 1.0, 2.3), r: 0.13)
    if calc.rem(i, 2) == 0 { b-out((i * 1.0, -2.3), r: 0.08) }
  }
  arrow((-1.0, -1.4), (-1.0, 1.4), w: 1.2pt)
  content((-1.2, 0), anchor: "east", [$grad B$])
  polyline(drift-orbit(6.2, 0.5, 0.9, -0.28, 1, shrink: 0.3), plot-orange)
  polyline(drift-orbit(1.2, -1.2, 0.3, 0.093, -1, turns: 9, shrink: 0.3), plot-blue)
  content((7.5, 0.5), anchor: "west", text(fill: plot-orange)[ion])
  content((7.5, -1.2), anchor: "west", text(fill: plot-blue)[electron])
})

// Curvature: a field line bent about its centre of curvature; v_par along
// it; the ion drift into the page, the electron drift out of it.
#let curvature-picture() = canvas(length: 12mm, {
  import draw: *
  let R = 4.0
  arc((0, 0), start: 140deg, stop: 40deg, radius: R, anchor: "origin",
    stroke: 1.1pt + b-purple, mark: (end: "stealth", fill: b-purple))
  content((R * calc.cos(40deg) + 0.2, R * calc.sin(40deg) - 0.1), anchor: "west", text(fill: b-purple)[$bold(B)$])
  circle((0, 0), radius: 0.06, fill: ink, stroke: none)
  arrow((0, 0), (0, R - 0.08), w: 0.8pt)
  content((-0.15, R / 2), anchor: "east", [$R_c bold(e)_R$])
  arrow((-1.5, R + 0.25), (0.5, R + 0.25), w: 1.1pt)
  content((-0.5, R + 0.55), anchor: "south", [$v_parallel$])
  b-in((-3.0, 0.9), r: 0.2, paint: plot-orange)
  content((-2.7, 0.9), anchor: "west", text(fill: plot-orange)[ion])
  b-out((1.9, 1.5), r: 0.2, paint: plot-blue)
  content((2.2, 1.5), anchor: "west", text(fill: plot-blue)[electron])
})

// Magnetic mirror: field lines pinched at both ends, B_0 at the midplane.
#let mirror-picture() = canvas(length: 12mm, {
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

// Loss cone in velocity space at the midplane.
#let loss-cone-picture() = canvas(length: 12mm, {
  import draw: *
  let a = 35deg
  let r = 3.2
  line((-3.6, 0), (3.6, 0), stroke: 0.6pt + muted, mark: (end: "stealth", fill: muted))
  line((0, 0), (0, 3.4), stroke: 0.6pt + muted, mark: (end: "stealth", fill: muted))
  content((3.7, 0), anchor: "west", [$v_parallel$])
  content((0, 3.5), anchor: "south", [$v_perp$])
  for sgn in (1, -1) {
    line((0, 0), ..curve(t => (sgn * r * calc.cos(t), r * calc.sin(t)), 0deg, a, n: 40),
      close: true, fill: rgb("#0072B226"), stroke: none)
    line((0, 0), (sgn * r * calc.cos(a), r * calc.sin(a)), stroke: 0.9pt + plot-blue)
  }
  arc((1.4, 0), start: 0deg, stop: a, radius: 1.4, anchor: "start", stroke: 0.7pt + ink)
  content((1.75, 0.45), [$alpha_c$])
  content((2.6, 0.75), text(fill: plot-blue)[lost])
  content((0, 2.4), text(fill: plot-orange)[trapped])
})

// Guiding centre: r = R + rho.
#let guiding-centre-picture() = canvas(length: 14mm, {
  import draw: *
  polyline(drift-orbit(0, 0, 0.9, 0.25, 1, turns: 4), plot-orange, w: 0.9pt)
  line((0, 0), (2 * calc.pi * 4 * 0.25, 0), stroke: (paint: ink, thickness: 0.8pt, dash: "dashed"))
  let t = 2.4 * calc.pi
  let gc = (0.25 * t, 0)
  let p = (0.25 * t + 0.9 * calc.sin(t), 0.9 * calc.cos(t))
  let o = (-0.6, -3.2)
  arrow(o, gc, w: 0.9pt)
  arrow(o, p, paint: muted, w: 0.7pt)
  arrow(gc, p, paint: plot-orange, w: 0.9pt)
  circle(gc, radius: 0.07, fill: ink, stroke: none)
  content((o.at(0) - 0.1, o.at(1)), anchor: "east", text(fill: muted)[$O$])
  content(((o.at(0) + gc.at(0)) / 2 + 0.35, (o.at(1) + gc.at(1)) / 2 - 0.1), anchor: "west", [$bold(R)$])
  content(((o.at(0) + p.at(0)) / 2 - 0.25, (o.at(1) + p.at(1)) / 2 + 0.1), anchor: "east", text(fill: muted)[$bold(r)$])
  content((p.at(0) + 0.35, p.at(1) - 0.1), anchor: "west", text(fill: plot-orange)[$bold(rho)$])
})

// Mirror force: field lines converge towards +z (B grows); on the orbit ring
// B_r points to the axis and the gyro-averaged force points back to weak B.
#let mirror-force-picture() = canvas(length: 12mm, {
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

// Faraday's law over one gyration: B out of the page grows; the induced E
// circulates clockwise and does work on the clockwise ion.
#let faraday-picture() = canvas(length: 11mm, {
  import draw: *
  let R = 2.4
  for i in range(-1, 2) { for j in range(-1, 2) { b-out((i * 1.0, j * 1.0), r: 0.1) } }
  circle((0, 0), radius: R, stroke: 1.1pt + plot-orange)
  for k in range(4) {
    let a = 45deg + k * 90deg
    let p = (1.35 * R * calc.cos(a), 1.35 * R * calc.sin(a))
    let t = (calc.sin(a) * 0.8, -calc.cos(a) * 0.8)
    arrow((p.at(0) - t.at(0) / 2, p.at(1) - t.at(1) / 2), (p.at(0) + t.at(0) / 2, p.at(1) + t.at(1) / 2),
      paint: plot-blue, w: 1.1pt)
  }
  content((1.35 * R * 0.707 + 0.45, 1.35 * R * 0.707 + 0.1), anchor: "west", text(fill: plot-blue)[$bold(E)$])
  circle((0, R), radius: 0.12, fill: plot-orange, stroke: none)
  arrow((0.15, R), (1.5, R), w: 1.1pt)
  content((0.75, R + 0.15), anchor: "south", [$bold(v)_perp$])
  line((0, 0), (-R * 0.707, -R * 0.707), stroke: 0.7pt + ink)
  content((-R * 0.35 - 0.45, -R * 0.35 + 0.35), [$rho_L$])
  b-out((-3.5, -3.3), r: 0.16)
  content((-3.2, -3.3), anchor: "west", text(fill: b-purple)[$bold(B)(t)$])
})
