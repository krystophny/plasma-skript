#import "@preview/cetz:0.5.2"
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "@preview/lilaq:0.6.0" as lq
#import "theme.typ": accent, blue, orange, muted

#let model-hierarchy = figure(
  alt: "A model hierarchy diagram. The full particle-field description is at the top. Arrows lead downward to kinetic, multiple-fluid, and single-fluid magnetohydrodynamic descriptions, each retaining fewer microscopic degrees of freedom.",
  caption: [
    Model hierarchy from a full particle-field description to reduced fluid
    models. The arrows indicate coarse-graining and closure assumptions, not a
    universal ranking of physical accuracy. All labels are model names, not
    dimensional quantities.
  ],
)[
  #fletcher.diagram(
    spacing: (3cm, 1.2cm),
    node-stroke: 1pt,
    edge-stroke: 1pt,
    node((0, 0), [Particle--field model]),
    node((-1.2, -1), [Kinetic\ $f(t, bold(r), bold(v))$]),
    node((1.2, -1), [Multiple fluid]),
    node((0, -2), [Single-fluid MHD]),
    edge((0, 0), (-1.2, -1), [coarse-grain], "->"),
    edge((0, 0), (1.2, -1), [species moments], "->"),
    edge((-1.2, -1), (0, -2), [closure], "->"),
    edge((1.2, -1), (0, -2), [one-fluid limit], "->"),
  )
]

#let gyroradius-geometry = figure(
  alt: "A circular orbit in a uniform magnetic field. The orbit center is marked, the radius from the center to the particle is labelled gyroradius, and a straight arrow shows the perpendicular velocity at the particle.",
  caption: [
    Geometry of uniform-field gyromotion. The radius is the gyroradius
    $rho$ (a length in Gaussian CGS), and the tangent arrow represents the
    perpendicular velocity $bold(v)_perp$.
  ],
)[
  #cetz.canvas({
    import cetz.draw: *
    circle((0, 0), radius: 1.2, stroke: 1pt + blue)
    circle((0, 0), radius: 0.06, fill: orange, stroke: none)
    circle((1.2, 0), radius: 0.08, fill: accent, stroke: none)
    line((0, 0), (1.2, 0), stroke: 1pt + orange)
    line((1.2, 0), (1.2, 0.75), stroke: 1pt + accent)
    content((0, -0.28), [guiding center])
    content((0.6, 0.18), [$rho$])
    content((1.35, 0.82), [$bold(v)_perp$])
  })
]

#let debye-profile = figure(
  alt: "A dimensionless plot of screened electrostatic potential versus distance measured in Debye lengths. The potential is largest at zero distance and decreases symmetrically toward zero as the distance exceeds several Debye lengths.",
  caption: [
    Illustrative Debye screening profile. Both axes are dimensionless: the
    distance is normalized by the electron Debye length $lambda_D$, and the
    potential is normalized by its value $phi_0$ at the source.
  ],
)[
  #lq.diagram(
    width: 10cm,
    height: 5.2cm,
    xlabel: [$x / lambda_D$ (dimensionless)],
    ylabel: [$phi / phi_0$ (dimensionless)],
    lq.plot(
      (-4, -3, -2, -1, 0, 1, 2, 3, 4),
      (0.018, 0.050, 0.135, 0.368, 1, 0.368, 0.135, 0.050, 0.018),
      color: blue,
      mark: "o",
      label: [screened potential],
    ),
  )
]
