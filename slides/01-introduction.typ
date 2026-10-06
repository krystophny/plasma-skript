#import "theme.typ": *
#import "@preview/physica:0.9.8": dv
#show: deck.with(chapter: 1)
#slide(section: "intro-plasma-state", title: [Plasma state])[
  #at(1, 6, y: 8mm, diagram(spacing: 22mm,
    node((0,0), [ions $+Z e$]), edge("<->"), node((1,0), [electrons $-e$]),
    edge((0,0),(0.5,1),"-|>"), edge((1,0),(0.5,1),"-|>"), node((0.5,1), [collective fields]),
  ))
  #at(7, 6, y: 18mm)[
    #result-box($rho_q = sum_s q_s n_s$, [charge density])
    #v(12mm) mobile charges \ collective response \ observation scale
    #v(8mm) #text(fill: muted)[$q_s$ charge; $n_s$ density]
  ]
]
#photo-page("sun_flare_sdo.jpg", [NASA/SDO, public domain], "photo-sun")
#photo-page("aurora_iss.jpg", [NASA, public domain], "photo-aurora")
#photo-page("carina_eso.jpg", [ESO, CC BY 4.0], "photo-carina")
#photo-page("hall_thruster_jpl.jpg", [NASA/JPL-Caltech, public domain], "photo-thruster")
#animation-page("collective-response", "collective_response", loop: false)
#slide(section: "intro-plasma-state", title: [Quasineutrality])[
  #at(1, 6, y: 8mm)[
    $rho_q = e (sum_i Z_i n_i - n_e)$
    #v(12mm) #result-box($n_e approx sum_i Z_i n_i$, [$L >> lambda_D$])
    #v(10mm) #text(fill: muted)[$L$ observation length \ $lambda_D$ screening length (chapter 3)]
  ]
  #at(7, 6, plot("enclosed_charge", columns: 6))
]
#plot-page("nt_plane", columns: 10, section: "intro-plasma-state", title: [Example plasmas])
#plot-pair("maxwellian_heating", "maxwellian_drift", section: "intro-speed-energy-temperature", title: [Thermal motion])
#slide(section: "intro-speed-energy-temperature", title: [Thermal speed])[
  #at(1, 6, y: 8mm)[
    #result-box($v_("th",s) = sqrt((2 k_B T_s)/m_s)$, [thermal-speed convention])
    #v(10mm) $chevron.l (v_x-u_s)^2 chevron.r = (k_B T_s)/m_s$
    #v(8mm) $v_"peak" = v_("th",s), quad v_"rms" = sqrt(3/2) v_("th",s)$
    #v(10mm) #text(fill: muted)[$m_s$ mass; $u_s$ mean flow \ $T_s$ temperature]
  ]
  #at(7, 6, plot("maxwell_speed", columns: 6))
]
#plot-page("thermal_speed", columns: 8, section: "intro-speed-energy-temperature", title: [Temperature scales],
  below: [$k_B T = 1 "eV" quad <-> quad T approx 11605 "K"$])
#slide(section: "intro-scales", title: [Characteristic scales])[
  #at(1, 12, grid(columns: (1fr, 1fr), column-gutter: gutter, row-gutter: 8mm,
    [$lambda_D = sqrt((epsilon_0 k_B T_e)/(n_e e^2))$], [$omega_(p e) = sqrt((n_e e^2)/(epsilon_0 m_e))$],
    [$rho_e = v_("th",e)/omega_(c e)$], [$lambda_"mfp" = chevron.l v chevron.r / nu_(e i)$],
  ))
  #at(1, 12, y: 46mm, plot("scale_ordering", columns: 12))
]
#slide(section: "intro-model-hierarchy", title: [Microscopic dynamics])[
  #at(1, 12, y: 8mm)[
    #result-box($dv(bold(r)_j,t)=bold(v)_j, quad m_j dv(bold(v)_j,t)=q_j (bold(E)+bold(v)_j times bold(B))$, [$N$ coupled trajectories])
    #v(12mm) #grid(columns: (1fr, 1fr), column-gutter: gutter,
      [$N tilde.op 10^20$ \ $tilde.op N^2$ pair interactions], [self-consistent $bold(E), bold(B)$ \ Maxwell field equations])
    #v(18mm) #diagram(spacing: 38mm,
      node((0,0), [particle trajectories]), edge("-|>"), node((1,0), [$rho_q, bold(j)$]),
      edge("-|>"), node((2,0), [$bold(E),bold(B)$]), edge((2,0),(0,0),"-|>", bend: -45deg),
    )
  ]
]
#slide(section: "intro-model-hierarchy", title: [Phase space])[
  #at(1, 6, y: 10mm, diagram(spacing: 24mm,
    node((0,0), [$bold(x)$ \ position (3)]), node((1,0), [$bold(v)$ \ velocity (3)]),
    edge((0,0),(0.5,1),"-|>"), edge((1,0),(0.5,1),"-|>"), node((0.5,1), [$bold(z)=(bold(x),bold(v))$]),
  ))
  #at(7, 6, y: 18mm)[
    #result-box($f_s(bold(x),bold(v),t)$, [one-particle distribution])
    #v(12mm) $f_s dif^3 x dif^3 v$ \ particle count [1]
    #v(8mm) #text(fill: muted)[$f_s$: $"s"^3 "m"^(-6)$]
  ]
]
#slide(section: "intro-model-hierarchy", title: [Coarse graining])[
  #at(1, 12, y: 10mm, diagram(spacing: 24mm,
    node((0,0), [particles]), edge("-|>"), node((1,0), [ensemble average]),
    edge("-|>"), node((2,0), [finite cells]),
  ))
  #at(1, 12, y: 72mm, result-box($n_s(bold(x),t)=integral f_s dif^3 v$, [velocity integration → number density]))
]
#animation-page("particles-to-moments", "particles_to_moments", loop: false)
#slide(section: "intro-model-hierarchy", title: [Model ladder])[
  #at(1, 12, y: 8mm, diagram(spacing: 17mm,
    node((0,0), [particles]), edge("-|>"), node((1,0), [$f_s$]), edge("-|>"),
    node((2,0), [moments]), edge("-|>"), node((3,0), [fluids]),
  ))
  #at(1, 6, y: 70mm)[$n_s = integral f_s dif^3 v$ \ $n_s bold(u)_s = integral bold(v) f_s dif^3 v$]
  #at(7, 6, y: 70mm, result-box([two fluids → MHD], [scale ordering + closure]))
]
#slide(section: "intro-plasma-state", title: [Plasma phenomena])[
  #at(1, 12, y: 12mm, grid(columns: (1fr, 1fr), column-gutter: gutter, row-gutter: 18mm,
    [screening \ $lambda_D$], [oscillations \ $omega_(p e)$],
    [charge and heat transport \ $bold(j), bold(q)$], [radiation \ free–free; bound–free; lines],
    [electromagnetic response \ $q (bold(E)+bold(v) times bold(B))$], [collective interaction \ $N_D >> 1$],
  ))
]
#credits-page((
  ("photo-sun", [NASA/SDO, public domain], "svs.gsfc.nasa.gov/14589"),
  ("photo-aurora", [NASA, ISS Expedition 23, public domain], "commons.wikimedia.org/wiki/File:Aurora_Australis_From_ISS.JPG"),
  ("photo-carina", [ESO, CC BY 4.0], "eso.org/public/images/eso0905a"),
  ("photo-thruster", [NASA/JPL-Caltech, public domain], "commons.wikimedia.org/wiki/File:Xenon_hall_thruster.jpg"),
), [Original plots, diagrams, animations: Christopher Albert, CC BY 4.0.])
