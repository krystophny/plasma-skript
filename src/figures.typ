#import "figure-models.typ" as model
#import "@preview/cetz:0.5.2"
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "@preview/lilaq:0.6.0" as lq
#import "@preview/physica:0.9.8": grad, pdv, curl, dv, laplacian
#import "theme.typ": accent, accent-light, blue, ink, orange, muted, normalized-axis, normalized-label, paper, unit


// Quiet plot style shared by web SVG and paged output: no mirrored axes or
// minor ticks, a faint grid, thin gray spines, and outward ticks.
#let plot-style(it) = {
  show: lq.set-diagram(
    xaxis: (subticks: none, mirror: false),
    yaxis: (subticks: none, mirror: false),
  )
  show: lq.set-grid(stroke: 0.4pt + luma(91%))
  show: lq.set-spine(stroke: 0.5pt + luma(40%))
  show: lq.set-tick(inset: 0pt, outset: 3pt, stroke: 0.5pt + luma(40%))
  show: lq.set-legend(stroke: none, fill: none)
  it
}
#let plot-diagram(..args) = context {
  let body = { show: plot-style; lq.diagram(..args) }
  if target() == "paged" { body }
  else { html.div(class: "quantitative-plot")[#body] }
}
// A plot of a derived result: plot_<name>() in derivations/chapters/chNN_*.py
// lambdifies the tested SymPy expression and writes
// derivations/build/fig/<name>.svg (used here) and .pdf (used by the slides).
// Image alt text: the plot's name in words; the enclosing figure's `alt`
// carries the full description.
#let plot-alt(name) = "Plot: " + name.replace("_", " ").replace("-", " ")
// The default `auto` keeps the natural si.figure size, so the 10 pt figure
// text matches every other natural-size plot.
#let derived-plot(name, width: auto) = context {
  // The outline is needed before these derivations can generate their figures.
  if sys.inputs.at("outline-only", default: "false") != "true" {
    let img = image("/derivations/build/fig/" + name + ".svg", width: width,
      alt: plot-alt(name))
    if target() == "paged" { align(center, img) }
    else { html.div(class: "quantitative-plot", img) }
  }
}
// Two derived plots side by side, for a direct comparison on equal axes.
// Each panel is drawn at its native width (si.figure size), so the text size
// matches a single derived plot.
#let derived-plot-pair(left, right, width: auto) = context {
  if sys.inputs.at("outline-only", default: "false") != "true" {
    let img(name) = image("/derivations/build/fig/" + name + ".svg", width: width,
      alt: plot-alt(name))
    if target() == "paged" {
      align(center, grid(columns: 2, column-gutter: 0.8cm, img(left), img(right)))
    } else {
      html.div(style: "display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem;",
        html.div(class: "quantitative-plot", img(left))
        + html.div(class: "quantitative-plot", img(right)))
  }
  }
}
#let samples(lo, hi, n: 80) = range(n + 1).map(i => lo + (hi - lo) * i / n)
// Okabe–Ito blue and vermilion plus a neutral gray. Every curve also carries
// a distinct dash pattern and a direct label, so color is never the only cue.
#let plot-blue = rgb("#0072B2")
#let plot-orange = rgb("#B55000")
#let plot-gray = rgb("#555555")
#let plot-stroke = 1.1pt
// A smooth analytic curve: no markers; `dash` gives the redundant encoding.
#let curve(xs, f, color: plot-blue, dash: none) = (
  lq.plot(xs, xs.map(f), color: color, mark: none,
    stroke: (thickness: plot-stroke, dash: dash)),
)
// Explicit decimal labels for logarithmic axes with few decades.
#let decimal-ticks(values) = values.map(v => (v, [#v]))
// A direct curve label in data coordinates, set in the curve color.
#let tag(x, y, body, color: plot-blue, align: left) = lq.place(x, y,
  align: align, pad(0.3em, text(size: 0.9em, fill: color.darken(15%), body)))

// CeTZ and Fletcher drawings need an explicit frame in HTML export; the
// site build supplies theme-aware paint without changing the drawing geometry.
#let graphic(body) = context {
  if target() == "paged" { body }
  else { html.div(class: "quantitative-plot", html.frame(body)) }
}

// Quiet concept-diagram style: thin gray rectangles, slightly darker
// connectors, smaller edge labels. Diagrams read from top to bottom.
#let concept-style = (
  node-stroke: 0.6pt + luma(55%),
  edge-stroke: 0.7pt + luma(25%),
  node-corner-radius: 3pt,
  node-shape: rect,
  label-size: 0.85em,
)

#let web-model-map() = context {
  set text(font: "STIX Two Text", size: 11pt, fill: rgb("#1c1f23"))
  let note(body) = text(size: 10.5pt, fill: rgb("#4a5058"), style: "italic", body)
  let detail(body) = text(size: 9.5pt, fill: rgb("#4a5058"), body)
  let box(pos, body, name) = node(pos, align(center, body), name: name,
    width: 3.2cm)
  fletcher.diagram(
    node-inset: 7pt,
    node-stroke: 0.6pt + luma(55%),
    node-fill: white,
    node-corner-radius: 3pt,
    edge-stroke: 0.7pt + luma(25%),
    box((0cm, 0cm), [Particles + fields \ #detail[particle ODEs \ Maxwell PDEs]], <particles>),
    box((-2.1cm, -3.2cm), [Single-particle \ motion \ #detail[one trajectory]], <orbit>),
    box((2.1cm, -3.2cm), [Kinetic theory \ #detail[one PDE/species \ 6+1D]], <kinetic>),
    box((2.1cm, -6.4cm), [Multiple-fluid \ theory \ #detail[species fluids \ 3+1D]], <fluids>),
    box((2.1cm, -9.6cm), [Single-fluid \ MHD \ #detail[bulk fluid \ 3+1D]], <mhd>),
    edge(<particles.south>, <orbit.north>, "->"),
    edge(<particles.south>, <kinetic.north>, "->"),
    edge(<kinetic.south>, <fluids.north>, "->"),
    edge(<fluids.south>, <mhd.north>, "->"),
    node((-3cm, -1.8cm), note([prescribed \ fields]), stroke: none, fill: none),
    node((3cm, -1.8cm), note([coarse \ graining]), stroke: none, fill: none),
    node((-0.05cm, -4.8cm), note([velocity moments \ + closure]), stroke: none, fill: none),
    node((-0.05cm, -8cm), note([combine species \ + MHD ordering]), stroke: none, fill: none),
  )
}

#let model-hierarchy = context {
  let alt-description = "Particle ODEs coupled to Maxwell's equations branch to a prescribed-field single trajectory, or to one kinetic PDE per species in six phase-space coordinates and time. Velocity moments and closure give one fluid per species in three spatial coordinates and time; combining species with MHD assumptions gives one bulk fluid."
  let caption-text = [
    Two reductions of the particle--field description. Prescribing the
    fields gives a test-particle model; retaining collective feedback leads
    to kinetic and fluid descriptions, with an additional assumption at each
    step. 6+1D: three position and three velocity coordinates and time;
    3+1D: position and time. At 100 grid points per coordinate a 3D grid has
    $10^6$ points and a 6D grid $10^12$: the curse of dimensionality.
  ]

  if target() == "paged" {
    figure(alt: alt-description, caption: caption-text, web-model-map())
  } else {
    html.figure(
      class: "concept-figure model-figure",
      aria-label: "Plasma models: prescribed fields give a test-particle model; coarse graining gives kinetic theory; velocity moments and closure give species fluids; combining species with further assumptions gives MHD.",
    )[
      // Keep responsive sizing with the SVG even when site CSS is cached.
      #html.style(".model-figure-diagram svg { display: block; width: 100% !important; max-width: 26rem; height: auto !important; margin-inline: auto; }")
      #html.div(class: "model-figure-diagram quantitative-plot", role: "img",
        aria-label: "Particle ODEs coupled to Maxwell's equations branch to a prescribed-field single trajectory, or to one kinetic PDE per species in six phase-space coordinates and time. Velocity moments and closure give one fluid per species in three spatial coordinates and time; combining species with MHD assumptions gives one bulk fluid.")[
        #html.frame[#web-model-map()]
      ]
      #html.figcaption[
        Two reductions of the particle–field description. Prescribing the
        fields gives a test-particle model. Retaining collective feedback
        leads to kinetic and fluid descriptions, with an additional
        assumption at each reduction.
        Here 6+1D means three position coordinates, three velocity
        coordinates, and time; 3+1D retains position and time.
        These coordinates are in #unit("m"), #unit("m/s"), and
        #unit("s"), respectively. ODE and PDE denote ordinary and partial
        differential equations.
      ]
    ]

    html.p[
      For $N = 10^20$ particles (a count with unit [1]), the
      microscopic model has $N$ coupled vector equations for the trajectories,
      together with the four Maxwell equations, including their constraints.
      Kinetic theory replaces those individual trajectories with one
      distribution function per species. Fluid models keep density, bulk
      velocity, and pressure, and use a closure for discarded velocity detail.
    ]

    html.p[
      This is the #html.strong[curse of dimensionality]: at fixed resolution
      per coordinate, the size of a full grid grows exponentially with the
      number of coordinates. At 100 grid points per coordinate, each added
      coordinate multiplies the storage by 100. A three-coordinate grid has $10^6$ points and a
      six-coordinate grid has $10^12$ points. Storing one 8-byte scalar per
      point requires 8 MB and 8 TB, respectively. Counts have unit [1];
      MB and TB use decimal bytes.
    ]

    html.details(class: "disclosure", open: false)[
      #html.summary[Why kinetic models need more grid points]
      #html.p[
        A fluid field depends on three position coordinates and time. A
        kinetic distribution also depends on three velocity coordinates.
        The particle description instead evolves a trajectory for each
        particle, together with Maxwell's field equations.
      ]
      #html.p[
        With 100 points per coordinate, each additional coordinate multiplies
        the point count by 100. A two-coordinate position–velocity slice
        already has $10^4$ points. Counts have unit [1].
      ]
      #html.p[
        These estimates count one stored scalar.
        Multiple species, field components, time integration, and boundary
        data add storage. Coarser grids or other representations change
        the cost, but require their own accuracy checks.
      ]
    ]

  }
}

#let gyroradius-geometry = figure(
  alt: "A circular orbit of a positive charge in a uniform magnetic field pointing into the page, traversed counterclockwise. The orbit center is marked, the radius from the center to the particle is labelled gyroradius, and a straight arrow shows the perpendicular velocity at the particle.",
  caption: [
    Geometry of uniform-field gyromotion for a positive charge, with
    $bold(B)$ into the page ($times.o$). The radius is the gyroradius
    $rho$ (a length in #unit("m")), and the tangent arrow represents the
    perpendicular velocity $bold(v)_perp$; a negative charge circles the
    other way.
  ],
)[
  #graphic(cetz.canvas({
    import cetz.draw: *
    circle((0, 0), radius: 1.5, stroke: 1pt + blue)
    circle((0, 0), radius: 0.05, fill: ink, stroke: none)
    line((0, 0), (1.5, 0), stroke: 0.8pt + ink)
    circle((1.5, 0), radius: 0.08, fill: accent, stroke: none)
    line((1.5, 0), (1.5, 0.95), stroke: 1pt + accent, mark: (end: "stealth", fill: accent))
    content((0, -0.32), text(size: 0.9em)[guiding center])
    content((0.75, 0.24), [$rho$])
    content((1.82, 0.95), [$bold(v)_perp$])
    content((-1.55, 1.3), [$times.o thin bold(B)$])
  }))
]

