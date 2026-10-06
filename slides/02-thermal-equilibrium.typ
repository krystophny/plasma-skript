#import "theme.typ": *
#import "@preview/physica:0.9.8": pdv
#import "/src/thermal-figures.typ": microstates, thermal-table
#show: deck.with(chapter: 2)
#import "thermal-drawings.typ": exchange-boxes, entropy-maximum, reservoir, ionization-picture

// Muted name under a formula, centred.
#let named(formula, name) = align(center)[#formula #v(5mm) #text(fill: muted, name)]

#slide(section: "thermal-microstates", title: [What is temperature?])[
  #set text(size: 22pt)
  #at(1, 12, y: 38mm, grid(columns: (1fr, auto, 1fr, auto, 1fr, auto, 1fr), align: center + horizon,
    named($E$, [energy]), $-->$,
    named($W(E)$, [microstates]), $-->$,
    named($S = k_B ln W$, [entropy]), $-->$,
    named(text(size: result-size, $1/T = pdv(S, E)$), [temperature]),
  ))
  #at(1, 12, y: 118mm, align(center, text(fill: muted)[$W$ multiplicity [1]#h(1.4em)$k_B$ Boltzmann constant]))
]
#slide(section: "thermal-microstates", title: [Microstate counting])[
  #at(1, 7, y: 4mm, microstates())
  #at(8, 5, y: 18mm)[
    $W_1 = 2$ #v(9mm) $W_2 = 4$ #v(9mm) $W_3 = 8$
    #v(16mm)
    #result-box($W_3 = W_2 W_1$, [$4 times 2$, not $4 + 2$])
  ]
]
#slide(section: "thermal-microstates", title: [Additive entropy])[
  #at(1, 12, y: 22mm, align(center, text(size: result-size)[
    $W_(A+B) = W_A W_B quad ==> quad ln W_(A+B) = ln W_A + ln W_B$
  ]))
  #at(3, 8, y: 70mm, result-box(align(center, $S = k_B ln W, quad S_(A+B) = S_A + S_B$), [entropy, J/K]))
]
#slide(section: "thermal-temperature", title: [Two exchanging boxes])[
  #at(1, 5, y: 14mm, exchange-boxes())
  #at(7, 6, y: 0mm, entropy-maximum())
  #at(1, 12, y: 100mm, result-box($dif S_"tot" = (1/T_A - 1/T_B) dif E_A = 0 quad ==> quad T_A = T_B$,
    [maximum entropy: equal temperatures]))
]
#slide(section: "thermal-temperature", title: [Energy balance])[
  #at(1, 12, y: 40mm, align(center, text(size: result-size,
    $dif E = underbrace(T dif S, "heat") underbrace(- p dif V, "work")
      + underbrace(mu dif N, "particles") + underbrace(bold(u) dot dif bold(P), "bulk flow")$)))
  #at(1, 12, y: 120mm, align(center, text(fill: muted)[$p$ pressure#h(1.2em)$mu$ chemical potential#h(1.2em)$bold(u)$ bulk velocity#h(1.2em)$bold(P)$ total momentum#h(1.2em)$T > 0$]))
]
#slide(section: "thermal-boltzmann", title: [Reservoir weight])[
  #at(1, 6, y: 6mm, reservoir())
  #at(8, 5, y: 6mm)[
    $P_a prop W_"rest" (E_"tot" - E_a)$
    #v(10mm) $= exp((S_"rest" (E_"tot" - E_a))/k_B)$
    #v(10mm) $S_"rest" (E_"tot" - E_a) approx S_"rest" (E_"tot") - E_a / T$
  ]
  #at(1, 12, y: 104mm, result-box($P_a prop exp(-E_a/(k_B T))$, [Boltzmann factor of microstate $a$]))
]
#slide(section: "thermal-boltzmann", title: [Drifting Maxwellian])[
  #at(1, 6, y: 6mm)[
    $bold(u) = bold(P)/(N m)$
    #v(10mm) $E_"kin" = bold(P)^2/(2 N m) + E_"random"$
    #v(14mm) #result-box($f_s prop exp(-(bold(v) - bold(u)_s)^2/v_("th",s)^2)$, [$v_("th",s) = sqrt((2 k_B T_s)/m_s)$, §1.2])
  ]
  #at(7, 6, plot("maxwellian_drift", columns: 6))
]
#slide(section: "thermal-saha", title: [Thermal particle slots])[
  #at(1, 6, y: 10mm)[
    #result-box($M_s = (g_s V)/lambda_("th",s)^3$, [thermally available one-particle slots [1]])
    #v(12mm) $lambda_("th",s) = h/sqrt(2 pi m_s k_B T)$
    #v(10mm) #text(fill: muted)[$lambda_("th",s)$ thermal de Broglie wavelength \ $g_s$ internal states at equal energy \ $h$ Planck constant]
  ]
  #at(7, 6, y: 10mm)[
    #result-box($M_s/N_s = g_s/(n_s lambda_("th",s)^3) >> 1$, [dilute: many free slots per particle])
  ]
]
#slide(section: "thermal-saha", title: [Adding and removing])[
  #at(1, 12, y: 6mm, align(center, text(size: result-size, $W_s (N_s) approx M_s^(N_s)/(N_s !)$)))
  #at(1, 6, y: 52mm, align(center)[
    #text(fill: muted)[add one particle] #v(8mm)
    $(W_s (N_s + 1))/(W_s (N_s)) = M_s/(N_s + 1) approx M_s/N_s$
  ])
  #at(7, 6, y: 52mm, align(center)[
    #text(fill: muted)[remove one particle] #v(8mm)
    $(W_s (N_s - 1))/(W_s (N_s)) = N_s/M_s$
  ])
  #at(1, 12, y: 122mm, align(center, text(fill: muted)[dilute and indistinguishable: $1 << N_s << M_s$]))
]
#slide(section: "thermal-saha", title: [One ionization])[
  #at(2, 10, y: 4mm, ionization-picture())
  #at(1, 12, y: 70mm, grid(columns: (1fr, 1fr, 1fr, 1fr), align: center + bottom,
    named($(n_n lambda_("th",n)^3)/g_n$, [remove neutral]),
    named($g_i/(n_i lambda_("th",i)^3)$, [add ion]),
    named($2/(n_e lambda_("th",e)^3)$, [add electron]),
    named($e^(-chi slash k_B T)$, [reservoir pays $chi$]),
  ))
  #at(1, 12, y: 128mm, align(center, $R = W_"after" / W_"before" = $ + [product of the four factors] + $, quad R = 1$ + [ in equilibrium]))
]
#slide(section: "thermal-saha", title: [Heavy particle cancellation])[
  #at(1, 12, y: 14mm, align(center)[$m_n approx m_i quad ==> quad lambda_("th",n) approx lambda_("th",i)$])
  #at(1, 12, y: 44mm, align(center, text(size: result-size,
    $R approx underbrace((n_n g_i)/(n_i g_n), "neutral" arrow.r "ion") dot underbrace(2/(n_e lambda_("th",e)^3), "new free electron") dot e^(-chi slash k_B T)$)))
  #at(1, 12, y: 124mm, align(center, text(fill: muted)[the genuinely new freedom is the free electron]))
]
#slide(section: "thermal-saha", title: [Saha equation])[
  #at(1, 12, y: 26mm, align(center, text(size: 30pt,
    $underbrace((n_i n_e)/n_n, "composition") = underbrace(2/lambda_("th",e)^3, "free-electron states")
      dot underbrace(g_i/g_n, "internal states") dot underbrace(e^(-chi slash k_B T), "energy penalty")$)))
  #at(1, 12, y: 118mm, align(center, text(fill: muted)[$chi$ ionization energy#h(1.4em)$g_i = g_n = 1$ here: order-one factors]))
]
#slide(section: "thermal-saha", title: [Saha equation in numbers])[
  #at(1, 12, y: 22mm, align(center, text(size: result-size,
    $(n_i n_e)/n_n = 2 ((2 pi m_e k_B T)/h^2)^(3 slash 2) e^(-chi slash k_B T)$)))
  #at(1, 12, y: 78mm, align(center,
    $2 ((2 pi m_e k_B)/h^2)^(3 slash 2) = 4.83 times 10^21 "m"^(-3) "K"^(-3 slash 2)$))
  #at(1, 12, y: 112mm, align(center, text(fill: muted)[hydrogen: $chi = 13.6 "eV"$, $chi / k_B = 1.58 times 10^5 "K"$]))
]
#plot-page("saha_fraction", columns: 8, section: "thermal-ionization", title: [Ionization fraction],
  below: [$x = n_i/(n_i + n_n), quad n_e = n_i, quad x^2/(1 - x) = 1/n dot 2/lambda_("th",e)^3 e^(-chi slash k_B T)$])
