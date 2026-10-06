#import "theme.typ": *
#import "@preview/physica:0.9.8": dv
#import "/src/opening-diagrams.typ": electron-slab
#show: deck.with(chapter: 4)
#import "oscillation-drawings.typ": slab-picture
#animation-page("plasma-oscillation", "plasma_oscillation", section: "intro-plasma-oscillations")
#slide(section: "intro-plasma-oscillations", title: [Cold electron slab])[
  #at(2, 10, y: 6mm, slab-picture())
  #at(1, 12, y: 116mm, align(center, text(fill: muted)[
    fixed ions $n_i = n_0$#h(1.5em)cold electrons $k_B T_e -> 0$#h(1.5em)small shift $abs(xi) << L$#h(1.5em)$sigma$ surface charge]))
]
#slide(section: "intro-plasma-oscillations", title: [Oscillator equation])[
  #at(1, 12, y: 8mm, align(center)[
    $sigma = e n_0 xi quad --> quad E = sigma/epsilon_0 quad --> quad m_e dv(xi, t, 2) = -e E = -(n_0 e^2)/epsilon_0 xi$
  ])
  #at(1, 12, y: 48mm, align(center, text(size: result-size,
    $dv(xi, t, 2) + omega_(p e)^2 xi = 0, quad xi = xi_0 cos(omega_(p e) t + delta)$)))
  #at(3, 8, y: 90mm, result-box(align(center, $omega_(p e) = sqrt((n_0 e^2)/(epsilon_0 m_e))$), [electron plasma frequency]))
]
#plot-page("plasma_frequency", columns: 8, section: "intro-plasma-oscillations", title: [Plasma frequency scale],
  below: [$f_(p e) = omega_(p e)/(2 pi), quad omega_(p e) prop sqrt(n_e)$])
#slide(section: "intro-plasma-oscillations", title: [Metal and fusion])[
  #set text(size: 21pt)
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
  #at(1, 12, y: 14mm, align(center)[
    $v_("th",e) = sqrt((2 k_B T_e)/m_e) quad quad omega_(p e) = sqrt((n_e e^2)/(epsilon_0 m_e))$
  ])
  #at(1, 12, y: 56mm, align(center, text(size: result-size,
    $lambda_D = underbrace(v_("th",e), "thermal speed") dot underbrace(1/(sqrt(2) omega_(p e)), "response time")$)))
  #at(1, 12, y: 124mm, align(center, text(fill: muted)[screening length = distance a thermal electron moves in one plasma response time (chapter 3)]))
]
#slide(section: "intro-plasma-oscillations", title: [Model validity])[
  #let item(f, name) = align(center)[#text(size: result-size, f) #v(5mm) #text(fill: muted, name)]
  #at(1, 12, y: 14mm, grid(columns: (1fr, 1fr, 1fr), row-gutter: 26mm,
    item($k_B T_e -> 0$, [else pressure: dispersion]), item($nu << omega_(p e)$, [else collisional damping]),
    item($m_i >> m_e$, [ions too slow to follow]),
    item($bold(B) = 0$, [else gyromotion couples]), item($abs(xi) << L$, [linear restoring force]),
    item($omega > omega_(p e)$, [EM waves propagate]),
  ))
]
#credits-page((), [Original figures and animation: Christopher Albert, CC BY 4.0. \ Physics: Chen (2016); Bittencourt (2004). \ Constants: NIST CODATA (2018), as in the Skript.])
