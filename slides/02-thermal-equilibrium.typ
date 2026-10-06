#import "theme.typ": *
#import "@preview/physica:0.9.8": pdv
#import "/src/thermal-figures.typ": microstates, thermal-table
#show: deck.with(chapter: 2)
#slide(section: "thermal-temperature", title: [Temperature meaning])[
  #at(1, 12, y: 12mm, diagram(spacing: 24mm,
    node((0,0), [energy $E$]), edge("-|>"), node((1,0), [states $W(E)$]),
    edge("-|>"), node((2,0), [entropy $S(E)$]),
  ))
  #at(1, 12, y: 84mm, result-box($1/T = pdv(S,E)$, [fixed volume, particle number, total momentum]))
]
#slide(section: "thermal-microstates", title: [Microstate counting])[
  #at(2, 10, y: 6mm, align(center, microstates()))
  #at(1, 12, y: 112mm, result-box($W_3=W_2 W_1=4 times 2=8$, [one new binary choice doubles the states]))
]
#slide(section: "thermal-microstates", title: [Additive entropy])[
  #at(1, 6, y: 15mm)[
    $W_A=4, quad W_B=2$
    #v(14mm) $W_(A+B)=W_A W_B=8$
    #v(14mm) $ln(W_A W_B)=ln W_A+ln W_B$
  ]
  #at(7, 6, y: 20mm)[
    #result-box($S=k_B ln W$, [entropy])
    #v(16mm) $S_(A+B)=S_A+S_B$
    #v(12mm) #text(fill: muted)[$W$ multiplicity [1] \ $S$: J/K; $k_B$: J/K]
  ]
]
#slide(section: "thermal-temperature", title: [Two exchanging boxes])[
  #at(1, 12, y: 10mm, diagram(spacing: 50mm,
    node((0,0), [A \ $E_A,T_A,S_A$]), edge("<->", [$dif E_A=-dif E_B$]),
    node((1,0), [B \ $E_B,T_B,S_B$]),
  ))
  #at(1, 12, y: 78mm, result-box($dif S_"tot"=(1/T_A-1/T_B) dif E_A$, [$T_A=T_B$ at the entropy maximum]))
]
#slide(section: "thermal-temperature", title: [Entropy slope])[
  #at(1, 12, y: 12mm)[
    #result-box($1/T = pdv(S,E), quad dif S=(dif E)/T$, [fixed $V,N,bold(P)$])
    #v(18mm) $dif E=T dif S-p dif V+mu dif N+bold(u) dot dif bold(P)$
    #v(16mm) $T>0$ \ unbounded translational energy
    #v(10mm) #text(fill: muted)[$p$ pressure; $mu$ chemical potential; $bold(u)$ bulk velocity]
  ]
]
#slide(section: "thermal-boltzmann", title: [Reservoir weight])[
  #at(1, 6, y: 10mm, diagram(spacing: 25mm,
    node((0,0), [small system A \ $E_a$]), edge("<->"),
    node((0,1), [large reservoir \ $E_"tot"-E_a$]),
  ))
  #at(7, 6, y: 10mm)[
    $P_a prop W_"rest"(E_"tot"-E_a)$
    #v(12mm) $W_"rest"=exp(S_"rest"/k_B)$
    #v(12mm) $S_"rest"(E_"tot"-E_a)$ \ $approx S_"rest"(E_"tot")-E_a/T$
    #v(12mm) #result-box($P_a prop exp(-E_a/(k_B T))$, [Boltzmann factor per microstate])
  ]
]
#slide(section: "thermal-boltzmann", title: [Drifting Maxwellian])[
  #at(1, 6, y: 10mm)[
    $bold(u)=bold(P)/(N m)$
    #v(12mm) $E_"kin"=bold(P)^2/(2 N m)+E_"random"$
    #v(12mm) #result-box($F_s prop exp(-((bold(v)-bold(u)_s)^2)/v_("th",s)^2)$, [$v_("th",s)=sqrt((2 k_B T_s)/m_s)$])
    #v(8mm) #text(fill: muted)[thermal-speed convention: §1.2]
  ]
  #at(7, 6, plot("maxwellian_drift", columns: 6))
]
#slide(section: "thermal-saha", title: [Thermal particle slots])[
  #at(1, 6, y: 10mm, diagram(spacing: 24mm,
    node((0,0), [volume $V$]), edge("-|>"), node((0,1), [translational states $V/lambda_("th",s)^3$]),
    edge("-|>"), node((0,2), [internal choices $g_s$]),
  ))
  #at(7, 6, y: 12mm)[
    #result-box($M_s=(g_s V)/lambda_("th",s)^3$, [thermally available slots [1]])
    #v(14mm) $lambda_("th",s)=h/sqrt(2 pi m_s k_B T)$
    #v(14mm) #text(fill: muted)[$g_s$ same-energy internal states [1] \ $h$ Planck constant; $lambda_("th",s)$: m]
  ]
]
#slide(section: "thermal-saha", title: [Adding and removing])[
  #at(1, 12, y: 8mm, result-box($W_s(N_s) approx M_s^(N_s)/(N_s!)$, [dilute indistinguishable particles]))
  #at(1, 6, y: 65mm)[
    adding one particle
    #v(12mm) $W_s(N_s+1)/W_s(N_s)=M_s/(N_s+1)$
    #v(10mm) $approx M_s/N_s$
  ]
  #at(7, 6, y: 65mm)[
    removing one particle
    #v(12mm) $W_s(N_s-1)/W_s(N_s)=N_s/M_s$
    #v(10mm) #text(fill: muted)[$N_s >> 1$; $N_s << M_s$]
  ]
]
#slide(section: "thermal-saha", title: [One ionization])[
  #at(1, 12, y: 8mm, diagram(spacing: 35mm,
    node((0,0), [neutral A]), edge("-|>"), node((1,0), [ion A⁺ + electron e⁻]),
  ))
  #at(1, 12, y: 60mm, grid(columns: (1fr,1fr,1fr), column-gutter: gutter,
    [remove neutral \ $(n_n lambda_("th",n)^3)/g_n$],
    [add ion \ $g_i/(n_i lambda_("th",i)^3)$],
    [add electron \ $2/(n_e lambda_("th",e)^3)$],
  ))
  #at(1, 12, y: 117mm, result-box($R=(W_"after")/W_"before" = "particle factors" times exp(-chi/(k_B T))$, [reservoir pays $chi$]))
]
#slide(section: "thermal-saha", title: [Heavy particle cancellation])[
  #at(1, 12, y: 10mm)[
    $m_n approx m_i quad => quad lambda_("th",n) approx lambda_("th",i)$
    #v(18mm) $((n_n lambda_("th",n)^3)/g_n) (g_i/(n_i lambda_("th",i)^3)) approx (n_n g_i)/(n_i g_n)$
    #v(18mm) #result-box($R approx (n_n)/(n_i n_e) (2 g_i)/(g_n lambda_("th",e)^3) exp(-chi/(k_B T))$, [$R=1$: composition equilibrium])
  ]
]
#slide(section: "thermal-saha", title: [Saha composition balance])[
  #at(1, 12, y: 8mm, result-box($(n_i n_e)/n_n = 2/lambda_("th",e)^3 g_i/g_n exp(-chi/(k_B T))$, [Saha equation]))
  #at(1, 12, y: 67mm, grid(columns: (1fr,1fr,1fr), column-gutter: gutter,
    [$2/lambda_("th",e)^3$ \ free-electron states],
    [$g_i/g_n$ \ internal states], [$exp(-chi/(k_B T))$ \ energy penalty],
  ))
  #at(1, 12, y: 124mm)[$g_i=g_n=1$ \ internal quantum states: order-one factors]
]
#plot-page("saha_fraction", columns: 8, section: "thermal-ionization", title: [Ionization fraction],
  below: [$x=n_i/(n_i+n_n), quad n_e=n_i, quad x^2/(1-x)=A(T,n)$])
