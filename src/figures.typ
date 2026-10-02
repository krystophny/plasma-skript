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
#let samples(lo, hi, n: 80) = range(n + 1).map(i => lo + (hi - lo) * i / n)
// Okabe–Ito blue and vermilion plus a neutral gray. Every curve also carries
// a distinct dash pattern and a direct label, so color is never the only cue.
#let plot-blue = rgb("#0072B2")
#let plot-orange = rgb("#D55E00")
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
// plot surface keeps their dark ink legible in both site color schemes.
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
  set text(font: "New Computer Modern", size: 11pt, fill: rgb("#1c1f23"))
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
  let alt-description = "A plasma-model hierarchy titled Plasma Models. Plasma phenomena branch to single-particle motion and a distribution function. The distribution function leads to the Boltzmann equation and then to moments of the Boltzmann equation, which branch to single-fluid MHD and multiple-fluid models. Annotations identify about 10^20 coupled particle ODEs, four Maxwell PDEs in 3+1 dimensions, a kinetic PDE in 6+1 dimensions, and the removal of velocity detail in the fluid description. A lower panel compares the illustrative grid costs of 3D and 6D descriptions using 100 points per coordinate and shows a two-dimensional position-velocity grid."
  let caption-text = [
    Plasma model hierarchy from coupled particle trajectories and Maxwell's
    equations to kinetic and fluid descriptions. Prescribed electromagnetic forces remain in the test-particle model. Each kinetic species equation is coupled to field equations. The counts are illustrative:
    100 points per coordinate gives $10^6$ points in 3D and $10^12$ points in
    6D; the memory hints assume one 8-byte scalar per point. This is the
    curse of dimensionality: at fixed resolution per coordinate, the size
    of a full grid grows exponentially with the number of coordinates.
    The schematic
    phase-space axes use SI position in #unit("m") and velocity in
    #unit("m/s").
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #align(center)[#text(size: 15pt, weight: "bold")[Plasma Models]]

      #grid(
        columns: (1fr, 1fr),
        gutter: 0.55cm,
        align(right)[
          #text(size: 9pt, weight: "bold", fill: accent)[Illustrative $10^20$ particles] \
          #text(size: 8pt, fill: muted)[one vector second-order equation per particle]
        ],
        align(left)[
          #text(size: 9pt, weight: "bold", fill: blue)[Maxwell: 4 field equations in 3+1D] \
          #text(size: 8pt, fill: muted)[vector/scalar equations, including constraints]
        ],
      )

      #grid(
        columns: (2.6cm, 1fr, 2.8cm),
        gutter: 0.35cm,
        align(center + horizon)[
          #v(0.55cm)
          #block(
            width: 100%,
            inset: 0.45em,
            radius: 0.3em,
            fill: accent-light,
            stroke: 0.8pt + accent,
          )[
            #text(size: 8.5pt, weight: "bold", fill: accent)[Neglect \
              interactions] \
            #text(size: 8pt)[test particle]
          ]
        ],
        [
          #scale(x: 70%, y: 70%, reflow: true)[
            #fletcher.diagram(
              spacing: (1.05cm, 1.15cm),
              node-stroke: 0.9pt,
              edge-stroke: 0.9pt,
              node((0, 0), [Plasma phenomena], name: <phenomena>),
              node((-1.55, 1), [Single-particle \
                motion], name: <single_particle>),
              node((1.15, 1), [Distribution \
                function], name: <distribution>),
              node((2.85, 1), [Boltzmann \
                equation], name: <boltzmann>),
              node((2.85, 2), [Moments of Boltzmann \
                equation], name: <moments>),
              node((1.85, 3), [Single fluid \
                (MHD)], name: <single_fluid>),
              node((3.95, 3), [Multiple fluids], name: <multiple_fluids>),
              edge(
                (<phenomena.south-west>, 45%, <phenomena.south-east>),
                (<single_particle.north-west>, 75%, <single_particle.north-east>),
                [test particle],
                "->",
                label-side: left,
              ),
              edge(
                (<phenomena.south-west>, 55%, <phenomena.south-east>),
                (<distribution.north-west>, 25%, <distribution.north-east>),
                [coarse grain],
                "->",
                label-side: right,
              ),
              edge(<distribution.east>, <boltzmann.west>, [kinetic PDE], "->", label-sep: 0.25em),
              edge(<boltzmann.south>, <moments.north>, [take moments], "->", label-sep: 0.25em),
              edge(
                (<moments.south-west>, 45%, <moments.south-east>),
                (<single_fluid.north-west>, 75%, <single_fluid.north-east>),
                [closure],
                "->",
                label-side: left,
              ),
              edge(
                (<moments.south-west>, 55%, <moments.south-east>),
                (<multiple_fluids.north-west>, 25%, <multiple_fluids.north-east>),
                [species moments],
                "->",
                label-side: right,
              ),
            )
          ]
        ],
        align(center + horizon)[
          #block(
            width: 100%,
            inset: 0.45em,
            radius: 0.3em,
            fill: rgb("#FFF3E5"),
            stroke: 0.8pt + orange,
          )[
            #text(size: 8.5pt, weight: "bold", fill: orange)[Coarse graining] \
            #text(size: 8pt)[1 kinetic PDE per species in 6+1D] \
            #text(size: 8pt)[$f(bold(x), bold(v), t)$] \
            #text(size: 8.5pt, weight: "bold", fill: orange)[kinetic]
          ]
        ],
      )

      #align(center)[
        #text(size: 8.5pt, weight: "bold", fill: blue)[Remove velocity detail $bold(v)$] \
        #text(size: 8pt, fill: muted)[fluid variables in 3+1D]
      ]

      #grid(
        columns: (1.55fr, 1fr),
        gutter: 0.55cm,
        [
          #block(
            width: 100%,
            inset: 0.55em,
            radius: 0.3em,
            fill: paper,
            stroke: 0.7pt + muted,
          )[
            #text(size: 8.5pt, weight: "bold")[Curse of dimensionality] \
            #text(size: 8pt)[100 grid points per coordinate] \
            #text(size: 8pt)[$3D$: $10^6$ points, about 8 MB] \
            #text(size: 8pt)[$6D$: $10^12$ points, about 8 TB]
          ]
        ],
        [
          #align(center)[
            #cetz.canvas({
              import cetz.draw: *
              line((0, 0), (4.1, 0), stroke: 1pt + ink)
              line((0, 0), (0, 2.4), stroke: 1pt + ink)
              line((0, 0.48), (4.1, 0.48), stroke: 0.55pt + muted)
              line((0, 0.96), (4.1, 0.96), stroke: 0.55pt + muted)
              line((0, 1.44), (4.1, 1.44), stroke: 0.55pt + muted)
              line((0, 1.92), (4.1, 1.92), stroke: 0.55pt + muted)
              line((0.82, 0), (0.82, 2.4), stroke: 0.55pt + muted)
              line((1.64, 0), (1.64, 2.4), stroke: 0.55pt + muted)
              line((2.46, 0), (2.46, 2.4), stroke: 0.55pt + muted)
              line((3.28, 0), (3.28, 2.4), stroke: 0.55pt + muted)
              content((4.25, -0.1), [x #text(size: 7pt)[(#unit("m") )]])
              content((-0.25, 2.55), [v #text(size: 7pt)[(#unit("m/s") )]])
              content((3.45, 2.55), [2D])
              content((1.55, -0.48), [$10^4$ points])
            })
          ]
        ],
      )
    ]
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
        coordinates, and time; 3+1D retains position and time. In SI,
        these coordinates are in #unit("m"), #unit("m/s"), and
        #unit("s"), respectively. ODE and PDE denote ordinary and partial
        differential equations.
      ]
    ]

    html.p[
      For an illustrative $N = 10^20$ particles (a count with unit [1]), the
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
        These estimates count one stored scalar, not the full solver.
        Multiple species, field components, time integration, and boundary
        data add storage. Coarser grids or other representations change
        the cost, but require their own accuracy checks.
      ]
    ]

  }
}