#let debye-screened-point = figure(
  alt: "Radial plot of the potential of a point charge with and without Debye shielding. The dashed bare Coulomb potential falls off as 1 over r. The solid screened potential lies below it everywhere and decays to nearly zero within about three Debye lengths.",
  caption: [
    Bare (dashed) and Debye-screened (solid) potential of a point charge,
    $Q\/(4 pi epsilon_0 r)$ and $Q e^(-r\/lambda_D)\/(4 pi epsilon_0 r)$,
    from the expressions derived above. Radius in units of $lambda_D$,
    potential in units of $Q\/(4 pi epsilon_0 lambda_D)$. Their ratio is
    $e^(-r\/lambda_D)$; at $r = lambda_D$ the screened potential is $1\/e$
    of the bare one.
  ],
)[#derived-plot("debye_potential")]

#let debye-potential-comparison = figure(
  alt: "Two radial plots on identical axes, each comparing a dashed bare potential with a solid Debye-screened potential. Left: a point charge, where both curves diverge at the origin. Right: a permeable, uniformly charged sphere of radius half a Debye length, where the bare potential is quadratic and finite inside the sphere and the screened potential is lower everywhere. Outside the sources both screened curves decay to nearly zero within about three Debye lengths.",
  caption: [
    Point charge (left) and permeable, uniformly charged sphere of radius
    $R = lambda_D\/2$ (right), each bare (dashed) and Debye-screened (solid),
    from the expressions derived above. Same axes: radius in units of
    $lambda_D$, potential in units of $Q\/(4 pi epsilon_0 lambda_D)$. The
    finite source removes the central singularity; outside $R$ both screened
    curves carry the same exponential suppression of the Coulomb tail. The
    linear model assumes $abs(e phi) << k_B T_e$ throughout, which this
    normalization does not impose by itself.
  ],
)[#derived-plot-pair("debye_potential", "debye_sphere_potential")]

#let debye-regime-map = figure(
  alt: "Log-log plane of electron density from 10 to the 6 to 10 to the 32 per cubic metre and electron temperature from 0.01 eV to 100 keV. Three dashed lines of slope one mark Debye lengths of 100 m, 0.01 m and 1 micrometre. A solid line of slope one third marks N_D equal to one; the shaded region below it, at high density and low temperature, has N_D below one. Five example plasmas, ionosphere, H II region, solar corona, Hall thruster and tokamak core, all lie far above that line.",
  caption: [
    Where the collective ordering holds. Dashed: $lambda_D = L$, i.e.
    $k_B T_e = e^2 n_e L^2\/epsilon_0$, for three system sizes $L$; plasmas
    to the right of a line are quasineutral on that scale. Solid:
    $N_D = 1$, i.e. $k_B T_e = (e^2\/epsilon_0)(3\/(4 pi))^(2\/3) n_e^(1\/3)$;
    the shaded side has $N_D < 1$. Dots: typical parameters of five example
    plasmas (order of magnitude).
  ],
)[#derived-plot("nt_map")]

#let moment-ambiguity = figure(
  alt: "One-dimensional velocity distributions with the same density, bulk velocity and temperature. The solid Maxwellian has a single peak at the bulk velocity. The dashed distribution consists of two narrower beams at plus and minus 0.6 thermal speeds, with a dip at the bulk velocity.",
  caption: [
    Same $n$, $bold(u)$ and $T$, different $f$: a Maxwellian (solid) and two
    beams at $(v-u)\/v_"th" = plus.minus 0.6$ (dashed) whose width is chosen
    to give the same variance $k_B T\/m$. One velocity component,
    $v_"th" = sqrt(2 k_B T\/m)$; $f$ in units of $n\/v_"th"$. The moments
    first differ at fourth order.
  ],
)[#derived-plot("moment_ambiguity", width: 8.6cm)]

#let plasma-frequency-scale = figure(
  alt: "Log-log plot of the electron plasma frequency in hertz against electron density per cubic metre. A straight line of slope one half rises from about 10 kilohertz at 10 to the 6 per cubic metre. Horizontal guides mark megahertz, gigahertz and terahertz. Five example plasmas lie on the line: H II region near 0.3 MHz, ionosphere near 9 MHz, solar corona near 0.3 GHz, Hall thruster near 9 GHz and tokamak core near 90 GHz.",
  caption: [
    Electron plasma frequency $f_(p,e) = omega_(p,e)\/(2 pi)$ against
    electron density, with the five example plasmas of the
    density--temperature map. $f_(p,e)$ grows as $sqrt(n_e)$: radio for
    space plasmas, microwave for laboratory and fusion plasmas.
  ],
)[#derived-plot("plasma_frequency")]

#let collision-paths = figure(
  alt: "Two particle paths from left to right. Top, neutral gas: straight flights broken by four sharp turns, each marked by a dot for a hard collision. Bottom, plasma: a path made of many short segments, each turned by a small random angle, so the direction wanders gradually without any single sharp turn.",
  caption: [
    Neutral gas (top): straight flights between a few hard, large-angle
    collisions (dots). Plasma (bottom): many small-angle Coulomb deflections
    whose accumulated effect turns the particle by a comparable angle.
  ],
)[
  #let neutral = ((0, 0), (1.3, 0.06), (2.2, 0.42), (3.4, -0.22), (4.6, -0.1), (5.8, 0.3))
  // Small random kicks to the heading (fixed pseudo-random sequence), with a
  // weak pull back to the row: 75 steps of length 0.078.
  #let plasma = range(75).fold(((0, 0, 0),), (acc, i) => {
    let (x, y, th) = acc.last()
    let th2 = 0.95*th + 0.22*calc.sin(i*i*2.399 + 1.3) - 0.12*y
    acc + ((x + 0.078*calc.cos(th2), y + 0.078*calc.sin(th2), th2),)
  }).map(p => (p.at(0), p.at(1)))
  #graphic(cetz.canvas(length: 1.5cm, {
    import cetz.draw: *
    let row(dy, pts) = pts.map(((x, y)) => (x, y + dy))
    line(..row(1.2, neutral), stroke: 1pt + plot-blue)
    for p in row(1.2, neutral).slice(1, -1) {
      circle(p, radius: 0.06, fill: plot-blue, stroke: none)
    }
    line(..plasma, stroke: 1pt + plot-orange)
    content((6.1, 1.5), anchor: "west", text(fill: plot-blue)[neutral gas])
    content((6.1, plasma.last().at(1)), anchor: "west", text(fill: plot-orange)[plasma])
  }))
]

