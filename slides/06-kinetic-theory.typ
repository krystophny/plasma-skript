#import "theme.typ": *
#import "@preview/physica:0.9.8": dv, pdv, grad, div
#show: deck.with(chapter: 6)
// Row i appears at build step i + 1, or at steps.at(i); outside a build all show.
#let step-of(i, steps) = if steps == auto { i + 1 } else { steps.at(i) }
#let row(k, label, f) = (reveal(k, text(fill: muted, label)), reveal(k, f))
#let formula-rows(..items, gap: 8mm, steps: auto) = grid(columns: (auto, 1fr), column-gutter: 8mm, row-gutter: gap,
  align: (right + horizon, left + horizon), ..items.pos().enumerate().map(((i, r)) => row(step-of(i, steps), ..r)).flatten())
#let note(body) = text(fill: muted, body)
#let symbols(body) = at(1, 12, y: 146mm, note(body))
#let D = math.upright("D")
#let arnold = [V. I. Arnold, _Mathematical Methods of Classical Mechanics_, 2nd ed., Springer (1989), §16, #link("https://doi.org/10.1007/978-1-4757-2063-1")[doi:10.1007/978-1-4757-2063-1]]

// ------------------------------------------------ 1 Lagrange and Euler
#slide(section: "kinetic-derivatives", title: [Lagrangian and Eulerian descriptions])[
  #at(1, 12, y: -8mm, plot("flow_lagrange_euler", columns: 12))
  #at(1, 6, y: 125mm, align(center)[#note[Lagrange: follow a parcel] \ $dot(bold(x)) = bold(u)(bold(x), t), quad bold(x)(0) = bold(x)_0$])
  #at(7, 6, y: 125mm, align(center)[#note[Euler: fields at fixed $bold(x)$] \ $bold(u)(bold(x), t), quad g(bold(x), t)$ #h(4mm) #note[steady: $pdv(bold(u), t) = 0$]])
  #symbols[$bold(u)$ flow velocity · $bold(x)_0$ start · $g$ carried quantity · $bold(u) = (sin pi x cos pi y, -cos pi x sin pi y)$ · dots: equal time steps]
]

// ------------------------------------------------ 2 advection operator
#build(3, slide(section: "kinetic-derivatives", title: [Advection operator])[
  #at(1, 12, y: 0mm, plot("advection_probe", columns: 12))
  #at(1, 12, y: 106mm, formula-rows(gap: 7mm,
    ([along the parcel], $dv(, t) g(bold(x)(t), t) = pdv(g, t) + bold(u) dot grad g equiv (#D g)/(#D t)$),
    ([carried unchanged], $(#D g)/(#D t) = 0 quad => quad pdv(g, t) = - bold(u) dot grad g$),
  ))
  #symbols[bump $g(x, t) = g_0(x - u t)$, $u$ constant · $x_p$ fixed probe · $#D \/ #D t = partial_t + bold(u) dot grad$ advection operator]
])

// ------------------------------------------------ 3 volume under a flow
#slide(section: "kinetic-derivatives", title: [Volume carried by a flow])[
  #at(1, 12, y: -6mm, plot("volume_flow", columns: 12))
  #at(1, 12, y: 128mm, align(center)[numbers: area $A(t) \/ A(0)$ of the same parcels #h(6mm) #note[grey, blue, orange: increasing $t$]])
  #symbols[left: cellular flow, $t = 0, 0.6, 1.2$ · right: $bold(u) = (0.6 sin pi x, 0)$, $t = 0, 0.9, 2.2$ · areas from the computed boundary]
]

// ------------------------------------------------ 4 Liouville, after Arnold
#build(6, slide(section: "kinetic-derivatives", title: [Volume change of a flow])[
  #at(1, 12, y: 0mm, formula-rows(gap: 7mm,
    ([flow map], $g^t: bold(x)_0 |-> bold(x)(t), quad D(t) = g^t D(0)$),
    ([volume], $V(t) = integral_(D(0)) det (partial bold(x)) / (partial bold(x)_0) dif^n x_0$),
    ([short time], $(partial bold(x)) / (partial bold(x)_0) = I + t A + O(t^2), quad A = (partial bold(u)) / (partial bold(x))$),
    ([determinant], $det(I + t A) = 1 + t tr A + O(t^2), quad tr A = div bold(u)$),
    ([rate], $dv(V, t) = integral_(D(t)) div bold(u) dif^n x$),
  ))
  #at(2, 10, y: 100mm, reveal(6, result-box($div bold(u) = 0 quad <=> quad V(t) = V(0) "for every" D$,
    [divergence-free flow: incompressible])))
  #at(1, 12, y: 146mm, text(size: 12pt, fill: muted, arnold))
])

// ------------------------------------------------ 5 distribution function
#slide(section: "kinetic-distribution", title: [Distribution function])[
  #at(1, 12, y: -4mm, plot("distribution_cells", columns: 12))
  #at(1, 12, y: 126mm, align(center)[$dif N = f(bold(r), bold(v), t) dif^3 r dif^3 v$ #h(14mm) $n(bold(r), t) = integral f dif^3 v$])
  #symbols[3000 sampled particles, $n(x) prop 1 + 0.6 sin 2 pi x$, Maxwellian in $v$ · $Delta N approx f Delta x Delta v$ · margins: histograms and exact curves]
]