#let gyroradius-geometry = figure(
  alt: "A circular orbit in a uniform magnetic field. The orbit center is marked, the radius from the center to the particle is labelled gyroradius, and a straight arrow shows the perpendicular velocity at the particle.",
  caption: [
    Geometry of uniform-field gyromotion. The radius is the gyroradius
    $rho$ (a length in #unit("m")), and the tangent arrow represents the
    perpendicular velocity $bold(v)_perp$.
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
  }))
]

#let debye-profile = figure(
  alt: "A normalized planar sheet-source plot of screened electrostatic potential versus distance measured in Debye lengths. The potential is largest at zero distance and decreases symmetrically toward zero as the distance exceeds several Debye lengths.",
  caption: [
    Planar sheet-source screening, $phi/phi_0=exp(-abs(x)/lambda_D)$. This is not the spherical point-source Yukawa potential. Both axes use unit #text("[1]"): the
    distance is normalized by the electron Debye length $lambda_D$, and the
    potential is normalized by its value $phi_0$ at the source.
  ],
)[
  #plot-diagram(
    width: 10cm,
    height: 5.2cm,
    xlabel: normalized-axis[$x \/ lambda_D$],
    ylabel: normalized-axis[$phi \/ phi_0$],
    ..curve(samples(-4, 4, n: 160), x => calc.exp(-calc.abs(x))),
  )
]

#let debye-potential-comparison = figure(
  alt: "A normalized radial plot compares the potential of a finite uniformly charged sphere with and without Debye shielding. The bare potential follows a quadratic curve inside the sphere, joins a 1 over r Coulomb tail outside it, and remains above the screened curve. The Debye-screened curve is continuous at the sphere boundary and falls exponentially faster outside the source.",
  caption: [
    Linear Debye shielding for a permeable, uniformly charged sphere with
    $R/lambda_D = 0.5$. Both axes use unit #text("[1]"): the radius is
    normalized by the electron Debye length, and the potential by
    $Q/(4 pi epsilon_0 lambda_D)$ in SI. The dashed curve is the bare spherical source and the solid
    curve is the solution of the linearized spherical Debye--Hückel
    equation, including mobile plasma inside the source. Linearization requires $abs(e phi)/(k_B T_e) << 1$ throughout; normalization by $Q/(4 pi epsilon_0 lambda_D)$ alone does not guarantee this. The curves are normalized SI results.
  ],
)[
  #plot-diagram(
    width: 10cm,
    height: 5.6cm,
    xlabel: normalized-axis[$r \/ lambda_D$],
    ylabel: normalized-axis[$phi \/ (Q \/ (4 pi epsilon_0 lambda_D))$],
    ..curve(samples(0, 4, n: 160), r => model.sphere-bare(r),
      color: plot-orange, dash: "dashed"),
    ..curve(samples(0, 4, n: 160), r => model.sphere-screened(r)),
    tag(1.25, model.sphere-bare(1.25), color: plot-orange, align: left + bottom)[bare],
    tag(0.75, model.sphere-screened(0.75), align: left + bottom)[screened],
  )
]

#let maxwellian-profile = figure(
  alt: "A normalized one-dimensional velocity plot compares a centered Maxwellian distribution with a second Maxwellian shifted toward positive velocity. The centered curve peaks at zero velocity, while the shifted curve peaks at positive normalized velocity and has the same Gaussian width.",
  caption: [
    Centered and drifting one-dimensional Maxwellians. The horizontal axis is
    velocity normalized by $v_"th"=sqrt((2 k_B T)/m)$, and the vertical axis is
    distribution value normalized by the centered peak. Line style and direct
    labels distinguish the curves independently of color.
  ],
)[
  #plot-diagram(
    width: 10cm,
    height: 5.2cm,
    xlabel: normalized-axis[$v \/ v_"th"$],
    ylabel: normalized-axis[$f \/ f_0$],
    ..curve(samples(-3, 4, n: 140), x => model.maxwellian(x)),
    ..curve(samples(-3, 4, n: 140), x => model.maxwellian(x, drift: 1),
      color: plot-orange, dash: "dashed"),
    tag(-0.75, model.maxwellian(-0.75), align: right)[centered],
    tag(1.8, model.maxwellian(1.8, drift: 1), color: plot-orange)[drifting, #normalized-label[$u \/ v_"th"=1$]],
  )
]

#let collision-paths = figure(
  alt: "A conceptual comparison of two normalized particle paths. The neutral-gas path is a zigzag made of straight flights separated by a few marked hard collisions. The plasma path bends smoothly through many small deflections distributed along the flight, with no isolated hard-sphere event. The paths are illustrative, not measured trajectories.",
  caption: [
    Collision geometry in a neutral gas and a weakly coupled plasma. The
    horizontal distance and transverse displacement are normalized by the
    reference mean free path $lambda_"ref"$ and use unit #text("[1]").
    Dots mark the isolated hard collisions of the neutral path; the plasma
    path is a continuous curve with many small deflections, so the two
    interaction models are distinguished without relying on color.
  ],
)[
  #let neutral = ((0, 0), (1.3, 0.06), (2.2, 0.42), (3.4, -0.22), (4.6, -0.1), (5.8, 0.3))
  // Illustrative small-angle path: a slowly varying heading built from a few
  // incommensurate sines, integrated in steps of 0.05 [1].
  #let plasma = range(120).fold(((0, 0),), (acc, i) => {
    let th = 0.3*calc.sin(0.09*i) - 0.22*calc.sin(0.23*i + 0.5) + 0.04*calc.sin(2.7*i)
    let (x, y) = acc.last()
    acc + ((x + 0.05*calc.cos(th), y + 0.05*calc.sin(th)),)
  })
  #plot-diagram(
    width: 10cm,
    height: 5.2cm,
    ylim: (-0.45, 0.6),
    xlabel: normalized-axis[$ell \/ lambda_"ref"$],
    ylabel: normalized-axis[$y \/ lambda_"ref"$],
    lq.plot(neutral.map(p => p.first()), neutral.map(p => p.last()),
      color: plot-blue, mark: none, stroke: plot-stroke),
    lq.plot(neutral.slice(1, -1).map(p => p.first()), neutral.slice(1, -1).map(p => p.last()),
      color: plot-blue, stroke: none, mark: "o", mark-size: 4pt),
    lq.plot(plasma.map(p => p.first()), plasma.map(p => p.last()),
      color: plot-orange, mark: none, stroke: plot-stroke),
    tag(3.4, -0.22, align: left + top)[neutral gas: hard collisions],
    tag(3.5, 0.47, color: plot-orange, align: left)[plasma: many weak deflections],
  )
]