#let moment-hierarchy = figure(
  alt: "The distribution function f supplies, by velocity moments (thin dashed lines), the density n, the bulk velocity u, the pressure tensor P, and the third central tensor Q. Solid arrows run from each moment to the next: the continuity equation for n contains u, the momentum equation contains P, the pressure equation contains Q, and the Q equation contains a still higher moment. A closure must cut the chain.",
  caption: [
    Each moment equation contains the next moment. The equation for $n$
    contains $bold(u)$, the one for $bold(u)$ contains $bold(P)$, and the
    one for $bold(P)$ contains the third central tensor $bold(Q)$, whose
    contraction is the heat flux $bold(q)$. A fluid model cuts the chain
    with a closure. Dashed lines: moments of $f$.
  ],
)[
  #graphic(fletcher.diagram(
    spacing: (1.25cm, 1.2cm),
    ..concept-style,
    node((1.5, 0), [$f(t, bold(r), bold(v))$]),
    node((0, 1), [$n$]),
    node((1, 1), [$bold(u)$]),
    node((2, 1), [$bold(P)$]),
    node((3, 1), [$bold(Q)$]),
    node((4.1, 1), [closure], stroke: (paint: luma(55%), thickness: 0.6pt, dash: "dashed")),
    ..range(4).map(i => edge((1.5, 0), (i, 1), stroke: (paint: luma(60%), thickness: 0.5pt, dash: "dashed"))),
    edge((0, 1), (1, 1), [cont.], "->", label-side: right),
    edge((1, 1), (2, 1), [mom.], "->", label-side: right),
    edge((2, 1), (3, 1), [pressure], "->", label-side: right),
    edge((3, 1), (4.1, 1), [$dots.c$], "->", label-side: right),
  ))
]

#let multiple-fluid-hierarchy = figure(
  alt: "A multiple-fluid hierarchy starts with one kinetic distribution for each species. The electron and ion distributions are separately reduced to electron and ion density, velocity, and pressure fields. Both fluids exchange sources and forces with the shared electric and magnetic fields; summing the species equations gives one-fluid variables.",
  caption: [
    Species-resolved moments retain the relative motion of electrons and
    ions. Each fluid supplies charge and current to Maxwell's equations and
    feels the Lorentz force of the shared field. A one-fluid description
    follows only after the sums and relative-flow terms are defined.
  ],
)[
  #graphic(fletcher.diagram(
    spacing: (2.6cm, 1.15cm),
    ..concept-style,
    node((0, 0), [Kinetic species states \ $f_(e), f_(i)$]),
    node((-1.7, 1), [Electron fluid \ $n_(e), bold(u)_(e), bold(P)_(e)$]),
    node((1.7, 1), [Ion fluid \ $n_(i), bold(u)_(i), bold(P)_(i)$]),
    node((0, 2), [Coupled fields \ $bold(E), bold(B)$]),
    node((0, 3), [One-fluid sums \ $rho, bold(u), bold(P), bold(j)$]),
    edge((0, 0), (-1.7, 1), [velocity moments], "->"),
    edge((0, 0), (1.7, 1), [velocity moments], "->"),
    edge((-1.7, 1), (0, 2), [sources, force], "<->"),
    edge((1.7, 1), (0, 2), [sources, force], "<->"),
    edge((0, 2), (0, 3), [sum and define], "->"),
  ))
]

#let mhd-reduction = figure(
  alt: "A reduction map shows electron and ion fluid equations being combined into total mass and momentum balances, while their difference supplies a generalized Ohm law. Closure and ordering assumptions then reduce the system to single-fluid MHD.",
  caption: [
    Single-fluid MHD keeps the variables that survive a mass-weighted sum and
    records the species difference through Ohm's law. Every arrow is an
    approximation or definition that must be stated.
  ],
)[
  #graphic(fletcher.diagram(
    spacing: (1.35cm, 1.15cm),
    ..concept-style,
    node((0, 0), [Electron + ion equations]),
    node((-1.45, 1), [Mass-weighted sum \ $rho, bold(u), bold(P)$]),
    node((1.45, 1), [Species difference \ $bold(E)+bold(u) times bold(B)$]),
    node((0, 2), [Single-fluid MHD \ mass, momentum, induction]),
    edge((0, 0), (-1.45, 1), [sum], "->"),
    edge((0, 0), (1.45, 1), [subtract], "->"),
    edge((-1.45, 1), (0, 2), [closure], "->"),
    edge((1.45, 1), (0, 2), [ordering], "->"),
  ))
]

#let mhd-flux-diffusion = figure(
  alt: "The induction equation splits into two regimes. At high magnetic Reynolds number, advection dominates and magnetic flux through a material loop is approximately frozen. With finite resistivity, the magnetic diffusivity D_B = eta/mu_0 lets field diffuse on the time L squared over D_B, and field topology can change.",
  caption: [
    The magnetic Reynolds number $R_m$ compares advection with diffusion in
    the induction equation. For $R_m >> 1$ field lines move with the fluid;
    finite resistivity lets them slip and diffuse.
  ],
)[
  #graphic(fletcher.diagram(
    spacing: (1.1cm, 1.15cm),
    ..concept-style,
    node((0, 0), [Induction equation \
      $partial_t bold(B)=curl (bold(u) times bold(B))+D_B laplacian bold(B)$]),
    node((-1.35, 1), [$R_m >> 1$ \ flux frozen, field moves with $bold(u)$]),
    node((1.35, 1), [$D_B=eta \/ mu_0$ finite \ diffusion in $tau_D=L^2 \/ D_B$]),
    edge((0, 0), (-1.35, 1), [advection dominates], "->"),
    edge((0, 0), (1.35, 1), [diffusion retained], "->"),
  ))
]

