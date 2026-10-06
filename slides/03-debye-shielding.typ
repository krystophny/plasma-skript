#import "theme.typ": *
#import "@preview/physica:0.9.8": laplacian, dv
#show: deck.with(chapter: 3)
#animation-page("debye-shielding", "debye_shielding", section: "intro-debye-shielding", loop: false)
#slide(section: "intro-debye-shielding", title: [Boltzmann electrons])[
  #at(1, 6, y: 10mm)[
    #diagram(spacing: 25mm, node((0,0), [positive $phi$]), edge("-|>"),
      node((0,1), [electron energy $-e phi$]), edge("-|>"), node((0,2), [more electrons]))
  ]
  #at(7, 6, y: 22mm)[
    #result-box($n_e = n_0 exp((e phi)/(k_B T_e))$, [Boltzmann weight: chapter 2])
    #v(12mm) $n_i = n_0, quad T_e = "const"$
    #v(10mm) #text(fill: muted)[$n_0$ background density \ $phi$ electric potential]
  ]
]
#slide(section: "intro-debye-shielding", title: [Linear response])[
  #at(1, 6, y: 10mm)[
    $abs(e phi)/(k_B T_e) << 1$
    #v(12mm) $exp(y) approx 1+y$
    #v(12mm) $n_e approx n_0 (1+(e phi)/(k_B T_e))$
    #v(12mm) #result-box($rho_q approx -(n_0 e^2 phi)/(k_B T_e)$, [restoring charge response])
  ]
  #at(7, 6, plot("enclosed_charge", columns: 6))
]
#slide(section: "intro-debye-shielding", title: [Screened Poisson equation])[
  #at(1, 12, y: 10mm, grid(columns: (1fr,1fr), column-gutter: gutter, row-gutter: 15mm,
    [$laplacian phi = -rho_q/epsilon_0$], [$rho_q approx -(n_0 e^2 phi)/(k_B T_e)$],
    [$laplacian phi - phi/lambda_D^2 = 0$],
    result-box($lambda_D = sqrt((epsilon_0 k_B T_e)/(n_0 e^2))$, [Debye length]),
  ))
  #at(1, 12, y: 115mm)[$r>0, quad phi(r -> infinity) -> 0$ \ $n_0$: $"m"^(-3)$; $k_B T_e$: J; $lambda_D$: m]
]
#slide(section: "intro-debye-shielding", title: [Yukawa potential])[
  #at(1, 6, y: 8mm)[
    $phi = w/r$ \ $dv(w,r,2) = w/lambda_D^2$
    #v(10mm) $w prop exp(-r/lambda_D)$
    #v(10mm) #result-box($phi(r)=Q/(4 pi epsilon_0 r) exp(-r/lambda_D)$, [screened point charge])
    #v(8mm) #text(fill: muted)[$Q$ source charge; $r$ radius]
  ]
  #at(7, 6, plot("debye_potential", columns: 6))
]
#slide(section: "intro-debye-shielding", title: [Charge separation scale])[
  #at(1, 6, y: 10mm)[
    $Q = (4 pi)/3 R^3 n_0 e$
    #v(12mm) $phi(R)=Q/(4 pi epsilon_0 R)$
    #v(12mm) $e phi(R) approx k_B T_e$
    #v(12mm) #result-box($R approx sqrt(3) lambda_D$, [thermal energy balance])
  ]
  #at(7, 6, plot("debye_sphere_potential", columns: 6))
]
#animation-page("debye-potential-reduction", "debye_potential_reduction", section: "debye-finite-source")
#slide(section: "debye-finite-source", title: [Finite source response])[
  #at(1, 6, y: 8mm)[
    $rho_Q = (3 Q)/(4 pi R^3)$
    #v(10mm) $laplacian phi-phi/lambda_D^2=-rho_Q/epsilon_0$ \ $r<R$
    #v(10mm) $laplacian phi-phi/lambda_D^2=0$ \ $r>R$
    #v(10mm) $phi(R^-)=phi(R^+)$ \ $dv(phi,r)|_(R^-)=dv(phi,r)|_(R^+)$
  ]
  #at(7, 6)[
    #result-box($phi_"out" prop exp(-r/lambda_D)/r$, [same screened tail])
    #v(8mm) #plot("debye_sphere_potential", columns: 6)
  ]
]
#animation-page("debye-shielding-particles", "debye_shielding_particles", section: "debye-finite-source", loop: false)
#slide(section: "debye-collective-validity", title: [Debye sphere count])[
  #at(1, 6, align(center)[$N_D approx 3$ [1]])
  #at(7, 6, align(center)[$N_D approx 300$ [1]])
  #at(1, 6, y: 14mm, debye-sphere(3,11,3.4mm,exact: true))
  #at(7, 6, y: 14mm, debye-sphere(300,5,1.5mm))
  #at(1, 12, y: 140mm)[$N_D = (4 pi)/3 n_e lambda_D^3$ [1]]
]
#slide(section: "debye-collective-validity", title: [Weak coupling])[
  #at(1, 6, y: 8mm)[
    $(4 pi)/3 a^3 n_0 = 1$
    #v(10mm) $Gamma = e^2/(4 pi epsilon_0 a k_B T_e)$
    #v(10mm) $Gamma N_D^(2/3)=1/3$
    #v(10mm) #result-box($N_D >> 1 quad <==> quad Gamma << 1$, [many particles; weak pair energy])
    #v(8mm) #text(fill: muted)[$a$ mean spacing; $Gamma$ [1]]
  ]
  #at(7, 6, plot("debye_number", columns: 6))
]
#plot-page("nt_map", columns: 10, section: "debye-collective-validity", title: [Plasma regime map],
  below: [$lambda_D << L, quad N_D >> 1$])
#slide(section: "debye-collective-validity", title: [Ideal plasma])[
  #let item(f, name) = align(center)[#text(size: result-size, f) #v(5mm) #text(fill: muted, name)]
  #at(1, 12, y: 14mm, grid(columns: (1fr, 1fr, 1fr), row-gutter: 26mm,
    item($lambda_D << L$, [quasineutral in bulk]), item($N_D >> 1$, [collective, smooth fields]),
    item($Gamma << 1$, [weak coupling]),
    item($n_e lambda_("th",e)^3 << 1$, [classical statistics (chapter 2)]),
    item($omega_(p e) tau >> 1$, [collective faster than collisions]),
    item($T gt.tilde 10^4 "K"$, [mostly ionized (Saha)]),
  ))
]
#credits-page((), [Original figures and animation: Christopher Albert, CC BY 4.0. \ Physics: Chen (2016); Bittencourt (2004).])
