#import "theme.typ": *
#import "@preview/physica:0.9.8": laplacian, grad
#import "debye-drawings.typ": sphere-picture
#show: deck.with(chapter: 4)
#slide(section: "intro-debye-shielding", title: [Charge separation])[
  #at(1, 6, y: 4mm, sphere-picture())
  #at(7, 6, y: 6mm)[
    $Q = (4 pi)/3 r_0^3 n_0 e$
    #v(8mm) $e Phi(r_0) = (e Q)/(4 pi epsilon_0 r_0) = (n_0 e^2 r_0^2)/(3 epsilon_0)$
    #v(8mm) $e Phi(r_0) approx k_B T_e$
  ]
  #at(7, 5, y: 82mm, result-box(align(center, $r_0 approx sqrt(3) lambda_D$), [largest separated region]))
]
#slide(section: "intro-debye-shielding", title: [Weak and strong coupling])[
  #at(1, 6, align(center)[$lambda_D tilde a$: strong])
  #at(7, 6, align(center)[$lambda_D >> a$: weak])
  #at(1, 6, y: 14mm, debye-sphere(1, 11, 3.4mm, exact: true))
  #at(7, 6, y: 14mm, debye-sphere(30, 5, 2.2mm))
  #at(3, 8, y: 132mm, align(center, $Gamma = (e^2 \/ (4 pi epsilon_0 a))/(k_B T_e) = a^2/(4 pi lambda_D^2), quad a = n_0^(-1\/3)$))
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
#slide(section: "debye-collective-validity", title: [Plasma parameter])[
  #let row(label, f) = ([#text(fill: muted, label)], f)
  #at(1, 12, y: 4mm, grid(columns: (auto, 1fr), column-gutter: 10mm, row-gutter: 10mm, align: (right + horizon, left + horizon),
    ..row([mean spacing], $a approx n_0^(-1\/3)$),
    ..row([weak coupling], $e^2/(4 pi epsilon_0 a) << k_B T_e = (n_0 e^2 lambda_D^2)/epsilon_0$),
    ..row([], $1 << 4 pi n_0^(2\/3) lambda_D^2$),
  ))
  #at(3, 8, y: 84mm, result-box(align(center, $N_D = (4 pi)/3 n_0 lambda_D^3 >> 1$), [electrons in a Debye sphere]))
]
#slide(section: "debye-collective-validity", title: [Debye sphere count])[
  #at(1, 6, align(center)[$N_D approx 3$])
  #at(7, 6, align(center)[$N_D approx 300$])
  #at(1, 6, y: 14mm, debye-sphere(3, 11, 3.4mm, exact: true))
  #at(7, 6, y: 14mm, debye-sphere(300, 5, 1.5mm))
]
#plot-page("nt_map", columns: 10, section: "debye-collective-validity", title: [Plasma regime map])
#slide(section: "debye-collective-validity", title: [Ideal plasma])[
  #let item(f, name) = align(center)[#text(size: result-size, f) #v(6mm) #text(fill: muted, name)]
  #at(1, 12, y: 24mm, grid(columns: (1fr, 1fr), column-gutter: gutter,
    item($N_D >> 1$, [weak coupling, collective fields]),
    item($lambda_D << L$, [quasineutral bulk; walls affect a few $lambda_D$]),
  ))
]