#let moment-hierarchy = figure(
  alt: "A hierarchy diagram starts with the full distribution function f of position and velocity and branches to progressively higher velocity moments: number density n, bulk velocity u, pressure tensor P, and heat flux q. Each lower-level description retains less velocity-space information and requires a closure for the next moment.",
  caption: [
    Velocity moments compress the distribution function into macroscopic
    fields. The hierarchy is not a sequence of unrelated equations: the
    transport law for one moment generally contains the next moment. Here
    $bold(w)=bold(v)-bold(u)$; heat flux contracts the third central tensor,
    which is needed in full for a general pressure-tensor evolution.
    Arrows denote equation dependencies, not recovery of higher moments.
  ],
)[
  #graphic(fletcher.diagram(
    spacing: (1.1cm, 1.3cm),
    ..concept-style,
    node((0, 0), [Distribution $f(t, bold(r), bold(v))$]),
    node((-2.2, 1), [0th moment \ $n$]),
    node((0, 1), [normalized 1st raw moment \ $bold(u)$]),
    node((2.2, 1), [2nd central moment \ $bold(P)$]),
    node((2.2, 2), [contracted 3rd central moment \ $bold(q)$]),
    edge((0, 0), (-2.2, 1), [integrate], "->"),
    edge((0, 0), (0, 1), [weight $bold(v)$], "->"),
    edge((0, 0), (2.2, 1), [weight $bold(w) bold(w)$], "->"),
    edge((2.2, 1), (2.2, 2), [higher transport], "->"),
  ))
]

