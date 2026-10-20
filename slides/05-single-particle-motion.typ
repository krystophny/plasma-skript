#import "theme.typ": *
#import "@preview/physica:0.9.8": dv, pdv, grad
#import "motion-drawings.typ": gyration-picture, exb-picture, gradb-picture, curvature-picture, mirror-picture, loss-cone-picture, guiding-centre-picture
#show: deck.with(chapter: 5)
#let row(label, f) = ([#text(fill: muted, label)], f)
#let formula-rows(..items, gap: 8mm) = grid(columns: (auto, 1fr), column-gutter: 8mm, row-gutter: gap,
  align: (right + horizon, left + horizon), ..items.pos().map(r => row(..r)).flatten())
#let refs(body) = text(size: 12pt, fill: muted, body)
#let chen = [F. F. Chen, _Introduction to Plasma Physics and Controlled Fusion_, 3rd ed., Springer (2016), ch. 2, #link("https://doi.org/10.1007/978-3-319-22309-4")[doi:10.1007/978-3-319-22309-4]]
#let gyro = json("/derivations/build/gyration.json")
#let sig(v, digits: 2) = {
  let p = calc.floor(calc.log(calc.abs(v), base: 10))
  let d = calc.max(0, digits - 1 - p)
  str(calc.round(v, digits: d))
}
#let length(r) = if r < 1e-3 [#sig(r * 1e6) µm] else [#sig(r * 1e3) mm]
#let freq(f) = if f >= 1e9 [#sig(f / 1e9) GHz] else [#sig(f / 1e6) MHz]
#let sci(v) = {
  let p = calc.floor(calc.log(v, base: 10))
  let a = calc.round(v / calc.pow(10.0, p), digits: 1)
  $#a times 10^#p$
}
// ---------------------------------------------------------------- board plan
#slide(section: "motion-lorentz", title: [Gyration: force balance])[
  #at(1, 6, y: 6mm, gyration-picture(electron: false))
  #at(7, 6, y: 10mm, formula-rows(
    ([Lorentz force], $bold(F) = q bold(v) times bold(B)$),
    ([$bold(v) perp bold(B)$], $abs(bold(F)) = abs(q) v_perp B$),
    ([circular orbit], $(m v_perp^2)/r_L = abs(q) v_perp B$),
  ))
  #at(7, 6, y: 86mm, result-box($omega_c = (abs(q) B)/m, quad r_L = v_perp/omega_c$, [gyrofrequency, Larmor radius]))
]
#slide(section: "motion-lorentz", title: [Equations of motion])[
  #at(1, 5, y: 6mm, gyration-picture(electron: false, force: false, axes: true, unit: 10mm))
  #at(6, 7, y: 0mm, formula-rows(gap: 6.5mm,
    ([$bold(B) = B bold(hat(z))$], $m dot(v)_x = q B v_y, quad m dot(v)_y = -q B v_x$),
    ([], $dot(v)_z = 0$),
    ([$dv(, t)$], $dot.double(v)_x = (q B)/m dot(v)_y = -omega_c^2 v_x$),
    ([solution], $v_x = v_perp cos(omega_c t + phi)$),
    ([], $v_y = minus.plus v_perp sin(omega_c t + phi)$),
    ([integrate], $x = x_0 + r_L sin(omega_c t + phi)$),
    ([], $y = y_0 plus.minus r_L cos(omega_c t + phi)$),
    ([along $bold(B)$], $z = z_0 + v_parallel t$),
  ))
  #at(5, 8, y: 134mm, text(fill: muted)[upper sign $q > 0$, lower sign $q < 0$; $phi$ gyrophase at $t = 0$])
]
// --------------------------------------------------------------- summaries
#slide(section: "motion-lorentz", title: [Gyration])[
  #at(1, 7, y: 4mm, gyration-picture(unit: 10mm))
  #at(8, 5, y: 4mm, formula-rows(gap: 7mm,
    ([frequency], $omega_c = (abs(q) B)/m$),
    ([radius], $r_L = v_perp / omega_c = (m v_perp)/(abs(q) B)$),
    ([circle], $abs(bold(r)_perp - bold(r)_0) = r_L$),
    ([along $bold(B)$], [helix, $z = z_0 + v_parallel t$]),
  ))
  #at(8, 5, y: 86mm, text(fill: muted)[$bold(B)$ out of the page: ions clockwise, electrons counterclockwise; the orbit current weakens $bold(B)$ (diamagnetic)])
  #at(1, 12, y: 122mm, text(fill: muted)[$q$ charge, $m$ mass, $B = abs(bold(B))$, $v_perp$ and $v_parallel$ speed across and along $bold(B)$, $bold(r)_perp = (x, y)$, guiding centre $bold(r)_0 = (x_0, y_0)$])
  #at(1, 12, y: 150mm, refs(chen))
]
#animation-page("gyration-top-view", "gyration_top_view", section: "motion-lorentz")
#animation-page("gyration-components", "gyration_components", section: "motion-lorentz")
#animation-page("gyration-helix", "gyration_helix", section: "motion-lorentz")
#slide(section: "motion-lorentz", title: [Typical gyrofrequencies and Larmor radii])[
  #let rows = ()
  #for (sp, name) in (("e", [electron]), ("p", [proton])) {
    for b in (1.0, 5.0) {
      let pick(t) = gyro.table.filter(r => r.species == sp and r.B == b and r.T_eV == t).first()
      rows.push(([#name], [#int(b) T], freq(pick(10.0).f), length(pick(10.0).r), length(pick(10000.0).r)))
    }
  }
  #at(2, 10, y: 8mm, align(center, data-table(
    ([], $B$, $f_c = omega_c\/2 pi$, [$r_L$, $k_B T = 10$ eV], [$r_L$, $k_B T = 10$ keV]), rows)))
  #at(1, 12, y: 104mm, align(center)[$r_L = v_"th" \/ omega_c, quad v_"th" = sqrt(2 k_B T\/m)$ #h(1.5em) #text(fill: muted)[$T$ temperature, $k_B$ Boltzmann constant]])
  #at(1, 12, y: 122mm, align(center, text(fill: muted)[$r_(L i) \/ r_(L e) = sqrt(m_i\/m_e) approx 43$ at equal $T$, #h(0.5em) $omega_(c e)\/omega_(c i) = m_i\/m_e approx 1836$]))
]
#slide(section: "motion-lorentz", title: [Thermonuclear scales])[
  #let f = gyro.fusion
  #at(1, 12, y: 0mm, align(center, text(fill: muted)[hydrogen, $n_e = 10^20 "m"^(-3)$, $T_e = T_i = 10^8 "K"$ ($k_B T approx 8.6$ keV), $B = 5$ T]))
  #at(1, 6, y: 18mm, align(center, data-table(([frequency], [$"s"^(-1)$]), (
    ($omega_(c e)$, sci(f.omega_ce)), ($omega_(p e)$, sci(f.omega_pe)), ($omega_(c i)$, sci(f.omega_ci))))))
  #at(7, 6, y: 18mm, align(center, data-table(([length], [m]), (
    ($r_(L i)$, sci(f.r_Li)), ($lambda_D$, sci(f.lambda_D)), ($r_(L e)$, sci(f.r_Le))))))
  #at(1, 12, y: 100mm, align(center)[$omega_(c e) tilde omega_(p e) >> omega_(c i), quad r_(L e) tilde lambda_D << r_(L i) << "machine size"$])
  #at(1, 12, y: 122mm, align(center, text(fill: muted)[$omega_(p e) = sqrt(n_e e^2\/(epsilon_0 m_e))$ plasma frequency, $lambda_D = sqrt(epsilon_0 k_B T_e\/(n_e e^2))$ Debye length]))
]
#slide(section: "motion-lorentz", title: [Magnetized plasma])[
  #let item(f, name) = align(center)[#text(size: result-size, f) #v(6mm) #text(fill: muted, name)]
  #at(1, 12, y: 20mm, grid(columns: (1fr, 1fr), column-gutter: gutter,
    item($r_L << L$, [orbit small against the gradient length $L$]),
    item($omega_c tau >> 1$, [many turns between collisions, $tau$ collision time]),
  ))
  #at(2, 10, y: 92mm, align(center, text(fill: muted)[fusion: $r_(L i) approx 3$ mm against minor radius $a approx 1$ m; equal $T$: $omega_(c e) tau_e > omega_(c i) tau_i$]))
]
// ------------------------------------------------------------------ drifts
#slide(section: "motion-exb", title: [$E times B$ drift])[
  #at(1, 7, y: 6mm, exb-picture())
  #at(8, 5, y: 6mm, formula-rows(gap: 7mm,
    ([frame], $bold(E)' = bold(E) + bold(v)_E times bold(B) = 0$),
  ))
  #at(8, 5, y: 62mm, result-box($bold(v)_E = (bold(E) times bold(B))/B^2$, [independent of $q$ and $m$]))
  #at(1, 12, y: 130mm, text(fill: muted)[$bold(E)$ electric field, $bold(v)_E$ drift velocity, $bold(E)'$ field in the frame moving with $bold(v)_E$])
]
#slide(section: "motion-exb", title: [General force drift])[
  #at(1, 12, y: 6mm, formula-rows(gap: 9mm,
    ([guiding centre], $bold(F) + q bold(v)_D times bold(B) = 0$),
    ([$times bold(B)$], $bold(v)_D = (bold(F) times bold(B))/(q B^2)$),
    ([$bold(F) = q bold(E)$], $bold(v)_E = (bold(E) times bold(B))/B^2$),
    ([$bold(F) = m bold(g)$], $bold(v)_g = m/q (bold(g) times bold(B))/B^2$),
  ))
  #at(1, 12, y: 96mm, text(fill: muted)[$bold(F)$ constant force across $bold(B)$, $bold(v)_D$ drift velocity, $bold(g)$ gravitational acceleration, $n$ density])
  #at(1, 12, y: 112mm)[gravity drift: opposite for ions and electrons $=>$ current $bold(j) = n (m_i + m_e) (bold(g) times bold(B))\/B^2$]
]
#slide(section: "motion-guiding-center", title: [Guiding centre])[
  #at(1, 6, y: 10mm, guiding-centre-picture())
  #at(7, 6, y: 6mm, formula-rows(gap: 8mm,
    ([split], $bold(r) = bold(R) + bold(rho), quad abs(bold(rho)) = r_L$),
    ([velocity], $bold(v) = v_parallel bold(b) + bold(v)_D + bold(v)_"gyro"$),
    ([space], $r_L \/ L << 1$),
    ([time], $omega \/ omega_c << 1$),
  ))
  #at(1, 12, y: 118mm, text(fill: muted)[$bold(R)$ guiding centre, $bold(rho)$ gyration vector, $bold(b) = bold(B)\/B$, $L$ field-variation length, $omega$ rate of change of the fields, $bold(v)_"gyro"$ fast circular part])
]
#slide(section: "motion-guiding-center", title: [Magnetic moment])[
  #at(1, 12, y: 6mm, formula-rows(gap: 9mm,
    ([orbit current], $I = abs(q) omega_c \/ (2 pi), quad S = pi r_L^2$),
    ([moment], $mu = I S = (m v_perp^2)/(2 B)$),
    ([slow change], $dv(mu, t) approx 0$),
    ([flux], $pi r_L^2 B = (2 pi m)/q^2 mu = "const."$),
  ))
  #at(3, 8, y: 104mm, result-box(align(center, $mu = (m v_perp^2)/(2 B) = "const."$), [adiabatic invariant for $r_L\/L << 1$, $omega\/omega_c << 1$]))
]
#slide(section: "motion-nonuniform-fields", title: [Grad-$B$ drift])[
  #at(1, 6, y: 10mm, gradb-picture())
  #at(7, 6, y: 6mm, formula-rows(gap: 8mm,
    ([force], $bold(F)_mu = -mu grad B$),
    ([drift], $bold(v)_(grad B) = (mu bold(B) times grad B)/(q B^2)$),
  ))
  #at(7, 6, y: 84mm, text(fill: muted)[smaller $r_L$ where $B$ is stronger; ions and electrons drift in opposite directions])
  #at(1, 12, y: 128mm, text(fill: muted)[$grad B$ gradient of the field strength, $mu = m v_perp^2\/(2 B)$])
]
#slide(section: "motion-nonuniform-fields", title: [Curvature drift])[
  #at(1, 6, y: 6mm, curvature-picture())
  #at(7, 6, y: 6mm, formula-rows(gap: 8mm,
    ([centrifugal], $bold(F)_"curv" = (m v_parallel^2)/R_c^2 bold(R)_c$),
    ([drift], $bold(v)_"curv" = (m v_parallel^2)/(q B) bold(b) times bold(kappa)$),
  ))
  #at(1, 12, y: 100mm, align(center)[#text(fill: muted)[vacuum field:] #h(0.6em) $bold(v)_"curv" + bold(v)_(grad B) = m/(q B) (v_parallel^2 + v_perp^2/2) bold(b) times bold(kappa)$])
  #at(1, 12, y: 128mm, text(fill: muted)[$bold(R)_c$ from the centre of curvature to the field line, $bold(kappa) = (bold(b) dot grad) bold(b) = -bold(R)_c\/R_c^2$ curvature])
]
#slide(section: "motion-nonuniform-fields", title: [Magnetic mirror])[
  #at(1, 7, y: 10mm, mirror-picture())
  #at(8, 5, y: 6mm, formula-rows(gap: 8mm,
    ([along $bold(B)$], $m dv(v_parallel, t) = -mu pdv(B, s)$),
    ([energy], $(m v_parallel^2)/2 + mu B = "const."$),
    ([reflection], [$v_parallel = 0$ at $mu B = (m v^2)/2$]),
  ))
  #at(1, 12, y: 128mm, text(fill: muted)[$s$ arc length along $bold(B)$, $B_0$ midplane field, $B_max$ field at the mirror throat, $v$ speed])
]
#slide(section: "motion-nonuniform-fields", title: [Mirror ratio and loss cone])[
  #at(1, 6, y: 10mm, loss-cone-picture())
  #at(7, 6, y: 6mm, formula-rows(gap: 8mm,
    ([pitch angle], $sin alpha = v_perp \/ v$),
    ([$mu$ const.], $(sin^2 alpha)/B = "const."$),
    ([mirror ratio], $R_m = B_max \/ B_0$),
  ))
  #at(7, 6, y: 78mm, result-box($sin^2 alpha_c = 1/R_m$, [loss cone: $alpha_0 < alpha_c$ escapes]))
  #at(1, 12, y: 134mm, text(fill: muted)[$alpha$ angle between $bold(v)$ and $bold(B)$, $alpha_0$ at the midplane; independent of $q$ and $m$])
]
#slide(section: "motion-polarization", title: [Polarization drift])[
  #at(1, 12, y: 6mm, formula-rows(gap: 9mm,
    ([slow $bold(E)_perp (t)$], $bold(v)_perp = bold(v)_E + bold(v)_"pol" + bold(v)_"gyro"$),
    ([drift], $bold(v)_"pol" = m/(q B^2) pdv(bold(E)_perp, t)$),
    ([current], $bold(j)_"pol" = sum_s n_s q_s bold(v)_("pol",s) = rho_m/B^2 pdv(bold(E)_perp, t)$),
    ([validity], $omega << omega_c$),
  ))
  #at(1, 12, y: 108mm, text(fill: muted)[$bold(E)_perp$ field across $bold(B)$, $rho_m = sum_s n_s m_s$ mass density, $n_s$ density of species $s$; carried mainly by ions])
]
#slide(title: [Drifts])[
  #at(1, 12, y: 4mm, align(center, data-table(
    ([drift], [velocity], [ions vs electrons], [mass]),
    (
      ([$E times B$], $(bold(E) times bold(B))\/B^2$, [same], [none]),
      ([gravity], $m(bold(g) times bold(B))\/(q B^2)$, [opposite], [$prop m$]),
      ([grad-$B$], $mu (bold(B) times grad B)\/(q B^2)$, [opposite], [$prop m v_perp^2$]),
      ([curvature], $m v_parallel^2 (bold(b) times bold(kappa))\/(q B)$, [opposite], [$prop m v_parallel^2$]),
      ([polarization], $m dot(bold(E))_perp \/ (q B^2)$, [opposite], [$prop m$]),
    ),
    align: left)))
  #at(1, 12, y: 128mm, align(center, text(fill: muted)[$bold(v)_D = bold(F) times bold(B)\/(q B^2)$ for a force $bold(F)$; $mu$ magnetic moment, $bold(b) = bold(B)\/B$, $bold(kappa)$ curvature; opposite drifts carry currents]))
]