#let mhd-force-balance = figure(
  alt: "Cross-section of a z-pinch. Shading marks the pressure, highest on the axis. The current j_z flows out of the page on the axis, and the azimuthal field B_theta circles it. At a point inside the column, the pressure force minus grad p points outward and the magnetic force j cross B points inward with equal length: static force balance grad p = j cross B.",
  caption: [
    Static force balance $grad p=bold(j) times bold(B)$ in a $z$-pinch cross
    section. Pressure (shading) peaks on the axis, so $-grad p$ pushes
    outward; the axial current $j_z$ and its azimuthal field $B_theta$ give
    an inward $bold(j) times bold(B)$ of equal size.
  ],
)[
  #graphic(cetz.canvas(length: 1.25cm, {
    import cetz.draw: *
    for (r, l) in ((2.0, 95%), (1.5, 90%), (1.0, 85%), (0.5, 80%)) {
      circle((0, 0), radius: r, fill: luma(l), stroke: none)
    }
    circle((0, 0), radius: 2.0, stroke: 0.6pt + luma(55%))
    // B_theta: counterclockwise for j_z out of the page
    arc((0, 0), start: 150deg, stop: 420deg, radius: 2.35, anchor: "origin",
      stroke: 0.8pt + ink, mark: (end: ">", fill: ink))
    content((-2.45, -1.1), anchor: "east", $B_theta$)
    // axial current out of the page
    circle((0, 0), radius: 0.14, fill: white, stroke: 0.8pt + ink)
    circle((0, 0), radius: 0.035, fill: ink, stroke: none)
    content((-0.4, -0.3), $j_z$)
    // forces at a point inside the column, radius 1.35 at 100 degrees
    let (c, s) = (calc.cos(100deg), calc.sin(100deg))
    let at(r) = (r * c, r * s)
    circle(at(1.35), radius: 0.05, fill: ink, stroke: none)
    line(at(1.35), at(2.15), stroke: 1.3pt + orange, mark: (end: ">", fill: orange))
    line(at(1.35), at(0.55), stroke: 1.3pt + blue, mark: (end: ">", fill: blue))
    content((2.15 * c, 2.15 * s + 0.1), anchor: "south", text(fill: orange)[$-grad p$])
    content((0.95 * c + 0.2, 0.95 * s), anchor: "west",
      text(fill: blue)[$bold(j) times bold(B)$])
  }))
]

#let collision-regimes = figure(
  alt: "Two drivers of transport and their collisional responses. A density or temperature gradient, through collisional randomization, gives diffusion with flux minus D grad n. An applied force qE, through collisional drag, gives mobility u = mu E and, for charges, conductivity sigma.",
  caption: [
    Gradients and forces drive transport; collisions set the response.
    Collisions alone drive no current in a homogeneous equilibrium.
  ],
)[
  #graphic(fletcher.diagram(
    spacing: (2.2cm, 1.15cm),
    ..concept-style,
    node((0, 0), [Gradient \ $grad n, grad T$]),
    node((1, 0), [Applied force \ $q bold(E)$]),
    node((0, 1), [Diffusion \ $bold(Gamma)=-D grad n$]),
    node((1, 1), [Mobility $bold(u)=mu_("mob") bold(E)$ \ conductivity $sigma$]),
    edge((0, 0), (0, 1), [randomize], "->", label-side: left),
    edge((1, 0), (1, 1), [drag], "->", label-side: right),
  ))
]

#let coulomb-cutoff = figure(
  alt: "Momentum-transfer weight per logarithmic interval of impact parameter, in units of 4 pi b90 squared, versus b/b90 on a logarithmic axis from 0.01 to 1e8. The weight rises from zero below b90, is flat at one for every decade above b90, and is cut to zero at the Debye length, lambda_D/b90 = 4.2e6. The shaded area equals ln Lambda_cut, about 15.2.",
  caption: [
    Momentum transfer per logarithmic interval of impact parameter,
    $2 pi b^2 (1-cos chi)$ with $tan(chi\/2)=b_90\/b$, in units of
    $4 pi b_90^2$. Above $b_90$ every decade of $b$ contributes equally
    until screening cuts the integral at $lambda_D$, so the shaded area is a
    logarithm, $ln Lambda_"cut"$. Here $lambda_D\/b_90=4.2 times 10^6$ from the
    example below: $ln Lambda_"cut" approx 15.2=ln Lambda+ln 32$.
  ],
)[
  #derived-plot("coulomb-cutoff", width: 10cm)
]

#let conductivity-tensor = figure(
  alt: "Two panels on identical axes: DC conductivity of one species divided by the parallel conductivity, versus magnetization |Omega_s|/nu_s on a logarithmic axis from 0.01 to 100, with the parallel value one as a gray dotted line. Left: the Pedersen conductivity (blue, solid) falls from one to zero, passing one half at |Omega_s| = nu_s. Right: the Hall magnitude (orange, dashed) rises from zero to its maximum of one half at |Omega_s| = nu_s and falls again.",
  caption: [
    DC conductivity tensor of one species, Pedersen (left) and Hall (right)
    on the same axes: $sigma_perp\/sigma_parallel=1\/(1+X^2)$ and
    $abs(sigma_"H")\/sigma_parallel=X\/(1+X^2)$ with
    $X=abs(Omega_s)\/nu_s$. Weakly magnetized, the current follows
    $bold(E)$; at $abs(Omega_s)=nu_s$ (dot) Pedersen and Hall are equal;
    strongly magnetized, both vanish while $sigma_parallel$ is unchanged.
    The sign of $sigma_"H"$ follows the sign of $q_s$.
  ],
)[
  #derived-plot-pair("conductivity-pedersen", "conductivity-hall")
]

#let random-walk-diffusion = figure(
  alt: "Two Gaussian density profiles n/n0 versus x/L0, at t = tau_D (blue, solid) and t = 4 tau_D (orange, dashed). Double arrows mark plus and minus the rms width. From the first to the second time the rms width doubles and the peak halves, while the area stays the same.",
  caption: [
    A conserved pulse spreads by diffusion:
    $n\/n_0=tau^(-1\/2) exp(-xi^2\/(4 tau))$ with $xi=x\/L_0$, $tau=t\/tau_D$,
    $tau_D=L_0^2\/D$, and $n_0=N_0\/(sqrt(4 pi) L_0)$. From $t=tau_D$ to
    $t=4 tau_D$ the rms width $⟨x^2⟩^(1\/2)=sqrt(2 D t)$ (arrows) doubles and
    the peak halves; the area $N_0$ is conserved.
  ],
)[
  #derived-plot("random-walk-diffusion", width: 10cm)
]

#let ambipolar-balance = figure(
  alt: "Horizontal arrows show the x components of the electron and ion particle fluxes in the ambipolar worked example, in units of 1e17 per square metre per second. Electron diffusion alone gives about 17.6; the ambipolar field drift subtracts about 15.8. Ion diffusion gives about 1.0 and the field drift adds about 0.9. Both totals end on the common ambipolar flux 1.82, marked by a dotted vertical line.",
  caption: [
    Ambipolar diffusion in the example below. Diffusion alone (solid arrows)
    would carry electrons about 18 times faster than ions. The ambipolar
    field $E_a=0.897$ #unit("V/m") drifts electrons back and ions forward
    (dashed arrows) until both fluxes equal
    $Gamma_a=D_a abs(partial_x n)=1.82 times 10^17$ #unit("m^-2 s^-1").
  ],
)[
  #derived-plot("ambipolar-balance", width: 10cm)
]

#let cross-field-diffusion = figure(
  alt: "Log-log plot of perpendicular diffusion D_perp divided by the unmagnetized coefficient D_s versus magnetization |Omega_s|/nu_s from 0.01 to 1000. The curve is flat at one for weak magnetization and falls with slope minus two, as (nu_s/Omega_s) squared, beyond |Omega_s| = nu_s. A marked point at |Omega_s|/nu_s = 176 shows the worked electron example, about 3e-5.",
  caption: [
    Gyration suppresses diffusion across $bold(B)$:
    $D_(s,perp)\/D_s=1\/(1+(Omega_s\/nu_s)^2)$ with
    $D_s=k_B T_s\/(m_s nu_s)$, the unmagnetized and parallel coefficient.
    Beyond $abs(Omega_s)=nu_s$ it falls as $(nu_s\/Omega_s)^2$. The point is
    the electron example below, $D_perp\/D_parallel=3.23 times 10^(-5)$.
  ],
)[
  #derived-plot("cross-field-diffusion", width: 10cm)
]

#let diffusion-scalings = figure(
  alt: "Two log-log panels on identical axes: perpendicular diffusion coefficient in square metres per second versus magnetic field from 1 mT to 1 T for the worked-example plasma. Left: the classical collisional coefficient (blue, solid) falls as 1/B squared and is 3.20e-3 at 10 mT. Right: the empirical Bohm estimate (orange, dashed) falls as 1/B and is 62.5 at 10 mT.",
  caption: [
    Classical (left) and Bohm (right) cross-field diffusion on the same axes
    for the plasma of the example below: $n=10^16$ #unit("m^-3"),
    $k_B T_e=k_B T_i=10$ #unit("eV"), $sigma=10^5$ #unit("S/m"). At
    $B=10$ #unit("mT") (dots) the empirical Bohm estimate exceeds the
    classical value by $1.95 times 10^4$, and the gap grows in proportion
    to $B$.
  ],
)[
  #derived-plot-pair("diffusion-classical", "diffusion-bohm")
]

