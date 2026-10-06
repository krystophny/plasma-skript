#import "theme.typ": *
#import "@preview/physica:0.9.8": dv
#import "/src/opening-diagrams.typ": electron-slab
#show: deck.with(chapter: 4)
#animation-page("plasma-oscillation", "plasma_oscillation", section: "intro-plasma-oscillations")
#slide(section: "intro-plasma-oscillations", title: [Cold electron slab])[
  #at(1, 8, y: 15mm, electron-slab())
  #at(9, 4, y: 15mm)[
    $n_i=n_0$ \ $k_B T_e -> 0$ \ $abs(xi) << L$
    #v(14mm) #text(fill: muted)[$xi$ displacement \ $L$ slab width]
  ]
]
#slide(section: "intro-plasma-oscillations", title: [Restoring electric field])[
  #at(1, 8, y: 4mm, electron-slab())
  #at(9, 4, y: 8mm)[$sigma = e n_0 xi$ \ $E = sigma/epsilon_0$ \ $F_e = -e E$]
  #at(1, 12, y: 110mm, result-box($m_e dv(xi,t,2) = -(n_0 e^2)/epsilon_0 xi$, [restoring sign]))
]
#slide(section: "intro-plasma-oscillations", title: [Oscillator equation])[
  #at(1, 6, y: 5mm)[
    $sigma = e n_0 xi$
    #v(10mm) $E = (e n_0 xi)/epsilon_0$
    #v(10mm) $m_e dv(xi,t,2)=-e E$
    #v(10mm) $dv(xi,t,2)+omega_(p e)^2 xi=0$
    #v(10mm) $xi = xi_0 cos(omega_(p e)t+delta)$
  ]
  #at(7, 6)[
    #result-box($omega_(p e)=sqrt((n_0 e^2)/(epsilon_0 m_e))$, [electron plasma frequency])
    #v(8mm) #plot("plasma_frequency", columns: 6)
  ]
]
#plot-page("plasma_frequency", columns: 8, section: "intro-plasma-oscillations", title: [Plasma frequency scale],
  below: [$f_(p e) = omega_(p e)/(2 pi), quad omega_(p e) prop sqrt(n_e)$])
#slide(section: "intro-plasma-oscillations", title: [Metal and fusion])[
  #let examples = json("/derivations/build/plasma-frequency.json")
  #let sci(v) = {
    let power = calc.floor(calc.log(v, base: 10))
    let a = calc.round(v / calc.pow(10.0, power), digits: 2)
    $#a times 10^#power$
  }
  #at(1, 12, y: 8mm, grid(columns: (1fr,1fr), column-gutter: gutter, ..examples.map(r => [
    #text(size: title-size)[#r.name]
    #v(10mm) $n_e=$ #sci(r.n) $"m"^(-3)$
    #v(10mm) $omega_(p e)=$ #sci(r.omega) $"s"^(-1)$
    #v(10mm) $1/omega_(p e)=$ #sci(r.inverse) s
    #v(10mm) $2 pi/omega_(p e)=$ #sci(r.period) s
  ])))
  #at(1, 12, y: 132mm, text(fill: muted)[metal: free-electron estimate; fusion: classical cold response])
]
#slide(section: "intro-plasma-oscillations", title: [Electromagnetic wave cutoff])[
  #at(1, 6, y: 10mm)[
    #result-box($omega^2=omega_(p e)^2+c^2 k^2$, [cold, unmagnetized transverse wave])
    #v(12mm) $omega>omega_(p e): quad k^2>0$ \ propagation
    #v(12mm) $omega<omega_(p e): quad k^2<0$ \ evanescence
    #v(8mm) #text(fill: muted)[$c$ light speed; $k$ wavenumber]
  ]
  #at(7, 6, plot("cold_em_dispersion", columns: 6))
]
#slide(section: "intro-plasma-oscillations", title: [Thermal screening link])[
  #at(1, 6, y: 10mm)[
    $v_("th",e)=sqrt((2 k_B T_e)/m_e)$
    #v(14mm) $omega_(p e)=sqrt((n_e e^2)/(epsilon_0 m_e))$
    #v(14mm) #result-box($lambda_D = v_("th",e)/(sqrt(2) omega_(p e))$, [thermal distance in a response time])
    #v(8mm) #text(fill: muted)[$lambda_D$ screening length (chapter 3)]
  ]
  #at(7, 6, plot("thermal_speed", columns: 6))
]
#slide(section: "intro-plasma-oscillations", title: [Model validity])[
  #at(1, 12, y: 15mm, grid(columns: (1fr,1fr), column-gutter: gutter, row-gutter: 22mm,
    [cold electrons \ pressure → dispersion], [fixed ions \ slower ion response],
    [$nu << omega_(p e)$ \ collisions → damping], [$B=0$ \ magnetic field → gyromotion],
    [$abs(xi) << L$ \ linear restoring response], [transverse waves \ cutoff at $omega_(p e)$],
  ))
]
#credits-page((), [Original figures and animation: Christopher Albert, CC BY 4.0. \ Physics: Chen (2016); Bittencourt (2004). \ Constants: NIST CODATA (2018), as in the Skript.])
