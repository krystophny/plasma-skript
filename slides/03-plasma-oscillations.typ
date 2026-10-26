#import "theme.typ": *
#import "@preview/physica:0.9.8": dv
#import "oscillation-drawings.typ": slab-picture
#show: deck.with(chapter: 3)
#animation-page("plasma-oscillation", "plasma_oscillation", section: "intro-plasma-oscillations")
#slide(section: "intro-plasma-oscillations", title: [Electron plasma oscillations])[
  #at(1, 7, y: 4mm, scale(68%, reflow: true, slab-picture()))
  #at(8, 5, y: 4mm)[
    $Q = e n_0 A xi$ #h(0.6em) #text(fill: muted)[$A$ slab area]
    #v(7mm) #text(fill: muted)[Gauss] #h(0.6em) $epsilon_0 E A = Q$
    #v(7mm) #text(fill: muted)[Newton] #h(0.6em) $m_e dv(xi, t, 2) = -e E$
    #v(7mm) $dv(xi, t, 2) + omega_(p e)^2 xi = 0$
  ]
  #at(4, 6, y: 82mm, result-box(align(center, $omega_(p e) = sqrt((n_0 e^2)/(epsilon_0 m_e))$), [electron plasma frequency]))
]
#animation-page("sheet-oscillation", "sheet_oscillation", section: "intro-plasma-oscillations")
#animation-page("sheet-wave-breaking", "sheet_wave_breaking", section: "intro-plasma-oscillations")
#slide(section: "intro-plasma-oscillations", title: [Plasma frequency])[
  #let examples = json("/derivations/build/plasma-frequency.json")
  #let sci(v) = {
    let power = calc.floor(calc.log(v, base: 10))
    let a = calc.round(v / calc.pow(10.0, power), digits: 1)
    if a == 1 { $10^#power$ } else { $#a times 10^#power$ }
  }
  #at(1, 7, y: 4mm, plot("plasma_frequency", columns: 7))
  #at(8, 5, y: 10mm, {
    for r in examples [
      #text(size: title-size)[#r.name] \
      #v(4mm) $n_e =$ #sci(r.n) $"m"^(-3)$ \
      #v(2mm) $omega_(p e) =$ #sci(r.omega) $"s"^(-1)$ \
      #v(2mm) $omega_(p e)^(-1) =$ #sci(r.inverse) $"s"$
      #v(14mm)
    ]
  })
]
#animation-page("em-wave-plasma-reflection", "em_wave_plasma_reflection", section: "intro-plasma-oscillations", loop: false)
#slide(section: "intro-plasma-oscillations", title: [Electromagnetic waves])[
  #at(1, 6, y: 10mm)[
    #result-box($omega^2 = omega_(p e)^2 + c^2 k^2$, [dispersion relation])
    #v(14mm) $omega < omega_(p e)$: reflected
    #v(8mm) $omega > omega_(p e)$: transmitted
  ]
  #at(7, 6, y: 4mm, plot("cold_em_dispersion", columns: 6))
]
#slide(section: "intro-plasma-oscillations", title: [Frequency and length scales])[
  #let item(f, name) = [#text(size: result-size, f) #v(4mm) #text(fill: muted, name)]
  #at(1, 12, y: 10mm, grid(columns: (1fr, 1fr), column-gutter: gutter, row-gutter: 22mm,
    item($omega_(p s) = sqrt((n_s q_s^2)/(epsilon_0 m_s))$, [any species $s$]),
    item($omega_(p i) = sqrt((Z m_e)/m_i) thin omega_(p e)$, [ions, $n_i = n_e\/Z$: much slower]),
    item($d_e = c/omega_(p e)$, [inertial length: reach of a reflected wave]),
    item($omega_p^2 = omega_(p e)^2 + omega_(p i)^2 = (n_e e^2)/(epsilon_0 m_"eff")$, [ions move too: $1/m_"eff" = 1/m_e + Z/m_i$]),
  ))
]
#plot-page("two_species_oscillation", columns: 10, section: "intro-plasma-oscillations", title: [Ions move too],
  below: [$xi_i = -(m_e\/m_i) thin xi_e, quad omega_p^2 = omega_(p e)^2 + omega_(p i)^2, quad omega_(p i)^2\/omega_(p e)^2 = m_e\/m_i$ \
    #v(3mm) #text(fill: muted)[$xi_alpha$ displacement of species $alpha$, $v_0$ initial electron speed amplitude, $Z = 1$]])