#let wave-linearization = context {
  let alt-description = "A wave-model map starts with a homogeneous equilibrium, adds small perturbations, applies the plane-wave derivative rules, and ends with a linear algebra system whose determinant selects the allowed mode."
  let caption-text = [
    Wave analysis is a sequence of model choices: equilibrium, perturbation
    ordering, Fourier representation, and a nontrivial-amplitude condition.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (2.1cm, 1.2cm),
        ..concept-style,
        node((0, 0), [Equilibrium \
          $n_0, bold(u)_0, bold(E)_0, bold(B)_0$]),
        node((-1.35, 1), [Small perturbations \
          $epsilon A_1$]),
        node((1.35, 1), [Plane wave \
          $exp(i (bold(k) dot bold(r)-omega t))$]),
        node((0, 2), [Linear algebra \
          $M(omega,bold(k)) A=0$]),
        node((0, 3), [Dispersion relation \
          $det M=0$]),
        edge((0, 0), (-1.35, 1), [ordering], "->"),
        edge((0, 0), (1.35, 1), [Fourier], "->"),
        edge((-1.35, 1), (0, 2), [linearize], "->"),
        edge((1.35, 1), (0, 2), [replace derivatives], "->"),
        edge((0, 2), (0, 3), [nonzero amplitude], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram collision-diagram",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Equilibrium]
          #html.span[$n_0, bold(u)_0, bold(E)_0, bold(B)_0$]
        ]
        #html.div(class: "mhd-arrow")[add small perturbations]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Ordering]
            #html.span[$epsilon A_1$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Fourier form]
            #html.span[$exp(i (bold(k) dot bold(r)-omega t))$]
          ]
        ]
        #html.div(class: "mhd-arrow")[linearize and replace derivatives]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Linear algebra]
          #html.span[$M(omega,bold(k)) A=0$]
        ]
        #html.div(class: "mhd-arrow")[nonzero amplitude]
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Dispersion relation]
          #html.span[$det M=0$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

// Plot: wave-dispersion cell in derivations/chapters/ch12_introduction_waves.py.
#let wave-dispersion = figure(
  alt: "A normalized dispersion plot of frequency over electron plasma frequency against wave number times c over plasma frequency. The cold electromagnetic branch starts at the cutoff hat(omega)=1 for K=0 and approaches the dotted vacuum line hat(omega)=K; the cold electrostatic branch is the horizontal line hat(omega)=1.",
  caption: [
    Cold, unmagnetized, fixed-ion branches. The electromagnetic branch
    $hat(omega)^2=1+K^2$ has its cutoff at $hat(omega)=1$ and approaches the vacuum line
    $hat(omega)=K$; the electrostatic oscillation $hat(omega)=1$ has zero group velocity.
  ],
)[#derived-plot("wave-dispersion", width: 9.5cm)]

#let warm-kinetic-limits = context {
  let alt-description = "A model-limit ladder starts with a cold fluid response, adds pressure to obtain a warm-fluid branch, and then resolves particle velocities with a kinetic response. Each step adds physics and changes which damping and dispersion effects can be represented."
  let caption-text = [
    Cold fluid, warm fluid, and kinetic descriptions are nested model
    choices. Pressure introduces wavelength dependence; kinetic response
    additionally resolves resonant particles and phase mixing.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (2.1cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Cold fluid \
          no pressure]),
        node((0, 1), [Warm fluid \
          $c_s^2=gamma_s k_B T_s\/m_s$]),
        node((0, 2), [Kinetic response \
          $Z(zeta_s)$]),
        edge((0, 0), (0, 1), [pressure closure], "->"),
        edge((0, 1), (0, 2), [resonant particles], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram collision-diagram",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Cold fluid]
          #html.span[no pressure response]
        ]
        #html.div(class: "mhd-arrow")[add pressure closure]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Warm fluid]
          #html.span[$c_s^2=gamma_s k_B T_s\/m_s$]
        ]
        #html.div(class: "mhd-arrow")[resolve velocity space]
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Kinetic response]
          #html.span[$Z(zeta_s)$, resonances and phase mixing]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let magnetized-dielectric = context {
  let alt-description = "A response map starts with the cold-fluid momentum equation in a uniform background magnetic field. The transverse electric components are coupled by the signed cyclotron response, the parallel component remains separate, and the resulting three-by-three dielectric tensor feeds Maxwell's wave equation."
  let caption-text = [
    A uniform magnetic field makes the cold plasma dielectric response
    anisotropic. The transverse pair is coupled through the cyclotron term,
    while the field component parallel to the background field has its own
    plasma response.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (2.1cm, 1.2cm),
        ..concept-style,
        node((0, 0), [Cold momentum \
          $-i omega m_(s) bold(u)_(s)=q_(s)(bold(E)+bold(u)_(s) times bold(B)_(0))$]),
        node((-1.35, 1), [Transverse response \
          $epsilon_(perp), epsilon_(times)$]),
        node((1.35, 1), [Parallel response \
          $epsilon_(parallel)$]),
        node((0, 2), [Dielectric tensor \
          $bold(epsilon)_p$]),
        node((0, 3), [Wave matrix \
          $bold(M)(omega,bold(k)) bold(E)=0$]),
        edge((0, 0), (-1.35, 1), [couple $x,y$], "->"),
        edge((0, 0), (1.35, 1), [separate $z$], "->"),
        edge((-1.35, 1), (0, 2), [assemble], "->"),
        edge((1.35, 1), (0, 2), [assemble], "->"),
        edge((0, 2), (0, 3), [Maxwell], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram collision-diagram",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Cold momentum]
          #html.span[$-i omega m_(s) bold(u)_(s)=q_(s)(bold(E)+bold(u)_(s) times bold(B)_(0))$]
        ]
        #html.div(class: "mhd-arrow")[split by direction]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Transverse response]
            #html.span[$epsilon_(perp), epsilon_(times)$ couple $E_x,E_y$]
          ]
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Parallel response]
            #html.span[$epsilon_(parallel)$ acts on $E_z$]
          ]
        ]
        #html.div(class: "mhd-arrow")[assemble the tensor]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Dielectric tensor]
          #html.span[$bold(epsilon)_p$]
        ]
        #html.div(class: "mhd-arrow")[insert into Maxwell]
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Wave matrix]
          #html.span[$bold(M)(omega,bold(k)) bold(E)=0$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

// Plot: magnetized-parallel-dispersion cell in derivations/chapters/ch13_cold_magnetized_waves.py.
#let magnetized-parallel-dispersion = figure(
  alt: "Cold parallel dispersion, normalized frequency hat(omega) against K=kc/omega_pe at Y=0.3. The s=+1 branch starts at the cutoff hat(omega)=0.861, the s=-1 branch at hat(omega)=1.161; both approach the dotted vacuum line hat(omega)=K. Below the electron cyclotron resonance hat(omega)=0.3 the s=-1 whistler branch rises from zero and flattens toward the resonance.",
  caption: [
    Cold fixed-ion parallel propagation at
    #normalized-label[$Y=omega_(c,e)\/omega_(p,e)=0.3$], from
    $N_s^2=1-1/(hat(omega)(hat(omega)+s Y))$ with $K=hat(omega) N_s$. The two circular modes have
    different cutoffs $W_"cut,s"=(sqrt(Y^2+4)-s Y)/2$ (dots); only $s=-1$
    has the cyclotron resonance $hat(omega)=Y$, below which it propagates as the
    whistler.
  ],
)[#derived-plot("magnetized-parallel-dispersion", width: 9.5cm)]

#let magnetized-oblique-geometry = context {
  let alt-description = "A coordinate geometry diagram places the uniform background magnetic field along the z axis. The wave vector lies in the x-z plane, its z component is parallel to the field, its x component is perpendicular to the field, and the angle theta is measured between the wave vector and the magnetic field."
  let caption-text = [
    Oblique propagation is represented by $bold(k)=k (sin theta bold(e)_x+cos theta bold(e)_z)$,
    with $bold(B)_0$ along $z$. The angle is a model parameter: $theta=0$ is
    parallel propagation and $theta=pi\/2$ is perpendicular propagation.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.8cm, 1.25cm),
        ..concept-style,
        node((0, 0), [Uniform field \
          $bold(B)_0=B_0 bold(e)_z$]),
        node((-1.1, 1), [Parallel \
          $k_parallel=k cos theta$]),
        node((1.1, 1), [Perpendicular \
          $k_perp=k sin theta$]),
        node((0, 2), [Oblique wave vector \
          $bold(k)$ in the $x z$ plane]),
        node((0, 3), [Two coupled electromagnetic branches]),
        edge((0, 0), (-1.1, 1), [project], "->"),
        edge((0, 0), (1.1, 1), [project], "->"),
        edge((-1.1, 1), (0, 2), [retain], "->"),
        edge((1.1, 1), (0, 2), [retain], "->"),
        edge((0, 2), (0, 3), [determinant], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram collision-diagram",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Uniform field]
          #html.span[$bold(B)_0=B_0 bold(e)_z$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Parallel component]
            #html.span[$k_parallel=k cos theta$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Perpendicular component]
            #html.span[$k_perp=k sin theta$]
          ]
        ]
        #html.div(class: "mhd-arrow")[combine in the $x z$ plane]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Oblique wave vector]
          #html.span[$bold(k)=k(sin theta bold(e)_x+cos theta bold(e)_z)$]
        ]
        #html.div(class: "mhd-arrow")[solve the determinant]
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Two coupled branches]
          #html.span[polarization and refractive index depend on $theta$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