#plot-page("saha_factors", columns: 8, section: "thermal-ionization", title: [Entropy against energy],
  below: [half ionization where the free-electron states pay the energy penalty])
#slide(section: "thermal-ionization", title: [Why about $10^4$ K?])[
  #at(1, 6, y: 6mm)[
    #result-box($k_B T_(1 slash 2) = chi / ln(4 slash n lambda_("th",e)^3)$, [half ionization, $chi = 13.6 "eV"$])
    #v(12mm)
    $ln(4 slash n lambda_("th",e)^3) approx 10 dots 50$
    #v(8mm)
    $n = 10^18 dots 10^24 "m"^(-3): quad T_(1 slash 2) approx 7000 dots 16000 "K"$
    #v(8mm)
    #text(fill: muted)[logarithm: weak dependence on density]
  ]
  #at(7, 6, y: 6mm, context {
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
]
#slide(section: "thermal-ionization", title: [Saha in a tokamak divertor])[
  #at(1, 12, y: -4mm, image("/derivations/build/fig/saha_cmod.svg", width: cols(12)))
  #at(1, 12, y: 128mm, text(size: small-size, fill: muted)[
    Excited deuterium levels in the detached Alcator C-Mod divertor, measured from Balmer lines, against Saha–Boltzmann
    at the measured $k_B T_e$ and Stark $n_e$ (band: their uncertainty ranges). Data redrawn from D. Lumma, J. L. Terry,
    B. Lipschultz, Phys. Plasmas 4, 2555 (1997), doi:10.1063/1.872234; bars: digitization only.])
]
#slide(section: "thermal-ionization", title: [Equilibrium validity])[
  #at(1, 12, y: 10mm, grid(columns: (1fr,1fr), column-gutter: gutter, row-gutter: 22mm,
    [Saha \ local thermodynamic equilibrium], [dilute radiation escape \ coronal / collisional-radiative balance],
    [solar corona; tokamak edge \ many laboratory discharges], [nonthermal electrons; photons \ rate-dependent ionization],
    [high density \ pressure ionization], [ideal slots \ $n_s lambda_("th",s)^3/g_s << 1$],
  ))
]
#credits-page((), [Physics: Reif (1965); Saha (1920), DOI 10.1080/14786441008636148. \ Constants: NIST CODATA 2022. \ Original diagrams and computed plots: Christopher Albert, CC BY 4.0.])