#let multiple-fluid-hierarchy = context {
  let alt-description = "A schematic multiple-fluid hierarchy starts with one kinetic distribution for each species. The electron and ion distributions are separately reduced to electron and ion density, velocity, and pressure fields. Their coupled equations share electric and magnetic fields, and summing the species equations gives one-fluid variables only after the relative-flow stress is accounted for."
  let caption-text = [
    Species-resolved moments retain the relative motion of electrons and ions.
    The electromagnetic field couples the two fluid systems: each fluid
    supplies charge and current to Maxwell's equations and feels the Lorentz
    force of the shared field. A one-fluid
    description is obtained only after their sums and relative-flow terms are
    defined.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (2.6cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Kinetic species states \
          $f_(e), f_(i)$]),
        node((-1.7, 1), [Electron fluid \
          $n_(e), bold(u)_(e), bold(P)_(e)$]),
        node((1.7, 1), [Ion fluid \
          $n_(i), bold(u)_(i), bold(P)_(i)$]),
        node((0, 2), [Coupled fields \
          $bold(E), bold(B)$]),
        node((0, 3), [One-fluid sums \
          $rho, bold(u), bold(P), bold(j)$]),
        edge((0, 0), (-1.7, 1), [velocity moments], "->"),
        edge((0, 0), (1.7, 1), [velocity moments], "->"),
        edge((-1.7, 1), (0, 2), [sources, force], "<->"),
        edge((1.7, 1), (0, 2), [sources, force], "<->"),
        edge((0, 2), (0, 3), [sum and define], "->"),
      )
    ]
  } else {
    // Fletcher and CeTZ diagrams are intentionally replaced by a semantic
    // HTML fallback: the typed HTML target does not always emit their canvas.
    html.figure(class: "concept-figure")[
      #html.div(
        class: "hierarchy-fallback",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "hierarchy-node hierarchy-source")[
          #html.strong[Kinetic species states]
          #html.span[$f_(e), f_(i)$]
        ]
        #html.div(class: "hierarchy-arrow")[↓ velocity moments]
        #html.div(class: "hierarchy-branches")[
          #html.div(class: "hierarchy-node")[
            #html.strong[Electron fluid]
            #html.span[$n_(e), bold(u)_(e), bold(P)_(e)$]
          ]
          #html.div(class: "hierarchy-node")[
            #html.strong[Ion fluid]
            #html.span[$n_(i), bold(u)_(i), bold(P)_(i)$]
          ]
        ]
        #html.div(class: "hierarchy-arrow")[↕ charge and current sources; Lorentz force]
        #html.div(class: "hierarchy-node hierarchy-fields")[
          #html.strong[Coupled fields]
          #html.span[$bold(E), bold(B)$]
        ]
        #html.div(class: "hierarchy-arrow")[↓ sum and define]
        #html.div(class: "hierarchy-node hierarchy-sums")[
          #html.strong[One-fluid sums]
          #html.span[$rho, bold(u), bold(P), bold(j)$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let mhd-reduction = context {
  let alt-description = "A reduction map shows electron and ion fluid equations being combined into total mass and momentum balances, while their difference supplies a generalized Ohm law. Ordering and closure assumptions then reduce the system to single-fluid MHD."
  let caption-text = [
    Single-fluid MHD keeps the variables that survive a mass-weighted sum and
    records the species difference through Ohm's law. Every arrow is an
    approximation or definition that must be stated.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.35cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Electron + ion equations]),
        node((-1.45, 1), [Mass-weighted sum \
          $rho, bold(u), bold(P)$]),
        node((1.45, 1), [Species difference \
          $bold(E)+bold(u) times bold(B)$]),
        node((0, 2), [Single-fluid MHD \
          mass, momentum, induction]),
        edge((0, 0), (-1.45, 1), [sum], "->"),
        edge((0, 0), (1.45, 1), [subtract], "->"),
        edge((-1.45, 1), (0, 2), [closure], "->"),
        edge((1.45, 1), (0, 2), [ordering], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram mhd-reduction-fallback",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Electron + ion equations]
        ]
        #html.div(class: "mhd-arrow")[↙ weighted sum &nbsp; ↘ species difference]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node")[
            #html.strong[Mass-weighted sum]
            #html.span[$rho, bold(u), bold(P)$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Species difference]
            #html.span[$bold(E)+bold(u) times bold(B)$]
          ]
        ]
        #html.div(class: "mhd-arrow")[↓ closure and ordering]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Single-fluid MHD]
          #html.span[mass · momentum · induction]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let mhd-ohm-balance = context {
  let alt-description = "A generalized Ohm-law map places the ideal combination of electric field and bulk magnetic advection, E plus u cross B, at the top. Four arrows lead to the separate right-hand-side terms: resistive, Hall, electron-pressure, and electron-inertia."
  let caption-text = [
    Generalized Ohm's law is a balance of distinct physical effects. The
    simplified ideal form is obtained only after the retained corrections are
    compared with the chosen scales.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (0.55cm, 1.3cm),
        ..concept-style,
        node((0, 0), [Generalized Ohm law \
          $bold(E)+bold(u) times bold(B) = dots$]),
        node((-3, 1), [Resistive \ $eta bold(j)$]),
        node((-1, 1), [Hall \ $bold(j) times bold(B) \/ (e n c)$]),
        node((1, 1), [Electron pressure \ $-grad p_e \/ (e n)$]),
        node((3, 1), [Electron inertia \ $m_e \/ (e^2 n) thin partial_t bold(j)$]),
        edge((0, 0), (-3, 1), "->"),
        edge((0, 0), (-1, 1), "->"),
        edge((0, 0), (1, 1), "->"),
        edge((0, 0), (3, 1), "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram mhd-ohm-fallback",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Generalized Ohm law]
          #html.span[$bold(E)+bold(u) times bold(B)$]
        ]
        #html.div(class: "mhd-arrow")[four corrections are ordered separately]
        #html.div(class: "mhd-term-grid")[
          #html.div(class: "mhd-node mhd-node-hall")[
            #html.strong[Hall]
            #html.span[$bold(j) times bold(B) \/ (e n c)$]
          ]
          #html.div(class: "mhd-node")[
            #html.strong[Electron pressure]
            #html.span[$-grad p_e \/ (e n)$]
          ]
          #html.div(class: "mhd-node mhd-node-resistive")[
            #html.strong[Resistive]
            #html.span[$eta bold(j)$]
          ]
          #html.div(class: "mhd-node")[
            #html.strong[Electron inertia]
            #html.span[$m_e \/ (e^2 n) thin partial_t bold(j)$]
          ]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let mhd-flux-diffusion = context {
  let alt-description = "A transport map separates two regimes of the induction equation. At high magnetic Reynolds number, magnetic flux through a material loop is approximately constant on the chosen scales. With finite resistivity, a magnetic-diffusion term permits changes of field topology on a diffusion timescale."
  let caption-text = [
    The magnetic Reynolds number compares advection with diffusion. Ideal MHD
    transports field lines with the fluid; finite resistivity permits field-line
    slippage and diffusion.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.45cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Induction equation \
          $partial_t bold(B)=curl (bold(u) times bold(B))+D_B laplacian bold(B)$]),
        node((-1.35, 1), [Nearly ideal \
          $R_m >> 1$]),
        node((1.35, 1), [Finite resistivity \
          $D_B=eta \/ mu_0$]),
        node((-1.35, 2), [Approximately frozen flux \
          field lines move with $bold(u)$]),
        node((1.35, 2), [Diffusion \
          $tau_D=L^2 \/ D_B$]),
        edge((0, 0), (-1.35, 1), [advection dominates], "->"),
        edge((0, 0), (1.35, 1), [diffusion retained], "->"),
        edge((-1.35, 1), (-1.35, 2), [approximately conserved], "->"),
        edge((1.35, 1), (1.35, 2), [topology can change], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram mhd-flux-fallback",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Induction equation]
          #html.span[$pdv(bold(B),t)=curl (bold(u) times bold(B))+D_(B) laplacian bold(B)$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Nearly ideal: $R_m >> 1$]
            #html.span[Approximately frozen flux; field lines move with $bold(u)$]
          ]
          #html.div(class: "mhd-node mhd-node-diffusion")[
            #html.strong[Finite resistivity]
            #html.span[$D_B=eta \/ mu_0$; diffusion time $tau_D=L^2 \/ D_B$]
          ]
        ]
        #html.div(class: "mhd-arrow")[advection dominates ↔ diffusion permits topology changes]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let mhd-force-balance = context {
  let alt-description = "A static MHD force-balance diagram shows pressure-gradient force balanced by magnetic force density. The equilibrium condition is grad p equals j cross B, and both forces are perpendicular to the magnetic field."
  let caption-text = [
    Static MHD equilibrium is a local force balance. In a smooth isotropic
    plasma, pressure gradients are perpendicular to the field and are balanced
    by the magnetic force density.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.4cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Static MHD \
          $partial_t=0, bold(u)=bold(0)$]),
        node((-1.4, 1), [Pressure force \
          $-grad p$]),
        node((1.4, 1), [Magnetic force \
          $bold(j) times bold(B)$]),
        node((0, 2), [Force balance \
          $grad p=bold(j) times bold(B)$]),
        edge((0, 0), (-1.4, 1), [pressure], "->"),
        edge((0, 0), (1.4, 1), [magnetic], "->"),
        edge((-1.4, 1), (0, 2), [balance], "->"),
        edge((1.4, 1), (0, 2), [balance], "->"),
      )
    ]
  } else {
    html.figure(class: "concept-figure")[
      #html.div(
        class: "mhd-diagram mhd-force-fallback",
        role: "img",
        aria-label: alt-description,
      )[
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Static MHD]
          #html.span[$partial_t=0, bold(u)=bold(0)$]
        ]
        #html.div(class: "mhd-arrow")[two force densities act in opposite directions]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-pressure")[
            #html.strong[Pressure force]
            #html.span[$-grad p$]
          ]
          #html.div(class: "mhd-node mhd-node-magnetic")[
            #html.strong[Magnetic force]
            #html.span[$bold(j) times bold(B)$]
          ]
        ]
        #html.div(class: "mhd-arrow")[↓ equilibrium]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Force balance]
          #html.span[$grad p=bold(j) times bold(B)$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let collision-regimes = context {
  let alt-description = "A transport map starts with moving charged particles and separates two causes of organized motion: spatial inhomogeneity produces diffusion, while an applied external force produces mobility and conductivity. Both routes are mediated by collisions."
  let caption-text = [
    Gradients or external forces drive transport; collisions mediate its response.
    Collisions alone do not drive a current in homogeneous equilibrium.
    Density or temperature inhomogeneity produces diffusion; an applied force
    produces mobility and, for charged particles, electrical conductivity.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.45cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Moving charge carriers]),
        node((-1.35, 1), [Inhomogeneity \
          diffusion]),
        node((1.35, 1), [External force \
          mobility]),
        node((0, 2), [Transport and conductivity]),
        edge((0, 0), (-1.35, 1), [redirection], "->"),
        edge((0, 0), (1.35, 1), [drag], "->"),
        edge((-1.35, 1), (0, 2), [flux], "->"),
        edge((1.35, 1), (0, 2), [current], "->"),
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
          #html.strong[Moving charge carriers]
        ]
        #html.div(class: "mhd-arrow")[two transport mechanisms]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node")[
            #html.strong[Inhomogeneity]
            #html.span[Diffusion]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[External force]
            #html.span[Mobility and conductivity]
          ]
        ]
        #html.div(class: "mhd-arrow")[collisions provide the drag or scattering]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Transport response]
          #html.span[particle flux or electric current]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let coulomb-cutoff = context {
  let alt-description = "A Coulomb-scattering scale map shows the lower impact-parameter cutoff b ninety, set by strong ninety-degree deflection, and the upper cutoff at the Debye length. Their ratio defines a plasma parameter with unit [1] and its Coulomb logarithm."
  let caption-text = [
    Coulomb scattering is accumulated between a strong-deflection scale
    $b_90$ and the shielding scale $lambda_D$. The logarithm
    $ln Lambda=ln(lambda_D/b_90)$ records the broad range of effective
    impact parameters; the exact prefactor depends on the collision model.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.35cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Coulomb encounter]),
        node((-1.35, 1), [Strong deflection \
          $b_90$]),
        node((1.35, 1), [Screening cutoff \
          $lambda_D$]),
        node((0, 2), [Coulomb logarithm \
          #normalized-label[$ln Lambda$]]),
        edge((0, 0), (-1.35, 1), [lower scale], "->"),
        edge((0, 0), (1.35, 1), [upper scale], "->"),
        edge((-1.35, 1), (0, 2), [ratio], "->"),
        edge((1.35, 1), (0, 2), [ratio], "->"),
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
          #html.strong[Coulomb encounter]
          #html.span[impact parameter controls the deflection]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-hall")[
            #html.strong[Strong-deflection cutoff]
            #html.span[$b_90=(Z e^2)/(m_r v_"rel"^2)$]
          ]
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Shielding cutoff]
            #html.span[$b_"max" approx lambda_D$]
          ]
        ]
        #html.div(class: "mhd-arrow")[integrate over $b_90 < b < lambda_D$]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Coulomb logarithm]
          #html.span[#normalized-label[$ln Lambda=ln(lambda_D/b_90)$]]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let conductivity-tensor = context {
  let alt-description = "A conductivity map decomposes an applied electric field relative to a background magnetic field into parallel and perpendicular components. The parallel current follows the field, the Pedersen current follows the perpendicular field, and the Hall current is perpendicular to both the electric and magnetic fields."
  let caption-text = [
    A static magnetic field makes conductivity anisotropic. The parallel,
    Pedersen, and Hall entries are the three components of the conductivity
    tensor; their signs depend on the signed charge convention.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.45cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Applied field \
          $bold(E)$]),
        node((-1.35, 1), [Parallel response \
          $sigma_parallel$]),
        node((1.35, 1), [Pedersen response \
          $sigma_perp$]),
        node((1.35, 2), [Hall response \
          $sigma_"H"$]),
        edge((0, 0), (-1.35, 1), [along $bold(B)_0$], "->"),
        edge((0, 0), (1.35, 1), [across $bold(B)_0$], "->"),
        edge((1.35, 1), (1.35, 2), [rotated current], "->"),
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
          #html.strong[Applied electric field]
          #html.span[$bold(E)$ relative to $bold(B)_0$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Parallel]
            #html.span[$bold(J)_parallel=sigma_parallel bold(E)_parallel$]
          ]
          #html.div(class: "mhd-node")[
            #html.strong[Pedersen]
            #html.span[$sigma_perp$ follows $bold(E)_perp$]
          ]
        ]
        #html.div(class: "mhd-arrow")[the Hall term rotates the perpendicular current]
        #html.div(class: "mhd-node mhd-node-hall")[
          #html.strong[Hall]
          #html.span[$bold(J)_"H"$ is perpendicular to both $bold(E)$ and $bold(B)_0$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let random-walk-diffusion = context {
  let alt-description = "Conserved Gaussian density profiles versus x/L0, with density n/n0 and both axes normalized. At t/tauD=4 the profile is twice as wide and half as high as at t/tauD=1, with the same center and full-line area."
  let caption-text = [
    Conserved one-dimensional diffusion from a point source:
    $n/n_0=tau^(-1/2) exp(-xi^2/(4 tau))$, where $xi=x/L_0$,
    $tau=t/tau_D$, $tau_D=L_0^2/D$, and $n_0=N_0/(sqrt(4 pi) L_0)$.
    For volumetric density $n$ in #unit("m^-3"), the conserved column
    $N_0=integral n dif x$ has units #unit("m^-2").
    At $tau=4$ the width doubles and the peak halves relative to $tau=1$.
    The full-line area is constant; the displayed window truncates the tails.
    Both axes and normalized times use unit #text("[1]").
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xlabel: normalized-axis[$x \/ L_0$],
      ylabel: normalized-axis[$n \/ n_0$],
      ..curve(samples(-8, 8, n: 160), x => model.diffusion(x, 1)),
      ..curve(samples(-8, 8, n: 160), x => model.diffusion(x, 4),
        color: plot-orange, dash: "dashed"),
      tag(1.3, model.diffusion(1.3, 1), align: left + bottom)[#normalized-label[$t \/ tau_D=1$]],
      tag(3.6, model.diffusion(3.6, 4), color: plot-orange, align: left + bottom)[#normalized-label[$t \/ tau_D=4$]],
    )
  ]

}