// Plots: perpendicular-o-mode and perpendicular-x-mode in derivations/chapters/ch13_cold_magnetized_waves.py.
#let magnetized-cutoff-map = figure(
  alt: "Two panels on identical axes, perpendicular propagation at Y=0.3: squared refractive index N^2 against hat(omega)=omega/omega_pe. Left, the ordinary mode (dashed). Right, the extraordinary mode (solid). The ordinary mode crosses zero at its cutoff hat(omega)=1. The extraordinary mode crosses zero at hat(omega)=0.861, diverges at the upper-hybrid resonance hat(omega)=1.044, returns from minus infinity and crosses zero again at hat(omega)=1.161. The shaded region N^2<0 is evanescent.",
  caption: [
    Perpendicular cold modes, ordinary (left) and extraordinary (right), at
    #normalized-label[$Y=omega_(c,e)\/omega_(p,e)=0.3$], the values of the
    following example. Cutoffs are zeros of $N^2$ (dots), the upper-hybrid
    resonance is a pole of $N_X^2$; between a resonance and the next cutoff
    the extraordinary mode is evanescent (shaded, $N^2<0$).
  ],
)[#derived-plot-pair("perpendicular-o-mode", "perpendicular-x-mode")]

#let collisional-wave-response = context {
  let alt-description = "A response map starts with the collisionless cold-plasma dielectric response. Adding a collision frequency makes the effective mass complex, which makes the refractive index and wave number complex; the real part controls phase advance and the positive imaginary part produces spatial attenuation in the chosen Fourier convention."
  let caption-text = [
    For a propagating cold branch, collisions introduce absorption into a lossless response. The lossless tensor is Hermitian away from poles; its entries need not all be real. Stopbands can have imaginary wave number even without collisions. The
    real wave number controls phase advance; the imaginary part controls
    attenuation with the stated Fourier convention.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.85cm, 1.2cm),
        ..concept-style,
        node((0, 0), [Cold response \
          $nu=0$, propagating: real $N$]),
        node((-1.1, 1), [Effective mass \
          $m_"eff"=m(1+i nu\/omega)$]),
        node((1.1, 1), [Complex response \
          $N=N_r+i N_i$]),
        node((0, 2), [Phase + attenuation \
          $exp(i k_r z-k_i z)$]),
        edge((0, 0), (-1.1, 1), [add drag], "->"),
        edge((0, 0), (1.1, 1), [complexify], "->"),
        edge((-1.1, 1), (0, 2), [insert in wave law], "->"),
        edge((1.1, 1), (0, 2), [interpret $k_i$], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram collision-diagram",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Cold response]
          #html.span[$nu=0$; real $N$ on propagating branches]
        ]
        #html.div(class: "mhd-arrow")[add collisional drag]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Complex effective mass]
            #html.span[$m_"eff"=m(1+i nu\/omega)$]
          ]
          #html.div(class: "mhd-node mhd-node-hall")[
            #html.strong[Complex wave number]
            #html.span[$N=N_r+i N_i$]
          ]
        ]
        #html.div(class: "mhd-arrow")[phase advance + attenuation]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Spatial field]
          #html.span[$exp(i k_r z-k_i z)$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

