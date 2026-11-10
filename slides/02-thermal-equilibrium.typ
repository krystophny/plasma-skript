#import "theme.typ": *
#import "@preview/physica:0.9.8": pdv
#import "/src/thermal-figures.typ": microstates, thermal-table
#show: deck.with(chapter: 2)
#import "thermal-drawings.typ": exchange-boxes, entropy-maximum, reservoir, ionization-picture

// Muted name under a formula, centred.
#let named(formula, name) = align(center)[#formula #v(5mm) #text(fill: muted, name)]

#build(4, slide(section: "thermal-microstates", title: [What is temperature?])[
  #set text(size: 22pt)
  #at(1, 12, y: 38mm, grid(columns: (1fr, auto, 1fr, auto, 1fr, auto, 1fr), align: center + horizon,
    named($E$, [energy]), reveal(2, $-->$),
    reveal(2, named($W(E)$, [microstates])), reveal(3, $-->$),
    reveal(3, named($S = k_B ln W$, [entropy])), reveal(4, $-->$),
    reveal(4, named(text(size: result-size, $1/T = pdv(S, E)$), [temperature])),
  ))
  #at(1, 12, y: 118mm, align(center, text(fill: muted)[$W$ multiplicity [1]#h(1.4em)$k_B$ Boltzmann constant]))
])
#build(4, slide(section: "thermal-microstates", title: [Microstate counting])[
  #at(1, 7, y: 4mm, microstates())
  #at(8, 5, y: 18mm)[
    $W_1 = 2$ #v(9mm) #reveal(2, $W_2 = 4$) #v(9mm) #reveal(3, $W_3 = 8$)
    #v(16mm)
    #reveal(4, result-box($W_3 = W_2 W_1$, [$4 times 2$, not $4 + 2$]))
  ]
])
#build(2, slide(section: "thermal-microstates", title: [Additive entropy])[
  #at(1, 12, y: 22mm, align(center, text(size: result-size)[
    $W_(A+B) = W_A W_B quad ==> quad ln W_(A+B) = ln W_A + ln W_B$
  ]))
  #at(3, 8, y: 70mm, reveal(2, result-box(align(center, $S = k_B ln W, quad S_(A+B) = S_A + S_B$), [entropy, J/K])))
])
#build(3, slide(section: "thermal-temperature", title: [Two exchanging boxes])[
  #at(1, 5, y: 14mm, exchange-boxes())
  #at(7, 6, y: 0mm, reveal(2, entropy-maximum()))
  #at(1, 12, y: 100mm, reveal(3, result-box($dif S_"tot" = (1/T_A - 1/T_B) dif E_A = 0 quad ==> quad T_A = T_B$,
    [maximum entropy: equal temperatures])))
])
#slide(section: "thermal-temperature", title: [Energy balance])[
  #at(1, 12, y: 40mm, align(center, text(size: result-size,
    $dif E = underbrace(T dif S, "heat") underbrace(- p dif V, "work")
      + underbrace(mu dif N, "particles") + underbrace(bold(u) dot dif bold(P), "bulk flow")$)))
  #at(1, 12, y: 120mm, align(center, text(fill: muted)[$p$ pressure#h(1.2em)$mu$ chemical potential#h(1.2em)$bold(u)$ bulk velocity#h(1.2em)$bold(P)$ total momentum#h(1.2em)$T > 0$]))
]
#build(4, slide(section: "thermal-boltzmann", title: [Reservoir weight])[
  #at(1, 6, y: 6mm, reservoir())
  #at(8, 5, y: 6mm)[
    $P_a prop W_"rest" (E_"tot" - E_a)$
    #v(10mm) #reveal(2, $= exp((S_"rest" (E_"tot" - E_a))/k_B)$)
    #v(10mm) #reveal(3, $S_"rest" (E_"tot" - E_a) approx S_"rest" (E_"tot") - E_a / T$)
  ]
  #at(1, 12, y: 104mm, reveal(4, result-box($P_a prop exp(-E_a/(k_B T))$, [Boltzmann factor of microstate $a$])))
])
#plot-page("boltzmann_counting", columns: 10, section: "thermal-boltzmann", title: [Boltzmann factor by counting],
  below: [$P(E) prop W_"rest" (Q - E\/epsilon), quad W_"rest" (q) = ((q + N - 1)!)/(q! thin (N - 1)!), quad k_B T = epsilon\/ln 2$ \
    #v(3mm) #text(fill: muted)[$N$ reservoir oscillators sharing $Q = N$ quanta $epsilon$; $P_B$ Boltzmann value]])
#animation-page("hard-sphere-relaxation", "hard_sphere_relaxation", section: "thermal-boltzmann")
#build(3, slide(section: "thermal-boltzmann", title: [Drifting Maxwellian])[
  #at(1, 6, y: 6mm)[
    $bold(u) = bold(P)/(N m)$
    #v(10mm) #reveal(2, $E_"kin" = bold(P)^2/(2 N m) + E_"random"$)
    #v(14mm) #reveal(3, result-box($f_s prop exp(-(bold(v) - bold(u)_s)^2/v_("th",s)^2)$, [$v_("th",s) = sqrt((2 k_B T_s)/m_s)$, §1.2]))
  ]
  #at(7, 6, reveal(3, plot("maxwellian_drift", columns: 6)))
])
#build(2, slide(section: "thermal-saha", title: [Where the slots come from])[
  #at(1, 6, y: 2mm, plot("slot_standing_wave", columns: 6))
  #at(7, 6, y: 2mm, reveal(2, plot("slot_momentum_cutoff", columns: 6)))
  #at(1, 6, y: 112mm, align(center)[$M_s approx (g_s V)/lambda_s^3, quad lambda_s = h/p_s$ #v(4mm) #text(fill: muted)[one standing wave per de Broglie cell]])
  #at(6, 7, y: 112mm, reveal(2, align(center)[$lambda_e approx h/sqrt(2 m_e k_B T)$ #h(0.6em) $-->$ #h(0.6em) $lambda_("th",e) = h/sqrt(2 pi m_e k_B T)$ #v(4mm) #text(fill: muted)[sharp cutoff → Maxwellian weight: factor $sqrt(pi)$]]))
])
#build(2, slide(section: "thermal-saha", title: [Thermal particle slots])[
  #at(1, 6, y: 10mm)[
    #result-box($M_s = (g_s V)/lambda_("th",s)^3$, [thermally available one-particle slots [1]])
    #v(12mm) $lambda_("th",s) = h/sqrt(2 pi m_s k_B T)$
    #v(10mm) #text(fill: muted)[$lambda_("th",s)$ thermal de Broglie wavelength \ $g_s$ internal states at equal energy \ $h$ Planck constant]
  ]
  #at(7, 6, y: 10mm, reveal(2, result-box($M_s/N_s = g_s/(n_s lambda_("th",s)^3) >> 1$, [dilute: many free slots per particle])))
])
#build(3, slide(section: "thermal-saha", title: [Adding and removing])[
  #at(1, 12, y: 6mm, align(center, text(size: result-size, $W_s (N_s) approx M_s^(N_s)/(N_s !)$)))
  #at(1, 6, y: 52mm, reveal(2, align(center)[
    #text(fill: muted)[add one particle] #v(8mm)
    $(W_s (N_s + 1))/(W_s (N_s)) = M_s/(N_s + 1) approx M_s/N_s$
  ]))
  #at(7, 6, y: 52mm, reveal(3, align(center)[
    #text(fill: muted)[remove one particle] #v(8mm)
    $(W_s (N_s - 1))/(W_s (N_s)) = N_s/M_s$
  ]))
  #at(1, 12, y: 122mm, align(center, text(fill: muted)[dilute and indistinguishable: $1 << N_s << M_s$]))
])
#build(5, slide(section: "thermal-saha", title: [One ionization])[
  #at(2, 10, y: 4mm, ionization-picture())
  #at(1, 12, y: 70mm, grid(columns: (1fr, 1fr, 1fr, 1fr), align: center + bottom,
    reveal(1, named($(n_n lambda_("th",n)^3)/g_n$, [remove neutral])),
    reveal(2, named($g_i/(n_i lambda_("th",i)^3)$, [add ion])),
    reveal(3, named($2/(n_e lambda_("th",e)^3)$, [add electron])),
    reveal(4, named($e^(-chi slash k_B T)$, [reservoir pays $chi$])),
  ))
  #at(1, 12, y: 128mm, reveal(5, align(center, $R = W_"after" / W_"before" = $ + [product of the four factors] + $, quad R = 1$ + [ in equilibrium])))
])
#build(3, slide(section: "thermal-saha", title: [Heavy particle cancellation])[
  #at(1, 12, y: 14mm, align(center)[$m_n approx m_i quad ==> quad lambda_("th",n) approx lambda_("th",i)$])
  #at(1, 12, y: 44mm, reveal(2, align(center, text(size: result-size,
    $R approx underbrace((n_n g_i)/(n_i g_n), "neutral" arrow.r "ion") dot underbrace(2/(n_e lambda_("th",e)^3), "new free electron") dot e^(-chi slash k_B T)$))))
  #at(1, 12, y: 124mm, reveal(3, align(center, text(fill: muted)[the genuinely new freedom is the free electron])))
])
#slide(section: "thermal-saha", title: [Saha equation])[
  #at(1, 12, y: 26mm, align(center, text(size: 30pt,
    $underbrace((n_i n_e)/n_n, "composition") = underbrace(2/lambda_("th",e)^3, "free-electron states")
      dot underbrace(g_i/g_n, "internal states") dot underbrace(e^(-chi slash k_B T), "energy penalty")$)))
  #at(1, 12, y: 118mm, align(center, text(fill: muted)[$chi$ ionization energy#h(1.4em)$g_i = g_n = 1$ here: order-one factors]))
]
#build(3, slide(section: "thermal-saha", title: [Saha equation in numbers])[
  #at(1, 12, y: 22mm, align(center, text(size: result-size,
    $(n_i n_e)/n_n = 2 ((2 pi m_e k_B T)/h^2)^(3 slash 2) e^(-chi slash k_B T)$)))
  #at(1, 12, y: 78mm, reveal(2, align(center,
    $2 ((2 pi m_e k_B)/h^2)^(3 slash 2) = 4.83 times 10^21 "m"^(-3) "K"^(-3 slash 2)$)))
  #at(1, 12, y: 112mm, reveal(3, align(center, text(fill: muted)[hydrogen: $chi = 13.6 "eV"$, $chi / k_B = 1.58 times 10^5 "K"$])))
])
#plot-page("saha_fraction_deck", columns: 8, section: "thermal-ionization", title: [Ionization fraction],
  below: [$x = n_i/(n_i + n_n), quad n_e = n_i, quad x^2/(1 - x) = 1/n dot 2/lambda_("th",e)^3 e^(-chi slash k_B T)$])