#let ambipolar-balance = context {
  let alt-description = "An ambipolar transport map starts with a density gradient, sends ions and electrons toward opposite electric-force responses, and ends with a self-consistent ambipolar electric field and one common particle flux under a zero-current boundary condition. The electric field prevents the faster species from separating from the slower species."
  let caption-text = [
    Ambipolar diffusion couples the species fluxes. Quasi-neutrality together with a zero-current boundary condition determines
    the electric field that makes the electron and ion particle fluxes equal,
    producing the ambipolar coefficient $D_a$.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (2.1cm, 1.1cm),
        ..concept-style,
        node((0, 0), [Density gradient \
          $grad n$]),
        node((-1.35, 1), [Ion response \
          $mu_i bold(E)-D_i grad n \/ n$]),
        node((1.35, 1), [Electron response \
          $-mu_e bold(E)-D_e grad n \/ n$]),
        node((0, 2), [Ambipolar field \
          $bold(E)=(D_i-D_e)/(mu_i+mu_e) thin grad n \/ n$]),
        node((0, 3), [Common flux \
          $bold(Gamma)=-D_a grad n$]),
        edge((0, 0), (-1.35, 1), [], "->"),
        edge((0, 0), (1.35, 1), [], "->"),
        edge((-1.35, 1), (0, 2), [balance], "->"),
        edge((1.35, 1), (0, 2), [balance], "->"),
        edge((0, 2), (0, 3), [zero current], "->"),
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
          #html.strong[Density gradient]
          #html.span[$grad n$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Ion response]
            #html.span[$mu_i bold(E)-D_i grad n \/ n$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Electron response]
            #html.span[$-mu_e bold(E)-D_e grad n \/ n$]
          ]
        ]
        #html.div(class: "mhd-arrow")[equal particle flux]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Ambipolar field]
          #html.span[$bold(E)=(D_i-D_e)/(mu_i+mu_e) thin grad n \/ n$]
        ]
        #html.div(class: "mhd-arrow")[zero-current common flux]
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[$bold(Gamma)=-D_a grad n$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let cross-field-diffusion = context {
  let alt-description = "A normalized plot shows perpendicular diffusion falling as magnetization increases. The horizontal axis is the absolute cyclotron frequency divided by collision frequency with unit [1]; the vertical axis is perpendicular diffusion divided by the unmagnetized diffusion coefficient. The curve starts at one and approaches zero as the inverse square of magnetization."
  let caption-text = [
    Collisions enable cross-field steps by interrupting gyromotion. With
    $D_0=(k_B T)/(m nu)$, the classical single-species result is
    $D_perp/D_0=1/(1+(Omega/nu)^2)$.
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xlabel: normalized-axis[$abs(Omega) \/ nu$],
      ylabel: normalized-axis[$D_perp \/ D_0$],
      ..curve(samples(0, 10, n: 160), model.cross-field),
    )
  ]

}