// ------------------------------------------------ 6 phase-space flow
#slide(section: "kinetic-derivatives", title: [Flow in phase space])[
  #at(1, 12, y: -6mm, plot("phase_space_flow", columns: 12))
  #at(1, 6, y: 119mm, align(center)[#note[free streaming] #h(3mm) $dot(x) = v, quad dot(v) = 0$])
  #at(7, 6, y: 119mm, align(center)[#note[$bold(E) perp bold(B)$, ion] #h(3mm) $dot(bold(v)) = q/m (bold(E) + bold(v) times bold(B))$])
  #at(1, 12, y: 133mm, align(center)[$bold(z) = (bold(r), bold(v)), quad dot(bold(z)) = (bold(v), bold(a)), quad div_bold(z) dot(bold(z)) = div_bold(r) bold(v) + div_bold(v) bold(a) = 0$])
  #symbols[numbers: phase-space area relative to $t = 0$ · $bold(v)_E = bold(E) times bold(B) \/ B^2$ · $div_bold(v) (bold(v) times bold(B)) = 0$]
]

// ------------------------------------------------ 7 external fields only
#slide(section: "kinetic-boltzmann", title: [Non-interacting particles in a given field])[
  #at(1, 12, y: -4mm, plot("vlasov_well", columns: 12))
  #at(1, 12, y: 132mm, align(center)[$f(bold(z), t) = f_0 (bold(z)_0 (bold(z), t))$ #h(6mm) #note[$bold(z)_0$: start of the orbit through $bold(z)$ at $t$]])
  #symbols[pendulum well $dot(x) = v$, $dot(v) = -omega_0^2 sin x$ · dashed: separatrix · $f_0$ Gaussian · $n = integral f dif v$]
]

// ------------------------------------------------ 8 Vlasov, given fields
#build(4, slide(section: "kinetic-boltzmann", title: [Vlasov equation for given fields])[
  #at(1, 12, y: 0mm, formula-rows(gap: 8mm,
    ([particle number], $pdv(f, t) + div_bold(z) (f dot(bold(z))) = 0$),
    ([product rule], $div_bold(z) (f dot(bold(z))) = dot(bold(z)) dot grad_bold(z) f + f div_bold(z) dot(bold(z)), quad div_bold(z) dot(bold(z)) = 0$),
    ([along orbits], $(#D f)/(#D t) = pdv(f, t) + bold(v) dot grad f + bold(a) dot pdv(f, bold(v)) = 0$),
  ))
  #at(1, 12, y: 92mm, reveal(4, result-box($pdv(f, t) + bold(v) dot grad f + q/m (bold(E) + bold(v) times bold(B)) dot pdv(f, bold(v)) = 0$,
    [$bold(E)$, $bold(B)$ given: $f$ constant along each orbit])))
])

// ------------------------------------------------ 9 delta peaks
#build(3, slide(section: "kinetic-distribution", title: [Many particles as delta peaks])[
  #at(1, 12, y: 6mm, formula-rows(gap: 12mm,
    ([Klimontovich], $N(bold(z), t) = sum_(i = 1)^N delta(bold(z) - bold(z)_i (t))$),
    ([each peak on its orbit], $pdv(N, t) + dot(bold(z)) dot grad_bold(z) N = 0$),
    ([smoothing], $f_h = K_h * N = integral K_h (bold(z) - bold(z)') N(bold(z)', t) dif bold(z)'$),
  ))
  #symbols[$bold(z)_i (t)$ orbit of particle $i$ · $K_h$ kernel of width $h$, $integral K_h = 1$ · given fields: same equation as for $f$]
])
#animation-page("kernel-smoothing", "kernel_smoothing", section: "kinetic-distribution", loop: false)
#animation-page("kernel-width", "kernel_width", section: "kinetic-distribution", loop: false)

// ------------------------------------------------ 10 smoothing vs advection
#slide(section: "kinetic-boltzmann", title: [Smoothing and advection])[
  #at(1, 12, y: 0mm, plot("smoothing_advection", columns: 12))
  #at(1, 12, y: 108mm, align(center)[advect the peaks, then smooth #h(4mm) $K_h * N(t) approx f(t)$ #h(4mm) advect $f$])
  #symbols[same well and $f_0$ as before, $omega_0 t = 8$ · Gaussian $K_h$ in $(x, v)$ · filaments thinner than $h$ blur · noise $prop N_h^(-1\/2)$]
]

// ------------------------------------------------ 11 many-particle marginal
#build(4, slide(section: "kinetic-boltzmann", title: [Many-particle distribution and its marginal])[
  #at(1, 6, y: -4mm, plot("pair_marginal", columns: 6))
  #at(7, 6, y: 4mm, formula-rows(gap: 10mm,
    ([$N$ particles], $F_N (bold(z)_1, dots, bold(z)_N, t)$),
    ([Liouville], $pdv(F_N, t) + sum_i dot(bold(z))_i dot grad_(bold(z)_i) F_N = 0$),
    ([marginal], $f_1 (bold(z)_1) = N integral F_N dif bold(z)_2 dots dif bold(z)_N$),
    ([uncorrelated], $F_N = product_i f_1 (bold(z)_i) \/ N$),
  ))
  #symbols[$F_N$ probability density on the $6 N$-dimensional phase space · figure: $N = 2$ on a periodic line, $F_2 = 1$ and $F_2 = 1 + c(x_1 - x_2)$: same $f_1$]
])