// Plot: ion-wave-branches cell in derivations/chapters/ch14_finite_temperature_waves.py.
#let ion-wave-branches = figure(
  alt: "Normalized cold two-fluid parallel dispersion, hat(omega)=omega/omega_ci against K=k v_A/omega_ci. Both circular branches start along the dotted Alfvén line hat(omega)=K. The RH whistler branch bends above it; the LH branch bends below and approaches the ion cyclotron resonance hat(omega)=1.",
  caption: [
    Cold parallel two-fluid branches for $omega << omega_(c,e)$ and
    $v_A << c$, with $K=k v_A\/omega_(c,i)$ and $hat(omega)=omega\/omega_(c,i)$:
    $W_"RH"=(K^2+sqrt(K^4+4 K^2))/2$ and
    $W_"LH"=(sqrt(K^4+4 K^2)-K^2)/2$. Both start as Alfvén waves; LH
    stops at the ion cyclotron resonance, RH continues as the whistler.
  ],
)[#derived-plot("ion-wave-branches", width: 9.5cm)]

// Plots: warm-langmuir-branch and ion-acoustic-branch in derivations/chapters/ch14_finite_temperature_waves.py.
#let warm-longitudinal-modes = figure(
  alt: "Two panels, both roots of the two-species warm-fluid longitudinal dispersion relation against K=k lambda_De. Left, the electron plasma wave in units of omega_pe: it starts at 1 and approaches the dotted thermal line omega=k c_se. Right, the ion-acoustic branch in units of omega_pi: it rises along the dotted line omega=k c_s and levels off at the ion plasma frequency, marked by a horizontal line.",
  caption: [
    The two roots of the warm two-species longitudinal relation for
    isothermal electrons ($gamma_e=1$), cold ions and $m_i\/m_e=1836$, with
    $K=k lambda_(D,e)$. Left, the electron plasma wave in units of
    $omega_(p,e)$ follows $omega^2 approx omega_(p,e)^2(1+K^2)$. Right, the
    ion-acoustic branch in units of $omega_(p,i)$ rises as $omega approx k c_s$
    and saturates at $omega_(p,i)$ for $K >> 1$, where the fluid closure is
    no longer controlled. The two frequency scales differ by
    $sqrt(m_i\/m_e) approx 43$.
  ],
)[#derived-plot-pair("warm-langmuir-branch", "ion-acoustic-branch")]

#let mhd-wave-speeds = context {
  let alt-description = "A warm MHD wave map combines magnetic pressure and thermal pressure for perpendicular compression. Magnetic tension instead restores parallel shear-Alfvén waves. For perpendicular compression the pressure terms combine to give the magnetosonic speed v_m equal to the square root of v_A squared plus v_s squared."
  let caption-text = [
    In the warm MHD limit, magnetic tension restores parallel shear-Alfvén waves. For perpendicular
    compression, magnetic pressure and thermal pressure combine to give
    $v_m=sqrt(v_A^2+v_s^2)$.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.55cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Warm MHD \
          pressure + magnetic field]),
        node((-1.35, 1), [Magnetic pressure \
          $v_A^2=B_0^2\/(mu_0 rho_0)$]),
        node((1.35, 1), [Pressure \
          $v_s^2=gamma p_0\/rho_0$]),
        node((0, 2), [Compression \
          $v_m^2=v_A^2+v_s^2$]),
        edge((0, 0), (-1.35, 1), [field restoring], "->"),
        edge((0, 0), (1.35, 1), [thermal restoring], "->"),
        edge((-1.35, 1), (0, 2), [perpendicular], "->"),
        edge((1.35, 1), (0, 2), [perpendicular], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram collision-diagram",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Warm MHD]
          #html.span[pressure + magnetic field]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-hall")[
            #html.strong[Magnetic pressure]
            #html.span[$v_A^2=B_0^2\/(mu_0 rho_0)$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Thermal pressure]
            #html.span[$v_s^2=gamma p_0\/rho_0$]
          ]
        ]
        #html.div(class: "mhd-arrow")[combine for perpendicular compression]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Magnetosonic speed]
          #html.span[$v_m=sqrt(v_A^2+v_s^2)$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let warm-wave-ordering = context {
  let alt-description = "An ordering map starts from the cold magnetized wave model and branches according to the largest neglected effect: a collision frequency comparable to the wave frequency gives complex damping, ion inertia important below the ion cyclotron scale gives two-fluid or MHD branches, and a Debye-scale wave number or thermal pressure gives warm dispersion. If none is small, the model must be kinetic."
  let caption-text = [
    Model selection is controlled by normalized orderings with unit #text("[1]"). Compare
    $nu\/omega$, $omega\/omega_(c,i)$, and $k lambda_D$ before interpreting a
    cold-plasma branch.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.3cm, 1.35cm),
        ..concept-style,
        node((0, 0), [Cold magnetized wave]),
        node((-1.45, 1), [Collisions \
          #normalized-label[$nu \/ omega$] not small]),
        node((0, 1), [Ion inertia \
          #normalized-label[$omega \/ omega_(c,i)$] small]),
        node((1.45, 1), [Thermal pressure \
          #normalized-label[$k lambda_D$] not small]),
        node((0, 2), [Complex, two-fluid, or warm response]),
        node((0, 3), [Kinetic treatment if scales overlap]),
        edge((0, 0), (-1.45, 1), [drag], "->"),
        edge((0, 0), (0, 1), [mobile ions], "->"),
        edge((0, 0), (1.45, 1), [pressure], "->"),
        edge((-1.45, 1), (0, 2), [attenuation], "->"),
        edge((0, 1), (0, 2), [MHD branches], "->"),
        edge((1.45, 1), (0, 2), [warm dispersion], "->"),
        edge((0, 2), (0, 3), [check ordering], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram collision-diagram",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Cold magnetized wave]
          #html.span[begin with the cold branch]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Collisions]
            #html.span[#normalized-label[$nu \/ omega$] not small → complex damping]
          ]
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Ion inertia]
            #html.span[#normalized-label[$omega \/ omega_(c,i)$] small → two-fluid/MHD]
          ]
          #html.div(class: "mhd-node mhd-node-hall")[
            #html.strong[Thermal pressure]
            #html.span[#normalized-label[$k lambda_D$] not small → warm dispersion]
          ]
        ]
        #html.div(class: "mhd-arrow")[if scales overlap: use kinetic response]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

// Plots: hot-isotropic-dispersion and hot-isotropic-damping in derivations/chapters/ch15_hot_plasma_waves.py.
#let hot-isotropic-dispersion = figure(
  alt: "Two side-by-side panels against a=k lambda_De from 0.12 to 0.6. Left: real frequency of the exact Maxwellian Langmuir root and the Bohm-Gross asymptote; they agree for small a and separate beyond about 0.25. Right: damping rate of the exact root and the weak-damping asymptote; both are negligible below a of about 0.2, the asymptote overestimates near 0.3 and saturates, while the exact rate keeps growing.",
  caption: [
    Exact complex root $omega=omega_r+i gamma$ (real part left, damping rate right) of
    $epsilon_L=1+(1+zeta Z(zeta))\/a^2=0$ for one electron Maxwellian,
    $a=k lambda_(D,e)$, against the asymptotes
    $omega_r\/omega_(p,e)=sqrt(1+3a^2)$ and
    $gamma/omega_(p,e)=-sqrt(pi\/8) a^(-3) exp(-1\/(2a^2)-3\/2)$.
    The asymptotes hold for $a lt.tilde 0.25$; beyond, the wave is
    strongly damped and only the full root is meaningful.
  ],
)[#derived-plot-pair("hot-isotropic-dispersion", "hot-isotropic-damping")]

#let hot-velocity-space-slopes = context {
  let alt-description = "A normalized velocity-space plot compares a Maxwellian distribution, which decreases through a marked positive phase velocity, with a bump-on-tail distribution that has a positive slope near the same region. A negative slope supports Landau damping; a positive slope can support wave growth."
  let caption-text = [
    One-dimensional velocity marginals, with $xi=v\/v_"th"$,
    $v_"th"=sqrt(2 k_B T_e\/m_e)$ and $F_"ref"=n_0\/(sqrt(pi) v_"th")$.
    The Maxwellian is $F\/F_"ref"=exp(-xi^2)$; the equal-density
    mixture is $0.9 exp(-xi^2)+0.2 exp(-4(xi-2)^2)$.
    At the marked $v_phi\/v_"th"=1.7$, near the steepest positive slope of
    the mixture, their slopes have opposite signs.
    A positive slope can supply growth; a full dispersion calculation is
    still needed. Both axes use unit #text("[1]").
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xlabel: normalized-axis[$v \/ v_"th"$],
      ylabel: normalized-axis[$F \/ F_"ref"$],
      lq.plot((1.7, 1.7), (0, 1), color: plot-gray, mark: none,
        stroke: (thickness: 0.6pt, dash: "dotted")),
      ..curve(samples(-3, 4, n: 140), v => model.maxwellian(v)),
      ..curve(samples(-3, 4, n: 140), model.bump, color: plot-orange, dash: "dashed"),
      tag(-0.8, model.maxwellian(-0.8), align: right)[Maxwellian],
      tag(2.25, model.bump(2.0), color: plot-orange, align: left)[bump on tail],
      tag(1.7, 0.9, color: plot-gray, align: left)[#normalized-label[$v_phi \/ v_"th"=1.7$]],
    )
  ]

}

// Plot: two-stream-growth cell in derivations/chapters/ch15_hot_plasma_waves.py.
#let two-stream-growth = figure(
  alt: "Two-stream growth rate gamma/omega_p against K=|k v_0|/omega_p. The rate rises from zero, peaks at 1/(2 sqrt 2) for K=sqrt(3/8) (marked), and falls to zero at the band edge K=1; larger K is stable.",
  caption: [
    Cold symmetric equal-density electron beams with immobile ions;
    $omega_p$ uses the total electron density and $K=abs(k v_0)\/omega_p$.
    The unstable root gives
    $gamma/omega_p=sqrt((sqrt(1+8 K^2)-1-2 K^2)/2)$ for $0<K<1$,
    with the maximum $1\/(2 sqrt(2))$ at $K=sqrt(3\/8)$.
  ],
)[#derived-plot("two-stream-growth", width: 9.5cm)]

#let hot-magnetized-resonance = context {
  let alt-description = "A hot magnetized response map begins with a gyrotropic equilibrium distribution, expands the perturbed distribution into cyclotron harmonics, and ends at Doppler-shifted Landau and cyclotron resonances. The resonant denominator is omega minus k parallel v parallel minus harmonic number times the signed gyrofrequency."
  let caption-text = [
    In a hot magnetized plasma, particle orbits create a family of resonances:
    parallel Landau resonance for harmonic zero and cyclotron resonances for
    nonzero harmonic number. The branch can be damped or driven by the local
    velocity-space gradients.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.8cm, 1.1cm),
        ..concept-style,
        node((0, 0), [Gyrotropic equilibrium \
          $f_(0)(v_parallel, v_perp)$]),
        node((-1.4, 1), [Orbit harmonics \
          $n=0, ±1, ±2, ...$]),
        node((1.4, 1), [Doppler shift \
          $omega-k_parallel v_parallel$]),
        node((0, 2), [Resonance \
          $omega-k_parallel v_parallel-n Omega_s=0$]),
        node((0, 3), [Damping or growth \
          velocity-space gradients]),
        edge((0, 0), (-1.4, 1), [Fourier harmonics], "->"),
        edge((0, 0), (1.4, 1), [parallel motion], "->"),
        edge((-1.4, 1), (0, 2), [cyclotron phase], "->"),
        edge((1.4, 1), (0, 2), [Landau phase], "->"),
        edge((0, 2), (0, 3), [contour prescription], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram collision-diagram",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Gyrotropic $f_0$]
          #html.span[depends on $v_parallel$ and $v_perp$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Landau]
            #html.span[$n=0$: $omega-k_parallel v_parallel=0$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Cyclotron]
            #html.span[$n != 0$: orbit harmonics]
          ]
        ]
        #html.div(class: "mhd-arrow")[the sign of the distribution gradient selects damping or growth]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let sheath-structure = context {
  let alt-description = "A boundary-layer map runs from quasineutral plasma through a presheath and a Debye-scale charge-separated sheath to a material wall. Ions are accelerated toward the wall, electrons are selectively repelled, and the sheath-edge condition is constrained by the Bohm criterion."
  let caption-text = [
    A planar boundary is organized into a quasineutral plasma, a
    presheath that supplies directed ion flow, a charge-separated sheath of
    order a few Debye lengths, and the material wall. The labels describe
    model regions.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (2.2cm, 0.95cm),
        ..concept-style,
        node((0, 0), [Quasineutral plasma \
          $n_(e) approx n_(i)$]),
        node((0, 1), [Presheath \
          directed ion flow]),
        node((0, 2), [Sheath \
          width approximately a few $lambda_D$]),
        node((0, 3), [Material wall \
          $phi_"wall"<phi_"pl"$]),
        edge((0, 0), (0, 1), [ion acceleration], "->"),
        edge((0, 1), (0, 2), [Bohm entry], "->"),
        edge((0, 2), (0, 3), [particle collection], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram collision-diagram",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Quasineutral plasma]
          #html.span[$n_e$ approximately equals $n_i$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Presheath]
            #html.span[ions acquire directed flow]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Debye-scale sheath]
            #html.span[charge separation and electron filtering]
          ]
        ]
        #html.div(class: "mhd-arrow")[material wall collects particles]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