#let diffusion-scalings = context {
  let alt-description = "A normalized transport plot compares two fully ionized cross-field diffusion scalings as magnetic field strength increases. Classical diffusion decreases as one over magnetic field squared, while the empirical Bohm estimate decreases only as one over magnetic field."
  let caption-text = [
    Classical and Bohm-like cross-field scalings have different magnetic-field
    dependence. Each curve is normalized to its value at $B=B_0$; the Bohm
    curve is empirical and represents unresolved turbulent transport.
    Logarithmic axes turn the power laws into straight lines of slope $-2$
    and $-1$.
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xscale: "log",
      yscale: "log",
      xaxis: (ticks: decimal-ticks((0.5, 1, 2, 4, 8))),
      yaxis: (ticks: decimal-ticks((0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 4))),
      xlabel: normalized-axis[$B \/ B_0$],
      ylabel: normalized-axis[$D_(perp)(B) \/ D_(perp)(B_0)$],
      ..curve(samples(0.5, 8), model.classical),
      ..curve(samples(0.5, 8), model.bohm, color: plot-orange, dash: "dashed"),
      tag(3, model.classical(3), align: right + top)[classical $prop B^(-2)$],
      tag(3, model.bohm(3), color: plot-orange, align: left + bottom)[Bohm $prop B^(-1)$],
    )
  ]

}

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

#let wave-dispersion = context {
  let alt-description = "A normalized dispersion plot compares a vacuum electromagnetic line, a cold plasma electromagnetic branch that starts at the plasma cutoff, and a horizontal cold electrostatic plasma-oscillation branch. The vertical axis is frequency divided by the electron plasma frequency and the horizontal axis is wave number times the speed of light divided by that frequency."
  let caption-text = [
    Normalized dispersion relations. The vacuum line is $W=K$, the cold
    transverse plasma branch is $W=sqrt(1+K^2)$, and the fixed-ion cold
    electrostatic oscillation is $W=1$.
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.4cm,
      xlabel: normalized-axis[$K=k c \/ omega_(p,e)$],
      ylabel: normalized-axis[$W=omega \/ omega_(p,e)$],
      ..curve(samples(0, 4), x => x, color: plot-gray, dash: "dotted"),
      ..curve(samples(0, 4), model.cold-em),
      ..curve(samples(0, 4), x => 1, color: plot-orange, dash: "dashed"),
      tag(3.2, 3.2, color: plot-gray, align: left + top)[vacuum, $W=K$],
      tag(2.2, model.cold-em(2.2), align: right + bottom)[cold EM, $W=sqrt(1+K^2)$],
      tag(4, 1, color: plot-orange, align: right + bottom)[cold electrostatic, $W=1$],
    )
  ]

}

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
          $c_s^2=(gamma_s k_B T_s)/m_s$]),
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
          #html.span[$c_s^2=(gamma_s k_B T_s)/m_s$]
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

#let magnetized-parallel-dispersion = context {
  // Quadratic sampling resolves the square-root rise above each cutoff.
  let branch(sense, color: plot-blue, dash: none) = {
    let lo = model.circular-cutoff(sense: sense)
    let ws = range(161).map(i => lo + (4 - lo)*calc.pow(i/160, 2))
    (lq.plot(ws.map(w => model.circular-index(w, sense: sense)), ws,
      color: color, mark: none, stroke: (thickness: plot-stroke, dash: dash)),)
  }
  let alt-description = "Cold parallel dispersion versus refractive index N=kc/omega, with normalized frequency W=omega/omega_pe on the vertical axis. Two upper circular branches start at different cutoffs and approach the vertical vacuum line N=1. A horizontal W=1 line marks the longitudinal oscillation. All axes use unit [1]."
  let caption-text = [
    Cold fixed-ion parallel propagation at
    #normalized-label[$Y=omega_(c,e)/omega_(p,e)=0.3$].
    The upper propagating branches satisfy $N_s^2=1-1/(W(W+s Y))$ with the
    circular-mode label $s=±1$ of the text: $s=+1$ (solid) has the lower
    cutoff, $s=-1$ (dashed) the higher one.
    Here $N=(k c)/omega$ is the refractive index, $W=omega/omega_(p,e)$,
    and $K=(k c)/omega_(p,e)=W N$ is a different quantity.
    Vacuum is the vertical line $N=1$, not $W=N$.
    The low-frequency cyclotron continuation is not shown.
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.4cm,
      xlabel: normalized-axis[$N=k c \/ omega$],
      ylabel: normalized-axis[$W=omega \/ omega_(p,e)$],
      xlim: (0, 1.3),
      lq.plot((1, 1), (0, 4), color: plot-gray, mark: none,
        stroke: (thickness: plot-stroke, dash: "dotted")),
      ..branch(1, color: plot-blue),
      ..branch(-1, color: plot-orange, dash: "dashed"),
      lq.plot((0, 1.3), (1, 1), color: plot-gray, mark: none,
        stroke: (thickness: plot-stroke, dash: "dash-dotted")),
      tag(1, 3, color: plot-gray, align: left)[vacuum, $N=1$],
      tag(0.02, model.circular-cutoff(), align: left + top)[$s=+1$],
      tag(0.02, model.circular-cutoff(sense: -1), color: plot-orange, align: left + bottom)[$s=-1$],
      tag(0.55, 1, color: plot-gray, align: left + top)[longitudinal, $W=1$],
    )
  ]

}

