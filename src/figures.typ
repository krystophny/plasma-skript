#import "@preview/cetz:0.5.2"
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "@preview/lilaq:0.6.0" as lq
#import "@preview/physica:0.9.8": grad, pdv, curl
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

#let maxwellian-profile = figure(
  alt: "A dimensionless one-dimensional velocity plot compares a centered Maxwellian distribution with a second Maxwellian shifted toward positive velocity. The centered curve peaks at zero velocity, while the shifted curve peaks at positive normalized velocity and has the same Gaussian width.",
  caption: [
    Centered and drifting one-dimensional Maxwellians. The horizontal axis is
    velocity normalized by $v_"th"=sqrt(2 k_B T/m)$, and the vertical axis is
    distribution value normalized by the centered peak. Markers and direct
    labels distinguish the curves independently of color.
  ],
)[
  #lq.diagram(
    width: 10cm,
    height: 5.2cm,
    xlabel: [$v / v_"th"$ (dimensionless)],
    ylabel: [$f / f_0$ (dimensionless)],
    lq.plot(
      (-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3),
      (0.011, 0.044, 0.135, 0.325, 0.607, 0.882, 1, 0.882, 0.607, 0.325, 0.135, 0.044, 0.011),
      color: blue,
      mark: "o",
      label: [centered Maxwellian],
    ),
    lq.plot(
      (-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3),
      (0.000, 0.002, 0.011, 0.044, 0.135, 0.325, 0.607, 0.882, 1, 0.882, 0.607, 0.325, 0.135),
      color: orange,
      mark: "+",
      label: [drifting Maxwellian],
    ),
  )
]

#let moment-hierarchy = figure(
  alt: "A hierarchy diagram starts with the full distribution function f of position and velocity and branches to progressively higher velocity moments: number density n, bulk velocity u, pressure tensor P, and heat flux q. Each lower-level description retains less velocity-space information and requires a closure for the next moment.",
  caption: [
    Velocity moments compress the distribution function into macroscopic
    fields. The hierarchy is not a sequence of unrelated equations: the
    transport law for one moment generally contains the next moment.
  ],
)[
  #fletcher.diagram(
    spacing: (2.6cm, 1.15cm),
    node-stroke: 1pt,
    edge-stroke: 1pt,
    node((0, 0), [Distribution $f(t, bold(r), bold(v))$]),
    node((-1.8, -1), [0th moment $n$]),
    node((0, -1), [1st moment $bold(u)$]),
    node((1.8, -1), [2nd moment $bold(P)$]),
    node((0, -2), [3rd central moment $bold(q)$]),
    edge((0, 0), (-1.8, -1), [integrate], "->"),
    edge((0, 0), (0, -1), [weight $bold(v)$], "->"),
    edge((0, 0), (1.8, -1), [weight $bold(w) bold(w)$], "->"),
    edge((1.8, -1), (0, -2), [higher transport], "->"),
  )
]