#plot-page("saha_factors", columns: 8, section: "thermal-ionization", title: [Entropy against energy],
  below: [half ionization where the free-electron states pay the energy penalty])
#build(3, slide(section: "thermal-ionization", title: [Why about $10^4$ K?])[
  #at(1, 6, y: 6mm)[
    #result-box($k_B T_(1 slash 2) = chi / ln(4 slash n lambda_("th",e)^3)$, [half ionization, $chi = 13.6 "eV"$])
    #v(12mm)
    #reveal(2, $ln(4 slash n lambda_("th",e)^3) approx 10 dots 50$)
    #v(8mm)
    #reveal(3, $n = 10^18 dots 10^24 "m"^(-3): quad T_(1 slash 2) approx 7000 dots 16000 "K"$)
    #v(8mm)
    #reveal(3, text(fill: muted)[logarithm: weak dependence on density])
  ]
  #at(7, 6, y: 6mm, context if shown(3) {
    let data = json("/derivations/build/thermal-ionization.json")
    set text(size: 16pt)
    data-table(
      ([$n$ [m#super[−3]]], [$T_(1 slash 2)$ [K]], [$k_B T_(1 slash 2)$ [eV]], [$chi slash k_B T_(1 slash 2)$]),
      data.rows.map(r => (
        [$10^#str(r.exponent)$], [#str(int(calc.round(r.T / 100) * 100))],
        [#calc.round(r.kT, digits: 2)], [#calc.round(r.log, digits: 0)],
      )),
    )
  })
])
#slide(section: "thermal-ionization", title: [Saha in a tokamak divertor])[
  #at(1, 12, y: -4mm, image("/derivations/build/fig/saha_cmod.svg", width: cols(12)))
  #at(1, 12, y: 128mm, text(size: small-size, fill: muted)[
    Excited deuterium levels in the detached Alcator C-Mod divertor, measured from Balmer lines, against Saha–Boltzmann
    at the measured $k_B T_e$ and Stark $n_e$ (band: their uncertainty ranges). Data redrawn from D. Lumma, J. L. Terry,
    B. Lipschultz, Phys. Plasmas 4, 2555 (1997), doi:10.1063/1.872234; bars: digitization only.])
]
#build(3, slide(section: "thermal-ionization", title: [Equilibrium validity])[
  #at(1, 12, y: 10mm, grid(columns: (1fr,1fr), column-gutter: gutter, row-gutter: 22mm,
    [Saha \ local thermodynamic equilibrium], [dilute radiation escape \ coronal / collisional-radiative balance],
    reveal(2)[solar corona; tokamak edge \ many laboratory discharges], reveal(2)[nonthermal electrons; photons \ rate-dependent ionization],
    reveal(3)[high density \ pressure ionization], reveal(3)[ideal slots \ $n_s lambda_("th",s)^3/g_s << 1$],
  ))
])
#build(2, slide(section: "thermal-ionization", title: [Quantum degenerate plasma])[
  #at(1, 4, y: 6mm)[
    #result-box($(n_e lambda_("th",e)^3)/2 gt.tilde 1$, [slots full: Pauli exclusion, Fermi statistics])
    #v(10mm) $(n_e lambda_("th",e)^3)/2 << 1$ #h(0.5em) classical plasma
    #v(8mm) #text(fill: muted)[same slot count as in the Saha equation]
  ]
  #at(5, 8, y: 6mm, reveal(2, {
    set text(size: 16pt)
    data-table(
      ([plasma], [$n_e$ [m#super[−3]]], [$T$], [$n_e lambda_("th",e)^3 slash 2$]),
      (
        ([tokamak core], [$10^20$], [10 keV], [$2 times 10^(-14)$]),
        ([compressed ICF fuel], [$2 times 10^32$], [200 eV], [$10$]),
        ([electrons in copper], [$8.5 times 10^28$], [300 K], [$3 times 10^3$]),
        ([white dwarf], [$10^36$], [$10^7$ K], [$7 times 10^3$]),
      ),
      align: (left, right, right, right),
    )
  }))
])
#credits-page((), [Physics: Reif (1965); Saha (1920), DOI 10.1080/14786441008636148. \ Constants: NIST CODATA 2022. \ Original diagrams and computed plots: Christopher Albert, CC BY 4.0.])