#let magnetized-oblique-geometry = context {
  let alt-description = "A coordinate geometry diagram places the uniform background magnetic field along the z axis. The wave vector lies in the x-z plane, its z component is parallel to the field, its x component is perpendicular to the field, and the angle theta is measured between the wave vector and the magnetic field."
  let caption-text = [
    Oblique propagation is represented by $bold(k)=k (sin theta bold(e)_x+cos theta bold(e)_z)$,
    with $bold(B)_0$ along $z$. The angle is a model parameter: $theta=0$ is
    parallel propagation and $theta=pi/2$ is perpendicular propagation.
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

#let magnetized-cutoff-map = context {
  let alt-description = "A frequency map distinguishes three cold-plasma landmarks. A cutoff is marked where the refractive index squared reaches zero and the wave number vanishes. A resonance is marked where the refractive index grows without bound and the wavelength tends to zero. A positive refractive-index-squared interval is labelled propagating, while a negative interval is labelled evanescent."
  let caption-text = [
    Cutoffs and resonances are different limits of the same dispersion
    relation. Cutoffs bound propagation intervals from the low-wave-number
    side; resonances are singular responses where the cold model must be
    checked against warm, collisional, or kinetic physics.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (2.2cm, 1.15cm),
        ..concept-style,
        node((0, 0), [Frequency scan \
          $omega$]),
        node((-1.6, 1), [Cutoff \
          $N^2=0$, $k=0$]),
        node((0, 1), [Propagating \
          $N^2>0$]),
        node((1.6, 1), [Evanescent \
          $N^2<0$]),
        node((0, 2), [Resonance \
          $N^2 -> infinity$]),
        node((0, 3), [Recheck omitted physics]),
        edge((0, 0), (-1.6, 1), [branch endpoint], "->"),
        edge((0, 0), (0, 1), [real $k$], "->"),
        edge((0, 0), (1.6, 1), [imaginary $k$], "->"),
        edge((0, 1), (0, 2), [short scale], "->"),
        edge((0, 2), (0, 3), [warm or kinetic], "->"),
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
          #html.strong[Frequency scan]
          #html.span[$omega$ along a selected dispersion branch]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-result")[
            #html.strong[Cutoff]
            #html.span[$N^2=0$, so $k=0$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Propagating]
            #html.span[$N^2>0$, real $k$]
          ]
        ]
        #html.div(class: "mhd-node mhd-node-pressure")[
          #html.strong[Evanescent]
          #html.span[$N^2<0$, imaginary $k$]
        ]
        #html.div(class: "mhd-arrow")[singular short-scale response]
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[Resonance]
          #html.span[$N^2 -> infinity$; recheck cold ordering]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

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
          $m_"eff"=m(1+(i nu)/omega)$]),
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
            #html.span[$m_"eff"=m(1+(i nu)/omega)$]
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

#let ion-wave-branches = context {
  let alt-description = "Normalized cold two-fluid parallel dispersion. Both circular branches approach the Alfvén line at small K=kvA/omega_ci. The RH whistler branch bends above that line; the LH branch stays below it and approaches W=omega/omega_ci=1. Both axes use unit [1]."
  let caption-text = [
    Cold parallel two-fluid limit with negligible electron inertia,
    $omega << abs(Omega_e)$ and $v_A << c$.
    For $K=(k v_A)/omega_(c,i)$ and $W=omega/omega_(c,i)$,
    $W_"RH"=(K^2+sqrt(K^4+4 K^2))/2$ and
    $W_"LH"=(sqrt(K^4+4 K^2)-K^2)/2$.
    Both approach $W=K$ at small $K$; RH bends upward and LH approaches
    $W=1$. All plotted ratios use unit #text("[1]").
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xlim: (0, 2.75),
      xaxis: (ticks: (0, 0.5, 1, 1.5, 2)),
      xlabel: normalized-axis[$K=k v_A \/ omega_(c,i)$],
      ylabel: normalized-axis[$W=omega \/ omega_(c,i)$],
      ..curve(samples(0, 2), k => k, color: plot-gray, dash: "dotted"),
      ..curve(samples(0, 2), model.ion-rh),
      ..curve(samples(0, 2), model.ion-lh, color: plot-orange, dash: "dashed"),
      tag(1.2, model.ion-rh(1.2), align: right + bottom)[RH (whistler)],
      tag(2, 2, color: plot-gray)[Alfvén, $W=K$],
      tag(2, model.ion-lh(2), color: plot-orange)[LH (ion cyclotron)],
    )
  ]

}

#let warm-longitudinal-modes = context {
  let ks = range(121).map(i => calc.pow(10, -2 + 2.5*i/120))
  let alt-description = "A qualitative normalized dispersion plot on logarithmic axes compares a cold plasma-oscillation line at constant normalized frequency, a warm electron plasma-oscillation branch that rises above it as the Debye-scale wave number approaches one, and a low-frequency ion-acoustic branch that rises linearly and then levels off near the ion plasma frequency, far below the electron branches. Thermal pressure gives the branches wave-number dependence."
  let caption-text = [
    Unmagnetized isothermal-electron fluid comparison, $K=k lambda_(D,e)$:
    the fixed-ion electron branch is $W=sqrt(1+K^2)$, with
    $W=omega/omega_(p,e)$. The negligible-electron-inertia, cold-ion branch
    is $W=K/sqrt(1836(1+K^2))$ for $m_i/m_e=1836$.
    This compares separate limiting reductions, not two exact roots of one
    kinetic model. Logarithmic axes keep the ion branch visible: it is
    smaller by about $sqrt(m_e/m_i)$ and saturates at
    $omega_(p,i)/omega_(p,e)=sqrt(m_e/m_i)$ for $K>>1$, where both fluid
    closures are outside their controlled small-$K$ regime.
    Ratios use unit #text("[1]"). Here $lambda_(D,e)^2=(k_B T_e)/(m_e omega_(p,e)^2)$.
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xscale: "log",
      yscale: "log",
      xlabel: normalized-axis[$K=k lambda_(D,e)$],
      ylabel: normalized-axis[$W=omega \/ omega_(p,e)$],
      ..curve(ks, k => 1, color: plot-gray, dash: "dotted"),
      ..curve(ks, model.warm-electron),
      ..curve(ks, model.ion-acoustic, color: plot-orange, dash: "dashed"),
      tag(0.012, 1, color: plot-gray, align: left + top)[cold electron, $W=1$],
      tag(1.2, model.warm-electron(1.2), align: right + bottom)[isothermal electron],
      tag(0.05, model.ion-acoustic(0.05), color: plot-orange, align: left + top)[ion acoustic],
    )
  ]

}

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
          $v_A^2=B_0^2/(mu_0 rho_0)$]),
        node((1.35, 1), [Pressure \
          $v_s^2=(gamma p_0)/rho_0$]),
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
            #html.span[$v_A^2=B_0^2/(mu_0 rho_0)$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Thermal pressure]
            #html.span[$v_s^2=(gamma p_0)/rho_0$]
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
    $nu/omega$, $omega/omega_(c,i)$, and $k lambda_D$ before interpreting a
    cold-plasma branch.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.8cm, 1.1cm),
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

#let hot-isotropic-dispersion = context {
  let alt-description = "A normalized dispersion plot compares a cold plasma-oscillation line at constant frequency with a warm long-wavelength branch that rises as k times the Debye length increases. The warm branch is a fluid asymptote to the kinetic real response, and the plot is not a precision kinetic calculation."
  let caption-text = [
    Maxwellian long-wave Bohm–Gross asymptote
    $omega_r/omega_(p,e)=sqrt(1+3(k lambda_(D,e))^2)$ over
    $0 <= k lambda_(D,e) <= 0.3$. This is an asymptotic real frequency,
    not a full kinetic root or a damping calculation.
    $lambda_(D,e)^2=(k_B T_e)/(m_e omega_(p,e)^2)$; both axes use unit #text("[1]").
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xlabel: normalized-axis[$k lambda_(D,e)$],
      ylabel: normalized-axis[$omega_r \/ omega_(p,e)$],
      ..curve(samples(0, 0.3), k => 1, color: plot-gray, dash: "dotted"),
      ..curve(samples(0, 0.3), model.bohm-gross),
      tag(0.3, 1, color: plot-gray, align: right + bottom)[cold response],
      tag(0.2, model.bohm-gross(0.2), align: right + bottom)[Bohm–Gross asymptote],
    )
  ]

}