#let multiple-fluid-hierarchy = context {
  let alt-description = "A schematic multiple-fluid hierarchy starts with one kinetic distribution for each species. The electron and ion distributions are separately reduced to electron and ion density, velocity, and pressure fields. Their coupled equations share electric and magnetic fields, and summing the species equations gives one-fluid variables only after the relative-flow stress is accounted for."
  let caption-text = [
    Species-resolved moments retain the relative motion of electrons and ions.
    The electromagnetic field couples the two fluid systems; a one-fluid
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Kinetic species states \
          $f_(e), f_(i)$]),
        node((-1.7, -1), [Electron fluid \
          $n_(e), bold(u)_(e), bold(P)_(e)$]),
        node((1.7, -1), [Ion fluid \
          $n_(i), bold(u)_(i), bold(P)_(i)$]),
        node((0, -2), [Coupled fields \
          $bold(E), bold(B)$]),
        node((0, -3), [One-fluid sums \
          $rho, bold(u), bold(P), bold(j)$]),
        edge((0, 0), (-1.7, -1), [velocity moments], "->"),
        edge((0, 0), (1.7, -1), [velocity moments], "->"),
        edge((-1.7, -1), (0, -2), [Lorentz force], "->"),
        edge((1.7, -1), (0, -2), [Lorentz force], "->"),
        edge((0, -2), (0, -3), [sum and define], "->"),
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
        #html.div(class: "hierarchy-arrow")[↓ shared Lorentz force]
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Electron + ion equations]),
        node((-1.45, -1), [Mass-weighted sum \
          $rho, bold(u), bold(P)$]),
        node((1.45, -1), [Species difference \
          $bold(E)+bold(u)times bold(B)/c$]),
        node((0, -2), [Single-fluid MHD \
          mass, momentum, induction]),
        edge((0, 0), (-1.45, -1), [sum], "->"),
        edge((0, 0), (1.45, -1), [subtract], "->"),
        edge((-1.45, -1), (0, -2), [closure], "->"),
        edge((1.45, -1), (0, -2), [ordering], "->"),
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
            #html.span[$bold(E)+bold(u)times bold(B)/c$]
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
  let alt-description = "A generalized Ohm-law map places the ideal electric field and bulk magnetic advection on the left, with Hall, electron-pressure, resistive, and electron-inertia corrections listed as separate terms on the right."
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
        spacing: (1.25cm, 1.1cm),
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Generalized Ohm law \
          $bold(E)+bold(u)times bold(B)/c$]),
        node((-1.25, -1), [Hall \
          $bold(j)times bold(B)/(e n c)$]),
        node((1.25, -1), [Electron pressure \
          $-grad p_(e)/(e n)$]),
        node((-1.25, -2), [Resistive \
          $eta bold(j)$]),
        node((1.25, -2), [Electron inertia \
          $m_(e) partial_t bold(j)/(e^2 n)$]),
        edge((0, 0), (-1.25, -1), [correction], "->"),
        edge((0, 0), (1.25, -1), [correction], "->"),
        edge((0, 0), (-1.25, -2), [correction], "->"),
        edge((0, 0), (1.25, -2), [correction], "->"),
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
          #html.span[$bold(E)+bold(u)times bold(B)/c$]
        ]
        #html.div(class: "mhd-arrow")[four corrections are ordered separately]
        #html.div(class: "mhd-term-grid")[
          #html.div(class: "mhd-node mhd-node-hall")[
            #html.strong[Hall]
            #html.span[$bold(j)times bold(B)/(e n c)$]
          ]
          #html.div(class: "mhd-node")[
            #html.strong[Electron pressure]
            #html.span[$-grad_(bold(r))(p_(e))/(e n)$]
          ]
          #html.div(class: "mhd-node mhd-node-resistive")[
            #html.strong[Resistive]
            #html.span[$eta bold(j)$]
          ]
          #html.div(class: "mhd-node")[
            #html.strong[Electron inertia]
            #html.span[$m_(e) partial_t bold(j)/(e^2 n)$]
          ]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let mhd-flux-diffusion = context {
  let alt-description = "A transport map separates two regimes of the induction equation. At high magnetic Reynolds number, magnetic flux through a material loop is constant and field lines move with the fluid. With finite resistivity, a magnetic-diffusion term changes the field topology on a diffusion timescale."
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Induction equation \
          $partial_t bold(B)=grad times (bold(u)times bold(B))+D_B nabla^2 bold(B)$]),
        node((-1.35, -1), [Ideal \
          $R_m >> 1$]),
        node((1.35, -1), [Finite resistivity \
          $D_B=c^2 eta/(4 pi)$]),
        node((-1.35, -2), [Frozen flux \
          field lines move with $bold(u)$]),
        node((1.35, -2), [Diffusion \
          $tau_D=L^2/D_B$]),
        edge((0, 0), (-1.35, -1), [advection dominates], "->"),
        edge((0, 0), (1.35, -1), [diffusion retained], "->"),
        edge((-1.35, -1), (-1.35, -2), [flux conserved], "->"),
        edge((1.35, -1), (1.35, -2), [topology can change], "->"),
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
          #html.span[$pdv(bold(B),t)=curl_(bold(r))(bold(u)times bold(B))+D_(B)nabla^2 bold(B)$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Ideal: $R_m >> 1$]
            #html.span[Frozen flux; field lines move with $bold(u)$]
          ]
          #html.div(class: "mhd-node mhd-node-diffusion")[
            #html.strong[Finite resistivity]
            #html.span[$D_B=c^2 eta/(4 pi)$; diffusion time $tau_D=L^2/D_B$]
          ]
        ]
        #html.div(class: "mhd-arrow")[advection dominates ↔ diffusion changes topology]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let mhd-force-balance = context {
  let alt-description = "A static MHD force-balance diagram shows pressure-gradient force balanced by magnetic force density. The equilibrium condition is grad p equals j cross B divided by c, and both forces are perpendicular to the magnetic field."
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Static MHD \
          $partial_t=0, bold(u)=bold(0)$]),
        node((-1.4, -1), [Pressure force \
          $-grad p$]),
        node((1.4, -1), [Magnetic force \
          $bold(j)times bold(B)/c$]),
        node((0, -2), [Force balance \
          $grad p=bold(j)times bold(B)/c$]),
        edge((0, 0), (-1.4, -1), [pressure], "->"),
        edge((0, 0), (1.4, -1), [magnetic], "->"),
        edge((-1.4, -1), (0, -2), [balance], "->"),
        edge((1.4, -1), (0, -2), [balance], "->"),
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
            #html.span[$-grad_(bold(r))(p)$]
          ]
          #html.div(class: "mhd-node mhd-node-magnetic")[
            #html.strong[Magnetic force]
            #html.span[$bold(j)times bold(B)/c$]
          ]
        ]
        #html.div(class: "mhd-arrow")[↓ equilibrium]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Force balance]
          #html.span[$grad p=bold(j)times bold(B)/c$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let collision-regimes = context {
  let alt-description = "A transport map starts with moving charged particles and separates two causes of organized motion: spatial inhomogeneity produces diffusion, while an applied external force produces mobility and conductivity. Both routes are mediated by collisions."
  let caption-text = [
    Collisions turn random thermal motion into a measurable transport response.
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Moving charge carriers]),
        node((-1.35, -1), [Inhomogeneity \
          diffusion]),
        node((1.35, -1), [External force \
          mobility]),
        node((0, -2), [Transport and conductivity]),
        edge((0, 0), (-1.35, -1), [redirection], "->"),
        edge((0, 0), (1.35, -1), [drag], "->"),
        edge((-1.35, -1), (0, -2), [flux], "->"),
        edge((1.35, -1), (0, -2), [current], "->"),
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
  let alt-description = "A Coulomb-scattering scale map shows the lower impact-parameter cutoff b ninety, set by strong ninety-degree deflection, and the upper cutoff at the Debye length. Their ratio defines the dimensionless plasma parameter and its Coulomb logarithm."
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Coulomb encounter]),
        node((-1.35, -1), [Strong deflection \
          $b_90$]),
        node((1.35, -1), [Screening cutoff \
          $lambda_D$]),
        node((0, -2), [Coulomb logarithm \
          $ln Lambda$]),
        edge((0, 0), (-1.35, -1), [lower scale], "->"),
        edge((0, 0), (1.35, -1), [upper scale], "->"),
        edge((-1.35, -1), (0, -2), [ratio], "->"),
        edge((1.35, -1), (0, -2), [ratio], "->"),
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
            #html.span[$b_90=Z e^2/(m_r v_"rel"^2)$]
          ]
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Shielding cutoff]
            #html.span[$b_"max" approx lambda_D$]
          ]
        ]
        #html.div(class: "mhd-arrow")[integrate over $b_90 < b < lambda_D$]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Coulomb logarithm]
          #html.span[$ln Lambda=ln(lambda_D/b_90)$]
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Applied field \
          $bold(E)$]),
        node((-1.35, -1), [Parallel response \
          $sigma_"parallel"$]),
        node((1.35, -1), [Perpendicular response \
          $sigma_"perp"$]),
        node((0, -2), [Hall response \
          $sigma_"H"$]),
        edge((0, 0), (-1.35, -1), [along $bold(B)_0$], "->"),
        edge((0, 0), (1.35, -1), [across $bold(B)_0$], "->"),
        edge((1.35, -1), (0, -2), [rotated current], "->"),
        edge((-1.35, -1), (0, -2), [tensor basis], "->"),
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
            #html.span[$bold(J)_parallel=sigma_"parallel" bold(E)_parallel$]
          ]
          #html.div(class: "mhd-node")[
            #html.strong[Pedersen]
            #html.span[$sigma_"perp"$ follows $bold(E)_perp$]
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
  let alt-description = "A dimensionless density plot compares two symmetric random-walk distributions. At one normalized diffusion time the profile is narrow and centered at zero; at four normalized diffusion times it is broader but has the same center, showing zero mean displacement and growing variance."
  let caption-text = [
    Random-walk spreading keeps the mean position fixed while the variance
    grows linearly with time. Both axes are dimensionless: position is scaled
    by a reference length and density by the initial peak.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$x / L_0$ (dimensionless)],
        ylabel: [$n / n_0$ (dimensionless)],
        lq.plot(
          (-4, -3, -2, -1, 0, 1, 2, 3, 4),
          (0.004, 0.018, 0.082, 0.368, 1, 0.368, 0.082, 0.018, 0.004),
          color: blue,
          mark: "o",
          label: [$t / tau_D=1$],
        ),
        lq.plot(
          (-4, -3, -2, -1, 0, 1, 2, 3, 4),
          (0.135, 0.325, 0.607, 0.882, 1, 0.882, 0.607, 0.325, 0.135),
          color: orange,
          mark: "+",
          label: [$t / tau_D=4$],
        ),
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
          #html.strong[Symmetric random walk]
          #html.span[$⟨x⟩=0$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[$t / tau_D=1$]
            #html.span[narrow density profile]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[$t / tau_D=4$]
            #html.span[broader density profile]
          ]
        ]
        #html.div(class: "mhd-arrow")[$⟨x^2⟩=2 D t$ in one dimension]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let ambipolar-balance = context {
  let alt-description = "An ambipolar transport map starts with a density gradient, sends ions and electrons toward opposite electric-force responses, and ends with a self-consistent ambipolar electric field and one common particle flux. The electric field prevents the faster species from separating from the slower species."
  let caption-text = [
    Ambipolar diffusion couples the species fluxes. Quasi-neutrality supplies
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Density gradient \
          $grad n$]),
        node((-1.35, -1), [Ion response \
          $mu_i bold(E)-D_i grad n/n$]),
        node((1.35, -1), [Electron response \
          $-mu_e bold(E)-D_e grad n/n$]),
        node((0, -2), [Ambipolar field \
          $bold(E)=(D_i-D_e)/(mu_i+mu_e) grad n/n$]),
        node((0, -3), [Common flux \
          $bold(Gamma)=-D_a grad n$]),
        edge((0, 0), (-1.35, -1), [], "->"),
        edge((0, 0), (1.35, -1), [], "->"),
        edge((-1.35, -1), (0, -2), [balance], "->"),
        edge((1.35, -1), (0, -2), [balance], "->"),
        edge((0, -2), (0, -3), [quasi-neutrality], "->"),
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
            #html.span[$mu_i bold(E)-D_i grad n/n$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Electron response]
            #html.span[$-mu_e bold(E)-D_e grad n/n$]
          ]
        ]
        #html.div(class: "mhd-arrow")[equal particle flux]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Ambipolar field]
          #html.span[$bold(E)=(D_i-D_e)/(mu_i+mu_e) grad n/n$]
        ]
        #html.div(class: "mhd-arrow")[quasi-neutral common flux]
        #html.div(class: "mhd-node mhd-node-wide")[
          #html.strong[$bold(Gamma)=-D_a grad n$]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let cross-field-diffusion = context {
  let alt-description = "A normalized plot shows perpendicular diffusion falling as magnetization increases. The horizontal axis is the dimensionless product of signed cyclotron frequency magnitude and collision time; the vertical axis is perpendicular diffusion divided by the unmagnetized diffusion coefficient. The curve starts at one and approaches zero as the inverse square of magnetization."
  let caption-text = [
    Collisions enable cross-field steps by interrupting gyromotion. With
    $D_0=k_B T/(m nu)$, the classical single-species result is
    $D_perp/D_0=1/(1+(Omega/nu)^2)$.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$abs(Omega) / nu$ (dimensionless)],
        ylabel: [$D_perp / D_0$ (dimensionless)],
        lq.plot(
          (0, 0.1, 0.3, 1, 3, 10),
          (1, 0.990, 0.917, 0.500, 0.100, 0.0099),
          color: blue,
          mark: "o",
          label: [classical suppression],
        ),
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
          #html.strong[Parallel motion]
          #html.span[$D_parallel=D_0$]
        ]
        #html.div(class: "mhd-arrow")[increasing $abs(Omega)/nu$]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Weak magnetization]
            #html.span[$D_perp approx D_0$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Strong magnetization]
            #html.span[$D_perp approx D_0 (nu/Omega)^2$]
          ]
        ]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Cross-field transport]
          #html.span[collisions interrupt gyromotion]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let diffusion-scalings = context {
  let alt-description = "A normalized transport plot compares two fully ionized cross-field diffusion scalings as magnetic field strength increases. Classical diffusion decreases as one over magnetic field squared, while the empirical Bohm estimate decreases only as one over magnetic field."
  let caption-text = [
    Classical and Bohm-like cross-field scalings have different magnetic-field
    dependence. Each curve is normalized to its value at $B=B_0$; the Bohm
    curve is empirical and represents unresolved turbulent transport.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$B / B_0$ (dimensionless)],
        ylabel: [$D_(perp)(B) / D_(perp)(B_0)$ (dimensionless)],
        lq.plot(
          (0.5, 1, 2, 4, 8),
          (4, 1, 0.25, 0.0625, 0.0156),
          color: blue,
          mark: "o",
          label: [classical $B^(-2)$],
        ),
        lq.plot(
          (0.5, 1, 2, 4, 8),
          (2, 1, 0.5, 0.25, 0.125),
          color: orange,
          mark: "+",
          label: [Bohm $B^(-1)$],
        ),
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
          #html.strong[Fully ionized transport]
          #html.span[normalized at $B=B_0$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Classical]
            #html.span[$D_perp ∝ B^(-2)$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Bohm-like]
            #html.span[$D_perp ∝ B^(-1)$]
          ]
        ]
        #html.div(class: "mhd-arrow")[anomalous transport is linked to turbulence]
      ]
      #html.figcaption[#caption-text]
    ]
  }
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Equilibrium \
          $n_0, bold(u)_0, bold(E)_0, bold(B)_0$]),
        node((-1.35, -1), [Small perturbations \
          $epsilon A_1$]),
        node((1.35, -1), [Plane wave \
          $exp(i (bold(k) dot bold(r)-omega t))$]),
        node((0, -2), [Linear algebra \
          $M(omega,bold(k)) A=0$]),
        node((0, -3), [Dispersion relation \
          $det M=0$]),
        edge((0, 0), (-1.35, -1), [ordering], "->"),
        edge((0, 0), (1.35, -1), [Fourier], "->"),
        edge((-1.35, -1), (0, -2), [linearize], "->"),
        edge((1.35, -1), (0, -2), [replace derivatives], "->"),
        edge((0, -2), (0, -3), [nonzero amplitude], "->"),
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

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.4cm,
        xlabel: [$K=k c / omega_(p,e)$ (dimensionless)],
        ylabel: [$W=omega / omega_(p,e)$ (dimensionless)],
        lq.plot(
          (0, 0.5, 1, 2, 3, 4),
          (0, 0.5, 1, 2, 3, 4),
          color: muted,
          mark: "o",
          label: [vacuum $W=K$],
        ),
        lq.plot(
          (0, 0.5, 1, 2, 3, 4),
          (1, 1.118, 1.414, 2.236, 3.162, 4.123),
          color: blue,
          mark: "o",
          label: [cold EM $W=sqrt(1+K^2)$],
        ),
        lq.plot(
          (0, 0.5, 1, 2, 3, 4),
          (1, 1, 1, 1, 1, 1),
          color: orange,
          mark: "+",
          label: [cold electrostatic $W=1$],
        ),
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
          #html.strong[Normalized axes]
          #html.span[$K=k c / omega_(p,e)$ and $W=omega / omega_(p,e)$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Vacuum]
            #html.span[$W=K$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Cold electromagnetic]
            #html.span[$W=sqrt(1+K^2)$, cutoff $W=1$]
          ]
        ]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Cold electrostatic]
          #html.span[$W=1$, no group propagation]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Cold fluid \
          no pressure]),
        node((0, -1), [Warm fluid \
          $c_s^2=gamma_s k_B T_s/m_s$]),
        node((0, -2), [Kinetic response \
          $Z(zeta_s)$]),
        edge((0, 0), (0, -1), [pressure closure], "->"),
        edge((0, -1), (0, -2), [resonant particles], "->"),
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
          #html.span[$c_s^2=gamma_s k_B T_s/m_s$]
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Cold momentum \
          $-i omega m_(s) bold(u)_(s)=q_(s)(bold(E)+bold(u)_(s) times bold(B)_(0)/c)$]),
        node((-1.35, -1), [Transverse response \
          $epsilon_(perp), epsilon_(times)$]),
        node((1.35, -1), [Parallel response \
          $epsilon_(parallel)$]),
        node((0, -2), [Dielectric tensor \
          $bold(epsilon)_p$]),
        node((0, -3), [Wave matrix \
          $bold(M)(omega,bold(k)) bold(E)=0$]),
        edge((0, 0), (-1.35, -1), [couple $x,y$], "->"),
        edge((0, 0), (1.35, -1), [separate $z$], "->"),
        edge((-1.35, -1), (0, -2), [assemble], "->"),
        edge((1.35, -1), (0, -2), [assemble], "->"),
        edge((0, -2), (0, -3), [Maxwell], "->"),
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
          #html.span[$-i omega m_(s) bold(u)_(s)=q_(s)(bold(E)+bold(u)_(s) times bold(B)_(0)/c)$]
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
  let alt-description = "A normalized parallel-propagation dispersion plot compares the vacuum line with two circularly polarized cold-plasma branches. The branches begin at distinct cutoffs, approach the vacuum line at high frequency, and the lower-frequency resonant branch is identified as the cyclotron-sensitive branch. A horizontal line marks the longitudinal plasma oscillation."
  let caption-text = [
    Parallel propagation at fixed $Y=Omega_e/omega_(p,e)=0.3$. The circular
    branches have different cutoffs because the magnetic field distinguishes
    the two rotation senses. Only the upper propagating portions are plotted;
    the low-frequency continuation of one branch approaches the cyclotron
    resonance.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.4cm,
        xlabel: [$N=k c/omega_(p,e)$ (dimensionless)],
        ylabel: [$W=omega/omega_(p,e)$ (dimensionless)],
        lq.plot(
          (0, 0.5, 1, 2, 3, 4),
          (0, 0.5, 1, 2, 3, 4),
          color: muted,
          mark: "o",
          label: [vacuum $W=N$],
        ),
        lq.plot(
          (0, 0.397, 0.667, 0.795, 0.885, 0.948, 0.971),
          (0.861, 0.95, 1.2, 1.5, 2, 3, 4),
          color: blue,
          mark: "o",
          label: [circular $+$],
        ),
        lq.plot(
          (0, 0.272, 0.667, 0.855, 0.936, 0.966),
          (1.161, 1.2, 1.5, 2, 3, 4),
          color: orange,
          mark: "o",
          label: [circular $-$],
        ),
        lq.plot(
          (0, 0.8, 1.6, 2.4, 3.2),
          (1, 1, 1, 1, 1),
          color: accent,
          mark: "+",
          label: [longitudinal $W=1$],
        ),
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
          #html.strong[Normalized axes]
          #html.span[$N=k c/omega_(p,e)$, $W=omega/omega_(p,e)$, and $Y=0.3$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Vacuum]
            #html.span[$W=N$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Circular $+$]
            #html.span[cutoff $W=0.861$]
          ]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Circular $-$]
            #html.span[cutoff $W=1.161$, cyclotron-sensitive continuation]
          ]
          #html.div(class: "mhd-node mhd-node-result")[
            #html.strong[Longitudinal]
            #html.span[$W=1$, no group propagation in the cold limit]
          ]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Uniform field \
          $bold(B)_0=B_0 bold(e)_z$]),
        node((-1.1, -1), [Parallel \
          $k_"parallel"=k cos theta$]),
        node((1.1, -1), [Perpendicular \
          $k_"perp"=k sin theta$]),
        node((0, -2), [Oblique wave vector \
          $bold(k) in x-z$ plane]),
        node((0, -3), [Two coupled electromagnetic branches]),
        edge((0, 0), (-1.1, -1), [project], "->"),
        edge((0, 0), (1.1, -1), [project], "->"),
        edge((-1.1, -1), (0, -2), [retain], "->"),
        edge((1.1, -1), (0, -2), [retain], "->"),
        edge((0, -2), (0, -3), [determinant], "->"),
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
            #html.span[$k_"parallel"=k cos theta$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Perpendicular component]
            #html.span[$k_"perp"=k sin theta$]
          ]
        ]
        #html.div(class: "mhd-arrow")[combine in the $x-z$ plane]
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Frequency scan \
          $omega$]),
        node((-1.6, -1), [Cutoff \
          $N^2=0$, $k=0$]),
        node((0, -1), [Propagating \
          $N^2>0$]),
        node((1.6, -1), [Evanescent \
          $N^2<0$]),
        node((0, -2), [Resonance \
          $N^2 -> infinity$]),
        node((0, -3), [Recheck omitted physics]),
        edge((0, 0), (-1.6, -1), [branch endpoint], "->"),
        edge((0, 0), (0, -1), [real $k$], "->"),
        edge((0, 0), (1.6, -1), [imaginary $k$], "->"),
        edge((0, -1), (0, -2), [short scale], "->"),
        edge((0, -2), (0, -3), [warm or kinetic], "->"),
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
    Collisions turn a real cold-plasma response into a complex response. The
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Cold response \
          $nu=0$, real $N$]),
        node((-1.1, -1), [Effective mass \
          $m_"eff"=m(1+i nu/omega)$]),
        node((1.1, -1), [Complex response \
          $N=N_r+i N_i$]),
        node((0, -2), [Phase + attenuation \
          $exp(i k_r z-k_i z)$]),
        edge((0, 0), (-1.1, -1), [add drag], "->"),
        edge((0, 0), (1.1, -1), [complexify], "->"),
        edge((-1.1, -1), (0, -2), [insert in wave law], "->"),
        edge((1.1, -1), (0, -2), [interpret $k_i$], "->"),
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
          #html.span[$nu=0$; real refractive index]
        ]
        #html.div(class: "mhd-arrow")[add collisional drag]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Complex effective mass]
            #html.span[$m_"eff"=m(1+i nu/omega)$]
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
  let alt-description = "A qualitative normalized dispersion plot shows two low-frequency circular branches. Both begin as nearly linear shear-Alfvén behavior at small wave number; one continues toward a whistler-like branch while the other bends toward the ion-cyclotron resonance. The plot is schematic and not dimensional data."
  let caption-text = [
    Qualitative two-fluid parallel dispersion. At low frequency the two
    circular branches approach the same shear-Alfvén speed; ion inertia
    separates their higher-frequency continuations into whistler-like and
    ion-cyclotron branches.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$k v_A / omega_(c,i)$ (dimensionless)],
        ylabel: [$omega / omega_(c,i)$ (dimensionless)],
        lq.plot(
          (0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2),
          (0, 0.25, 0.49, 0.72, 0.94, 1.15, 1.35, 1.55, 1.75),
          color: blue,
          mark: "o",
          label: [RH / whistler-like],
        ),
        lq.plot(
          (0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2),
          (0, 0.22, 0.41, 0.57, 0.68, 0.76, 0.82, 0.87, 0.91),
          color: orange,
          mark: "+",
          label: [LH / ion-cyclotron],
        ),
        lq.plot(
          (0, 0.5, 1, 1.5, 2),
          (0, 0.5, 1, 1.5, 2),
          color: muted,
          mark: none,
          label: [low-frequency $omega=k v_A$],
        ),
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
          #html.strong[Two-fluid low-frequency branches]
          #html.span[normalized $omega$ versus normalized $k$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[RH / whistler-like]
            #html.span[starts at shear-Alfvén slope]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[LH / ion-cyclotron]
            #html.span[bends toward $omega=omega_(c,i)$]
          ]
        ]
        #html.div(class: "mhd-arrow")[low frequency: both approach $omega=k v_A$]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let warm-longitudinal-modes = context {
  let alt-description = "A qualitative normalized dispersion plot compares a cold plasma-oscillation line at constant normalized frequency, a warm electron plasma-oscillation branch that rises as the Debye-scale wave number increases, and a low-frequency ion-acoustic line. Thermal pressure gives the branches wave-number dependence."
  let caption-text = [
    Thermal pressure gives longitudinal modes spatial dispersion. The warm
    electron branch follows $omega^2=omega_p^2+k^2 c_s^2$ in the simple fluid
    closure, while the low-frequency two-fluid branch is ion acoustic.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$k lambda_D$ (dimensionless)],
        ylabel: [$omega / omega_p$ (dimensionless)],
        lq.plot(
          (0, 0.5, 1, 1.5, 2, 2.5, 3),
          (1, 1, 1, 1, 1, 1, 1),
          color: muted,
          mark: "o",
          label: [cold plasma oscillation],
        ),
        lq.plot(
          (0, 0.5, 1, 1.5, 2, 2.5, 3),
          (1, 1.118, 1.414, 1.803, 2.236, 2.693, 3.162),
          color: blue,
          mark: "o",
          label: [warm electron branch],
        ),
        lq.plot(
          (0, 0.5, 1, 1.5, 2, 2.5, 3),
          (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6),
          color: orange,
          mark: "+",
          label: [ion acoustic],
        ),
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
          #html.strong[Longitudinal response]
          #html.span[normalized frequency versus $k lambda_D$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Cold]
            #html.span[$omega/omega_p=1$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Warm electron]
            #html.span[$omega^2=omega_p^2+k^2c_s^2$]
          ]
        ]
        #html.div(class: "mhd-node mhd-node-result")[
          #html.strong[Ion acoustic]
          #html.span[low-frequency thermal branch]
        ]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let mhd-wave-speeds = context {
  let alt-description = "A warm MHD wave map separates magnetic tension and pressure restoring forces. Magnetic tension alone gives the shear-Alfvén speed v_A; pressure alone gives the sound speed v_s; for perpendicular compression the two restoring terms combine to give the magnetosonic speed v_m equal to the square root of v_A squared plus v_s squared."
  let caption-text = [
    In the warm MHD limit, magnetic tension and pressure are distinct
    restoring forces. Their perpendicular compressional combination gives
    $v_m=sqrt(v_A^2+v_s^2)$.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #fletcher.diagram(
        spacing: (1.55cm, 1.15cm),
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Warm MHD \
          pressure + magnetic field]),
        node((-1.35, -1), [Magnetic tension \
          $v_A^2=B_0^2/(4 pi rho_0)$]),
        node((1.35, -1), [Pressure \
          $v_s^2=gamma p_0/rho_0$]),
        node((0, -2), [Compression \
          $v_m^2=v_A^2+v_s^2$]),
        edge((0, 0), (-1.35, -1), [field restoring], "->"),
        edge((0, 0), (1.35, -1), [thermal restoring], "->"),
        edge((-1.35, -1), (0, -2), [perpendicular], "->"),
        edge((1.35, -1), (0, -2), [perpendicular], "->"),
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
            #html.strong[Magnetic tension]
            #html.span[$v_A^2=B_0^2/(4 pi rho_0)$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Thermal pressure]
            #html.span[$v_s^2=gamma p_0/rho_0$]
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
    Model selection is controlled by dimensionless orderings. Compare
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Cold magnetized wave]),
        node((-1.45, -1), [Collisions \
          $nu/omega$ not small]),
        node((0, -1), [Ion inertia \
          $omega/omega_(c,i)$ small]),
        node((1.45, -1), [Thermal pressure \
          $k lambda_D$ not small]),
        node((0, -2), [Complex, two-fluid, or warm response]),
        node((0, -3), [Kinetic treatment if scales overlap]),
        edge((0, 0), (-1.45, -1), [drag], "->"),
        edge((0, 0), (0, -1), [mobile ions], "->"),
        edge((0, 0), (1.45, -1), [pressure], "->"),
        edge((-1.45, -1), (0, -2), [attenuation], "->"),
        edge((0, -1), (0, -2), [MHD branches], "->"),
        edge((1.45, -1), (0, -2), [warm dispersion], "->"),
        edge((0, -2), (0, -3), [check ordering], "->"),
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
            #html.span[$nu/omega$ not small → complex damping]
          ]
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Ion inertia]
            #html.span[$omega/omega_(c,i)$ small → two-fluid/MHD]
          ]
          #html.div(class: "mhd-node mhd-node-hall")[
            #html.strong[Thermal pressure]
            #html.span[$k lambda_D$ not small → warm dispersion]
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
    A hot isotropic plasma replaces the strictly local cold frequency by a
    dispersive kinetic response. The warm curve is shown as its long-wave
    asymptote, not as a substitute for the full plasma-dispersion function.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$k lambda_D$ (dimensionless)],
        ylabel: [$omega_r / omega_p$ (dimensionless)],
        lq.plot(
          (0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2),
          (1, 1, 1, 1, 1, 1, 1),
          color: muted,
          mark: "o",
          label: [cold response],
        ),
        lq.plot(
          (0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2),
          (1, 1.058, 1.217, 1.442, 1.709, 2.000, 2.307),
          color: blue,
          mark: "+",
          label: [warm long-wave asymptote],
        ),
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
          #html.strong[Hot isotropic response]
          #html.span[normalized $omega_r$ versus $k lambda_D$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Cold]
            #html.span[$omega_r/omega_p=1$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Warm / kinetic]
            #html.span[frequency rises with wave number]
          ]
        ]
        #html.div(class: "mhd-arrow")[pressure and resonant particles supply spatial dispersion]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let hot-velocity-space-slopes = context {
  let alt-description = "A normalized velocity-space plot compares a Maxwellian distribution, which decreases through a marked positive phase velocity, with a bump-on-tail distribution that has a positive slope near the same region. A negative slope supports Landau damping; a positive slope can support wave growth."
  let caption-text = [
    The resonant velocity samples the local slope of the equilibrium
    distribution. A Maxwellian has a negative slope on its positive-velocity
    flank, whereas a bump-on-tail can reverse that slope and supply free
    energy to a wave.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$v / v_"th"$ (dimensionless)],
        ylabel: [$f_0 / f_"max"$ (dimensionless)],
        lq.plot(
          (-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3),
          (0.011, 0.044, 0.135, 0.325, 0.607, 0.882, 1, 0.882, 0.607, 0.325, 0.135, 0.044, 0.011),
          color: blue,
          mark: "o",
          label: [Maxwellian: negative slope],
        ),
        lq.plot(
          (-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3),
          (0.011, 0.044, 0.135, 0.325, 0.607, 0.882, 0.98, 0.80, 0.62, 0.72, 0.88, 0.42, 0.12),
          color: orange,
          mark: "+",
          label: [bump-on-tail: positive-slope region],
        ),
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
          #html.strong[Velocity-space slope at $v_"phi"$]
          #html.span[the resonant denominator samples $dif f_0/dif v$]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Maxwellian]
            #html.span[$dif f_0/dif v<0$ → damping]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Bump-on-tail]
            #html.span[$dif f_0/dif v>0$ → possible growth]
          ]
        ]
        #html.div(class: "mhd-arrow")[resonant particles exchange energy with the wave]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let two-stream-growth = context {
  let alt-description = "A normalized two-stream growth plot starts at zero wave growth, rises to a maximum at k v zero divided by omega p equal to the square root of three eighths, and returns to zero at the unstable-band boundary k v zero divided by omega p equal to one. The curve shows the cold symmetric two-stream model."
  let caption-text = [
    Cold symmetric counter-streaming beams are unstable for
    $0 < abs(k v_0) / omega_p < 1$. The maximum normalized growth rate is
    $gamma_"max"/omega_p=1/(2 sqrt(2))$ in this normalization.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$abs(k v_0) / omega_p$ (dimensionless)],
        ylabel: [$gamma / omega_p$ (dimensionless)],
        lq.plot(
          (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
          (0, 0.168, 0.249, 0.307, 0.340, 0.344, 0.354, 0.331, 0.282, 0.205, 0),
          color: accent,
          mark: "o",
          label: [unstable growth],
        ),
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
          #html.strong[Two-stream dispersion]
          #html.span[normalized growth rate versus normalized wave number]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Unstable band]
            #html.span[$0<abs(k v_0)/omega_p<1$]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Fastest growth]
            #html.span[$gamma_"max"/omega_p=1/(2 sqrt(2))$]
          ]
        ]
        #html.div(class: "mhd-arrow")[the lower frequency-squared branch becomes negative]
      ]
      #html.figcaption[#caption-text]
    ]
  }
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Gyrotropic equilibrium \
          $f_(0)(v_"parallel", v_"perp")$]),
        node((-1.4, -1), [Orbit harmonics \
          $n=0, ±1, ±2, ...$]),
        node((1.4, -1), [Doppler shift \
          $omega-k_parallel v_parallel$]),
        node((0, -2), [Resonance \
          $omega-k_parallel v_parallel-n Omega_s=0$]),
        node((0, -3), [Damping or growth \
          velocity-space gradients]),
        edge((0, 0), (-1.4, -1), [Fourier harmonics], "->"),
        edge((0, 0), (1.4, -1), [parallel motion], "->"),
        edge((-1.4, -1), (0, -2), [cyclotron phase], "->"),
        edge((1.4, -1), (0, -2), [Landau phase], "->"),
        edge((0, -2), (0, -3), [contour prescription], "->"),
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
          #html.span[depends on $v_"parallel"$ and $v_"perp"$]
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
        node-stroke: 1pt,
        edge-stroke: 1pt,
        node((0, 0), [Quasineutral plasma \
          $n_(e) approx n_(i)$]),
        node((0, -1), [Presheath \
          directed ion flow]),
        node((0, -2), [Sheath \
          width approximately a few $lambda_D$]),
        node((0, -3), [Material wall \
          $phi_"wall"<phi_"pl"$]),
        edge((0, 0), (0, -1), [ion acceleration], "->"),
        edge((0, -1), (0, -2), [Bohm entry], "->"),
        edge((0, -2), (0, -3), [particle collection], "->"),
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
    Schematic sheath profiles in normalized variables. The wall is at
    $x=0$, the plasma lies at increasing $x$, and
    $eta=-e phi/(k_B T_e)$ is the positive electron barrier. The curves
    illustrate the separation of electron and ion responses; they are not a
    self-consistent numerical solution for a particular discharge.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$x / lambda_D$ (dimensionless; wall at $0$)],
        ylabel: [normalized density or potential],
        lq.plot(
          (0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6),
          (0.12, 0.18, 0.27, 0.39, 0.53, 0.66, 0.76, 0.89, 0.97, 1.00),
          color: blue,
          mark: "o",
          label: [$n_(e) / n_(0)$],
        ),
        lq.plot(
          (0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6),
          (0.57, 0.63, 0.70, 0.76, 0.81, 0.85, 0.89, 0.95, 0.99, 1.00),
          color: orange,
          mark: "+",
          label: [$n_(i) / n_(0)$],
        ),
        lq.plot(
          (0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6),
          (2.80, 2.35, 1.92, 1.55, 1.20, 0.90, 0.66, 0.33, 0.12, 0.00),
          color: accent,
          mark: "x",
          label: [$eta=-e phi/(k_B T_e)$],
        ),
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
          #html.strong[Wall at x = 0]
          #html.span[the electron barrier is largest at the surface]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Electron density]
            #html.span[depleted near the wall; approaches the plasma value]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Ion density]
            #html.span[ions are accelerated and their density changes by continuity]
          ]
        ]
        #html.div(class: "mhd-arrow")[eta decreases to zero toward the sheath edge]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}