#plot-page("saha_factors", columns: 8, section: "thermal-ionization", title: [Competing statistical factors],
  below: [$A=1/2$ at $x=1/2$; $A=1$ at $x approx 0.618$])
#slide(section: "thermal-ionization", title: [Thermal ionization threshold])[
  #at(1, 12, y: 3mm, result-box($k_B T_(1/2)=chi/ln(4/(n lambda_("th",e)^3))$, [iterate $lambda_("th",e)(T)$; $chi=13.6$ eV]))
  #at(1, 12, y: 57mm, thermal-table())
  #at(1, 12, y: 138mm)[$T tilde.op 10^4$ K: intermediate-density thermal estimate]
]
#slide(section: "thermal-ionization", title: [Equilibrium validity])[
  #at(1, 12, y: 10mm, grid(columns: (1fr,1fr), column-gutter: gutter, row-gutter: 22mm,
    [Saha \ local thermodynamic equilibrium], [dilute radiation escape \ coronal / collisional-radiative balance],
    [solar corona; tokamak edge \ many laboratory discharges], [nonthermal electrons; photons \ rate-dependent ionization],
    [high density \ pressure ionization], [ideal slots \ $n_s lambda_("th",s)^3/g_s << 1$],
  ))
]
#credits-page((), [Physics: Reif (1965); Saha (1920), DOI 10.1080/14786441008636148. \ Constants: NIST CODATA 2022. \ Original diagrams and computed plots: Christopher Albert, CC BY 4.0.])