#let hot-velocity-space-slopes = context {
  let alt-description = "A normalized velocity-space plot compares a Maxwellian distribution, which decreases through a marked positive phase velocity, with a bump-on-tail distribution that has a positive slope near the same region. A negative slope supports Landau damping; a positive slope can support wave growth."
  let caption-text = [
    One-dimensional velocity marginals, with $xi=v/v_"th"$,
    $v_"th"=sqrt((2 k_B T_e)/m_e)$ and $F_"ref"=n_0/(sqrt(pi) v_"th")$.
    The Maxwellian is $F/F_"ref"=exp(-xi^2)$; the equal-density illustrative
    mixture is $0.9 exp(-xi^2)+0.2 exp(-4(xi-2)^2)$.
    At the marked $v_phi/v_"th"=1.7$, near the steepest positive slope of
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

#let two-stream-growth = context {
  let alt-description = "A normalized two-stream growth plot starts at zero wave growth, rises to a maximum at k v zero divided by omega p equal to the square root of three eighths, and returns to zero at the unstable-band boundary k v zero divided by omega p equal to one. The curve shows the cold symmetric two-stream model."
  let caption-text = [
    Exact cold symmetric equal-density electron beams with immobile ions.
    $omega_p$ uses the total electron density and $K=abs(k v_0)/omega_p$.
    The unstable root gives
    $gamma/omega_p=sqrt((sqrt(1+8 K^2)-1-2 K^2)/2)$ for $0<K<1$.
    The marked maximum is $1/(2 sqrt(2))$ at $K=sqrt(3/8)$.
    Both axes use unit #text("[1]").
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xlabel: normalized-axis[$K=abs(k v_0) \/ omega_p$],
      ylabel: normalized-axis[$gamma \/ omega_p$],
      ylim: (0, 0.42),
      ..curve((samples(0, 1, n: 160) + (calc.sqrt(3/8),)).sorted(), model.two-stream),
      lq.plot((calc.sqrt(3/8),), (1/(2*calc.sqrt(2)),), color: plot-orange,
        stroke: none, mark: "o", mark-size: 4.5pt),
      tag(calc.sqrt(3/8), 1/(2*calc.sqrt(2)), color: plot-orange, align: center + bottom)[maximum $1\/(2 sqrt(2))$ at $K=sqrt(3\/8)$],
    )
  ]

}

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
    model regions rather than sharp interfaces in every experiment.
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

#let sheath-profile = context {
  let alt-description = "A normalized boundary-profile plot uses distance from the wall in Debye lengths on the horizontal axis. The electron density rises from a depleted wall-side value toward the plasma density, the ion density stays larger in the sheath, and the positive normalized potential-energy drop decreases toward zero at the sheath edge."
  let caption-text = [
    Illustrative prescribed barrier $eta=2.8(1-x/(6 lambda_D))^2$
    on $0<=x/lambda_D<=6$, with wall at zero and potential referenced to
    the sheath edge: $eta=-(e phi)/(k_B T_e)$.
    Boltzmann electrons obey $n_e/n_0=exp(-eta)$; cold ions entering at
    the Bohm speed obey $n_i/n_0=1/sqrt(1+2 eta)$.
    These responses satisfy energy and particle flux conservation for the
    prescribed potential, but the potential is not a Poisson solution.
    All three plotted ratios and the position axis use unit #text("[1]").
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xlabel: normalized-axis[$x \/ lambda_D$ (wall at $0$)],
      ylabel: normalized-axis[$n_e \/ n_0$, $n_i \/ n_0$, $eta$],
      ..curve(samples(0, 6), model.sheath-barrier, color: plot-gray, dash: "dotted"),
      ..curve(samples(0, 6), model.sheath-electron),
      ..curve(samples(0, 6), model.sheath-ion, color: plot-orange, dash: "dashed"),
      tag(0.9, model.sheath-barrier(0.9), color: plot-gray, align: left + bottom)[$eta$],
      tag(2.2, model.sheath-ion(2.2), color: plot-orange, align: right + bottom)[$n_i \/ n_0$],
      tag(2.2, model.sheath-electron(2.2), align: left + top)[$n_e \/ n_0$],
    )
  ]

}

#let probe-iv-characteristic = context {
  let alt-description = "A normalized Langmuir-probe current--voltage curve has an ion-saturation plateau at strongly negative bias, crosses zero at the floating potential, rises in magnitude through an electron-retardation region, and approaches an electron-saturation regime at positive bias."
  let caption-text = [
    Idealized planar collection with ion-positive, electron-negative current:
    $I/(e Gamma_(e,0) A)=0.058-exp(min(u,0))$,
    $u=(e(phi_p-phi_"pl"))/(k_B T_e)$. The ion term is
    $Gamma_i/Gamma_(e,0)=sqrt((2 pi m_e)/m_i) approx 0.058$ for hydrogen, with
    $Gamma_i=n_0 sqrt((k_B T_e)/m_i)$ and
    $Gamma_(e,0)=n_0 sqrt((k_B T_e)/(2 pi m_e))$; the current vanishes at
    the floating value $u_f=ln 0.058 approx -2.85$.
    The constant ion contribution is an approximation; the positive-bias
    electron branch saturates continuously at the plasma potential.
    The electron-retardation exponential supplies the temperature diagnostic.
    All plotted ratios use unit #text("[1]"). Real collection depends on geometry.
  ]

  figure(
    alt: alt-description,
    caption: caption-text,
  )[
    #plot-diagram(
      width: 10cm,
      height: 5.2cm,
      xlabel: normalized-axis[$u=e (phi_p-phi_"pl") \/ (k_B T_e)$],
      ylabel: normalized-axis[$I \/ (e Gamma_(e,0) A)$],
      ylim: (-1.1, 0.25),
      lq.plot((-6, 2), (0, 0), color: plot-gray, mark: none, stroke: 0.5pt),
      ..curve(samples(-6, 2, n: 160), model.probe),
      lq.plot((calc.ln(0.058),), (0,), color: plot-orange, stroke: none,
        mark: "o", mark-size: 4.5pt),
      tag(calc.ln(0.058), 0, color: plot-orange, align: left + bottom)[floating, $u_f approx -2.85$],
      tag(-6, model.probe(-6), align: left + bottom)[ion saturation],
      tag(0.1, model.probe(1), align: left + top)[electron saturation],
    )
  ]

}