// Plots: sheath-potential and sheath-densities in derivations/chapters/ch16_sheaths_probes.py.
#let sheath-profile = figure(
  alt: "Self-consistent planar sheath against distance from the wall in Debye lengths, two panels. Left: the normalized potential drop eta falls from the hydrogen floating value 2.84 at the wall toward zero in the plasma. Right: the ion density stays above the electron density everywhere; both rise toward n_0 away from the wall, the electrons from about 0.06 and the ions from about 0.39.",
  caption: [
    Potential (left) and densities (right) from the Poisson solution of the sheath equation
    $eta''=M/sqrt(M^2+2 eta)-exp(-eta)$ for ions entering at the Bohm speed
    ($M=1$), integrated from a hydrogen wall at the floating potential
    $eta_w=-ln sqrt(2 pi m_e\/m_i)=2.84$, with
    $eta=-e phi\/(k_B T_e)$ and $x$ measured from the wall. Boltzmann
    electrons $n_e\/n_0=exp(-eta)$ are depleted faster than the cold ions
    $n_i/n_0=M/sqrt(M^2+2 eta)$, so the sheath carries positive space charge.
  ],
)[#derived-plot-pair("sheath-potential", "sheath-densities")]

// Plot: probe-iv-characteristic cell in derivations/chapters/ch16_sheaths_probes.py.
#let probe-iv-characteristic = figure(
  alt: "Normalized planar Langmuir-probe current against bias u. A small positive ion-saturation plateau at strongly negative bias, a zero crossing at the floating value u_f=-2.84 (marked), an exponential electron-retardation rise in magnitude, and a flat electron-saturation level -1 above the plasma potential u=0.",
  caption: [
    Idealized planar probe, ion current positive:
    $I/(e Gamma_(e,0) A)=Gamma_i/Gamma_(e,0)-exp(u)$ for $u<=0$ and
    electron saturation for $u>0$, with $u=(e(phi_p-phi_"pl"))/(k_B T_e)$.
    For hydrogen $Gamma_i/Gamma_(e,0)=sqrt((2 pi m_e)/m_i)=0.0585$, so the
    current vanishes at $u_f=-2.84$. The exponential retardation branch
    carries the temperature diagnostic; real saturation depends on geometry.
  ],
)[#derived-plot("probe-iv-characteristic", width: 9.5cm)]

// Chapter 1 plots: cells in derivations/chapters/ch01_introduction.py.
#let intro-enclosed-charge = figure(
  alt: "Net charge inside a sphere of radius r around a point charge, divided by the charge, against r over the Debye length. The bare value is a dashed horizontal line at one. The screened curve starts at one and falls smoothly, to about 0.74 at one Debye length and 0.2 at three Debye lengths.",
  caption: [
    Net charge inside radius $r$ around a point charge $Q$: bare (dashed)
    and Debye-screened (solid), $Q_"enc"\/Q = (1 + r\/lambda_D) e^(-r\/lambda_D)$
    from Gauss's law and the screened potential derived in the Debye-shielding
    chapter. Radius in units of $lambda_D$.
  ],
)[#derived-plot("enclosed_charge")]

#let intro-heating-drift = figure(
  alt: "Two plots on identical axes of one velocity component of a Maxwellian. Left, heating: the solid curve at temperature T and a dashed curve at 4T, both centred at zero; the hotter one is twice as wide and half as high. Right, acceleration: the solid curve at rest and a dashed curve of the same shape shifted to two thermal speeds.",
  caption: [
    One velocity component of a Maxwellian with the same density. Left:
    heating from $T$ to $4T$ doubles the width $v_"th"$ at fixed bulk
    velocity. Right: acceleration to $u = 2 v_"th"$ shifts the distribution
    at fixed width. Velocity in units of the initial $v_"th"$, $f$ in units
    of $n\/v_"th"$.
  ],
)[#derived-plot-pair("maxwellian_heating", "maxwellian_drift")]

#let intro-speed-distribution = figure(
  alt: "Distribution of particle speeds in an isotropic Maxwellian against v over the thermal speed. The curve rises from zero, peaks at v equal to v_th and decays. Vertical lines mark v_th at the peak, the mean speed at 1.13 v_th and the root-mean-square speed at 1.22 v_th.",
  caption: [
    Speed distribution $F(v)$ of an isotropic Maxwellian,
    $integral_0^oo F dif v = 1$. The thermal speed $v_"th"$ is the most
    probable speed; the mean speed is $2 v_"th"\/sqrt(pi)$ and the
    root-mean-square speed $sqrt(3\/2) v_"th"$. Speed in units of $v_"th"$.
  ],
)[#derived-plot("maxwell_speed")]

#let intro-thermal-speed = figure(
  alt: "Log-log plot of thermal speed in metres per second against k_B T in electron-volts from 0.01 eV to 10 keV, with the temperature in kelvin on the top axis. Two parallel lines of slope one half: electrons from about 6 times 10 to the 4 to 6 times 10 to the 7 metres per second, and protons a factor 43 lower.",
  caption: [
    Thermal speed $v_"th" = sqrt(2 k_B T\/m)$ of electrons (solid) and
    protons (dashed) against $k_B T$ in #unit("eV"); top axis: $T$ in
    #unit("K"), $1 #unit("eV") \/ k_B approx 1.16 dot 10^4 #unit("K")$. Both
    lines have slope $1\/2$; their ratio is $sqrt(m_p\/m_e) approx 43$.
    Nonrelativistic.
  ],
)[#derived-plot("thermal_speed")]

#let intro-scale-ordering = figure(
  alt: "Two panels with one row per example plasma: H II region, ionosphere, solar corona, Hall thruster and tokamak core. Left, lengths in metres on a logarithmic axis from a micrometre to 10 to the 18 metres: Debye length (circle), electron gyroradius (triangle), Coulomb mean free path (square) and system size (bar). Right, rates in inverse seconds: electron plasma frequency (circle), electron cyclotron frequency (triangle) and electron-ion collision frequency (square). In every row the Debye length lies far below the system size; the mean free path exceeds the system size in the tokamak core and the Hall thruster; the collision frequency lies far below the plasma frequency in every row.",
  caption: [
    Characteristic lengths (left) and rates (right) of five example
    plasmas: Debye length $lambda_D$, electron thermal gyroradius
    $rho_e = v_("th",e)\/omega_(c e)$, Coulomb mean free path
    $lambda_"mfp" = chevron.l v chevron.r\/nu_(e i)$, system size $L$; electron
    plasma and cyclotron frequencies $omega_(p e)$, $omega_(c e)$ and
    electron--ion collision frequency $nu_(e i)$. Order-of-magnitude
    $n_e$, $k_B T_e$, $B$ and $L$; the ionosphere's dominant
    electron--neutral collisions are not included.
  ],
)[#derived-plot("scale_ordering")]
