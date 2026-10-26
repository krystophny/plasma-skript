#import "theme.typ": *
#import "@preview/physica:0.9.8": laplacian, grad
#import "debye-drawings.typ": sphere-picture, coupling-still, coupling-heading, coupling-bar
#show: deck.with(chapter: 4)
#slide(section: "debye-collective-validity", title: [Charge separation])[
  #at(1, 6, y: 4mm, sphere-picture())
  #at(7, 6, y: 6mm)[
    $Q = (4 pi)/3 r_0^3 n_0 e$
    #v(8mm) $e Phi(r_0) = (e Q)/(4 pi epsilon_0 r_0) = (n_0 e^2 r_0^2)/(3 epsilon_0)$
    #v(8mm) $e Phi(r_0) approx k_B T_e$
  ]
  #at(7, 5, y: 82mm, result-box(align(center, $r_0 approx sqrt(3) lambda_D$), [largest separated region]))
]
#animation-page("thermal-charge-fluctuations", "thermal_charge_fluctuations", section: "debye-collective-validity")
#animation-page("coupling-regions", "coupling_regions", section: "debye-collective-validity", loop: false)
#slide(section: "debye-collective-validity", title: [Weak and strong coupling])[
  #at(1, 6, align(center, coupling-heading(0)))
  #at(7, 6, align(center, coupling-heading(1)))
  #at(1, 6, y: 11mm, align(center, coupling-still(0, cols(5))))
  #at(7, 6, y: 11mm, align(center, coupling-still(1, cols(5))))
  #at(1, 3, y: 118mm, pad(left: (cols(6) - cols(5)) / 2, coupling-bar(cols(5))))
  #at(3, 8, y: 120mm, align(center, $Gamma_e = (e^2 \/ (4 pi epsilon_0 a))/(k_B T_e) = a^2/(4 pi lambda_D^2), quad a = n_0^(-1\/3)$))
]
#slide(section: "debye-collective-validity", title: [Debye number])[
  #at(1, 6, y: 14mm, align(center, $Gamma_e N_D^(2\/3) = (36 pi)^(-1\/3) approx 0.21$))
  #at(1, 6, y: 64mm, result-box(align(center, $N_D = (4 pi)/3 n_0 lambda_D^3 >> 1$), [electrons in a Debye sphere]))
  #at(7, 6, y: 4mm, plot("debye_number", columns: 6))
  #at(7, 6, y: 112mm, align(center, text(fill: muted)[$N_D prop T_e^(3\/2) n_e^(-1\/2)$; shaded: $N_D < 1$]))
]
#plot-page("nt_map", columns: 10, section: "debye-collective-validity", title: [Plasma regime map])
#slide(section: "debye-collective-validity", title: [Ideal plasma])[
  #let item(f, name) = align(center)[#text(size: result-size, f) #v(6mm) #text(fill: muted, name)]
  #at(1, 12, y: 24mm, grid(columns: (1fr, 1fr), column-gutter: gutter,
    item($N_D >> 1$, [weak coupling, collective fields]),
    item($lambda_D << L$, [quasineutral bulk; walls affect a few $lambda_D$]),
  ))
]
#animation-page("debye-shielding-particles", "debye_shielding_particles", section: "intro-debye-shielding", loop: false)
#slide(section: "intro-debye-shielding", title: [Debye shielding])[
  #let row(label, f) = ([#text(fill: muted, label)], f)
  #at(1, 12, y: 4mm, grid(columns: (auto, 1fr), column-gutter: 10mm, row-gutter: 9mm, align: (right + horizon, left + horizon),
    ..row([force balance], $0 = -k_B T_e grad n_e + e n_e grad Phi quad => quad n_e = n_0 e^(e Phi\/k_B T_e)$),
    ..row([Poisson], $-epsilon_0 laplacian Phi = e (n_0 - n_e) + Q delta(bold(r))$),
    ..row([$e Phi << k_B T_e$], $laplacian Phi - Phi/lambda_D^2 = -Q/epsilon_0 delta(bold(r)), quad lambda_D = sqrt((epsilon_0 k_B T_e)/(n_0 e^2))$),
    ..row([$Phi = a(r)\/r$], $a'' = a/lambda_D^2$),
  ))
  #at(3, 8, y: 92mm, result-box(align(center, $Phi = Q/(4 pi epsilon_0 r) e^(-r\/lambda_D)$), [Debye–Hückel potential]))
]
#slide(section: "intro-debye-shielding", title: [Dielectric function])[
  #at(1, 6, y: 0mm, align(center)[
    #text(fill: muted)[net charge / imposed charge, pattern $e^(i bold(k) dot bold(r))$] \
    #v(2mm) $1/epsilon(k) = k^2/(k^2 + 1\/lambda_D^2)$])
  #at(7, 6, y: 0mm, align(center)[
    #text(fill: muted)[potential of the test charge $Q delta(bold(r))$] \
    #v(2mm) $hat(Phi)(k) = Q/(epsilon_0 k^2 epsilon(k)) = Q/(epsilon_0 (k^2 + 1\/lambda_D^2))$])
  #at(1, 6, y: 28mm, align(center, plot("debye_surviving_fraction", columns: 5)))
  #at(7, 6, y: 28mm, align(center, plot("debye_potential_k", columns: 5)))
  #at(1, 12, y: 124mm, align(center, text(size: result-size, $epsilon(k) = 1 + 1/(k^2 lambda_D^2)$)))
  #at(1, 12, y: 148mm, align(center, text(fill: muted)[#link("https://krystophny.github.io/plasma-skript/notebooks/debye.html")[notebook: Debye shielding]]))
]
#plot-page("debye_nonlinear_potential", columns: 7, section: "intro-debye-shielding", title: [Nonlinear screening: potential],
  below: [$Lambda = q e\/(4 pi epsilon_0 lambda_D k_B T_e)$, #h(0.4em) #text(fill: muted)[$q$ test charge] \
    #v(3mm) #text(fill: muted)[linear only fails at $r lt.tilde Lambda lambda_D$, where $e Phi > k_B T_e$]])
#plot-page("debye_nonlinear_density", columns: 7, section: "intro-debye-shielding", title: [Nonlinear screening: density],
  below: [$n_e\/n_0 = e^(e Phi\/k_B T_e)$ #h(0.4em) against #h(0.4em) $1 + e Phi\/k_B T_e$ \
    #v(3mm) #text(fill: muted)[solutions of the previous page; markers: $e Phi = k_B T_e$]])
#slide(section: "intro-debye-shielding", title: [Charge separation and screening])[
  #at(1, 6, y: 0mm, align(center)[
    #text(fill: muted)[rigid: electrons removed] \
    #v(2mm) $e Phi(r_0) approx k_B T_e quad => quad r_0 approx sqrt(3) lambda_D$])
  #at(7, 6, y: 0mm, align(center)[
    #text(fill: muted)[response: mobile electrons] \
    #v(2mm) $Phi = Q/(4 pi epsilon_0 r) e^(-r\/lambda_D)$])
  #at(1, 6, y: 24mm, align(center, plot("charge_separation_energy", columns: 5)))
  #at(7, 6, y: 24mm, align(center, plot("debye_potential", columns: 5)))
  #at(1, 12, y: 122mm, align(center, text(size: result-size, $lambda_D = sqrt((epsilon_0 k_B T_e)/(n_0 e^2))$)))
]
#animation-page("coupling-test-particle", "coupling_test_particle", section: "intro-debye-shielding")
#slide(section: "intro-debye-shielding", title: [Typical scales])[
  #let examples = json("/derivations/build/debye-scales.json")
  #let sci(v) = {
    let power = calc.floor(calc.log(v, base: 10))
    let a = calc.round(v / calc.pow(10.0, power), digits: 1)
    if a == 1 { $10^#power$ } else if a == 10 { $10^#(power + 1)$ } else { $#a times 10^#power$ }
  }
  #let plain(v) = if v >= 1000 { $#calc.round(v / 1000) thin 000$ } else { $#v$ }
  #at(1, 12, y: 8mm, table(
    columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    align: (left, right, right, right, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt + muted) } else { none },
    inset: (x: 4mm, y: 4.5mm),
    [], [$n_e$ [m#super[−3]]], [$k_B T_e$ [eV]], [$lambda_D$ [m]], [$omega_(p e)$ [s#super[−1]]], [$N_D$],
    ..examples.map(r => (
      r.name, sci(r.n), plain(r.T_eV), sci(r.lambda_D), sci(r.omega_pe), sci(r.N_D),
    )).flatten(),
  ))
  #at(1, 12, y: 118mm, align(center, text(fill: muted)[$lambda_D approx 7400 "m" sqrt((k_B T_e \/ "eV")/(n_e \/ "m"^(-3)))$, #h(8mm) $omega_(p e) approx 56 thin "s"^(-1) sqrt(n_e \/ "m"^(-3))$]))
  #at(1, 12, y: 140mm, align(center, text(fill: muted)[#link("https://krystophny.github.io/plasma-skript/notebooks/scales.html")[notebook: plasma scales]]))
]
#slide(section: "intro-debye-shielding", title: [Debye length and plasma frequency])[
  #at(3, 8, y: 14mm, result-box(align(center, $lambda_D = v_("th",e)/(sqrt(2) thin omega_(p e))$), [$v_("th",e) = sqrt(2 k_B T_e\/m_e)$]))
  #at(1, 12, y: 84mm, align(center)[
    fusion plasma, $n_e = 10^20 "m"^(-3)$, $k_B T_e = 10 "keV"$: \
    #v(4mm) $v_("th",e) = 5.9 times 10^7 "m/s", quad omega_(p e) = 5.6 times 10^11 "s"^(-1) quad => quad lambda_D = 74 "µm"$
  ])
]
