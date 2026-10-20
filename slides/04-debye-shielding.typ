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
#animation-page("coupling-test-particle", "coupling_test_particle", section: "debye-collective-validity")
#slide(section: "debye-collective-validity", title: [Weak and strong coupling])[
  #at(1, 6, align(center, coupling-heading(0, [strong])))
  #at(7, 6, align(center, coupling-heading(1, [weak])))
  #at(1, 6, y: 13mm, coupling-still(0, cols(6)))
  #at(7, 6, y: 13mm, coupling-still(1, cols(6)))
  #at(1, 2, y: 112mm, coupling-bar(cols(6)))
  #at(3, 8, y: 116mm, align(center, $Gamma_e = (e^2 \/ (4 pi epsilon_0 a))/(k_B T_e) = a^2/(4 pi lambda_D^2), quad a = n_0^(-1\/3)$))
]
#slide(section: "debye-collective-validity", title: [Debye number])[
  #at(2, 10, y: 14mm, align(center, $Gamma_e N_D^(2\/3) = (36 pi)^(-1\/3) approx 0.21$))
  #at(3, 8, y: 84mm, result-box(align(center, $N_D = (4 pi)/3 n_0 lambda_D^3 >> 1$), [electrons in a Debye sphere]))
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
#slide(section: "intro-debye-shielding", title: [Debye length and plasma frequency])[
  #at(3, 8, y: 14mm, result-box(align(center, $lambda_D = v_("th",e)/(sqrt(2) thin omega_(p e))$), [$v_("th",e) = sqrt(2 k_B T_e\/m_e)$]))
  #at(1, 12, y: 84mm, align(center)[
    fusion plasma, $n_e = 10^20 "m"^(-3)$, $k_B T_e = 10 "keV"$: \
    #v(4mm) $v_("th",e) = 5.9 times 10^7 "m/s", quad omega_(p e) = 5.6 times 10^11 "s"^(-1) quad => quad lambda_D = 74 "µm"$
  ])
]