#let probe-iv-characteristic = context {
  let alt-description = "A normalized Langmuir-probe current--voltage curve has an ion-saturation plateau at strongly negative bias, crosses zero at the floating potential, rises in magnitude through an electron-retardation region, and approaches an electron-saturation regime at positive bias."
  let caption-text = [
    Idealized planar-probe characteristic with conventional current into the
    probe. The electron-retardation branch is exponential in the normalized
    bias $u=e(phi_p-phi_"pl")/(k_B T_e)$, which makes its semilog slope a
    temperature diagnostic. Real probes require geometry, sheath, magnetic,
    secondary-emission, and collection corrections.
  ]

  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: caption-text,
    )[
      #lq.diagram(
        width: 10cm,
        height: 5.2cm,
        xlabel: [$u=e(phi_p-phi_"pl")/(k_B T_e)$ (dimensionless)],
        ylabel: [$I/(e Gamma_(e,0) A)$ (dimensionless)],
        lq.plot(
          (-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2),
          (0.040, 0.028, 0.008, -0.024, -0.077, -0.165, -0.310, -0.548, -0.942, -1.110, -1.220, -1.330, -1.440),
          color: accent,
          mark: "o",
          label: [idealized probe current],
        ),
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
          #html.strong[Ion-saturation region]
          #html.span[strongly negative probe bias; ion current is nearly constant]
        ]
        #html.div(class: "mhd-branches")[
          #html.div(class: "mhd-node mhd-node-ideal")[
            #html.strong[Floating potential]
            #html.span[net conventional current is zero]
          ]
          #html.div(class: "mhd-node mhd-node-ohm")[
            #html.strong[Electron retardation and saturation]
            #html.span[the electron current controls the slope and scale]
          ]
        ]
        #html.div(class: "mhd-arrow")[fit the appropriate branch before extracting plasma parameters]
      ]
      #html.figcaption[#caption-text]
    ]
  }
}
