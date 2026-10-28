#import "theme.typ": *
#import "@preview/physica:0.9.8": dv, pdv, grad
#import "motion-drawings.typ": gyration-picture, exb-picture, curvature-picture, loss-cone-picture, guiding-centre-picture, mirror-force-picture, faraday-picture, field-line-picture, gradb-picture, mirror-picture
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
#let note(body) = text(fill: muted, body)
// Shared row layout of the guiding-centre and mirror pages: fixed label
// column, gap and formula size, so the labels align from page to page.
#let rows-y = 8mm
#let result-y = 92mm
#let lrows(..items, size: 20pt, label-width: 50mm, gap: 14mm) = grid(columns: (label-width, auto),
  column-gutter: 8mm, row-gutter: gap, align: (right + horizon, left + horizon),
  ..items.pos().map(r => ([#text(fill: muted, r.at(0))], text(size: size, r.at(1)))).flatten())
#let symbols(body) = at(1, 12, y: 146mm, note(body))
// ------------------------------------------------------------ 1 gyration
#slide(section: "motion-lorentz", title: [Gyration: force balance])[
  #at(1, 6, y: 6mm, gyration-picture(electron: false))
  #at(7, 6, y: 6mm, formula-rows(
    ([Lorentz force], $bold(F) = q_alpha bold(v) times bold(B)$),
    ([$bold(v) perp bold(B)$], $abs(bold(F)) = abs(q_alpha) v_perp B$),
    ([centrifugal = Lorentz], $(m_alpha v_perp^2)/rho_L = abs(q_alpha) v_perp B$),
  ))
  #at(7, 6, y: 76mm, result-box($omega_c = (q_alpha B)/m_alpha, quad rho_L = v_perp/abs(omega_c)$, [gyrofrequency, Larmor radius]))
  #at(1, 12, y: 134mm, note[$q_alpha$, $m_alpha$ charge and mass of species $alpha$; $omega_c = q_alpha B\/m_alpha$ signed; $B = abs(bold(B))$; $v_perp$ speed across $bold(B)$])
]
#slide(section: "motion-lorentz", title: [Equations of motion])[
  #at(1, 5, y: 6mm, gyration-picture(electron: false, force: false, axes: true, unit: 10mm))
  #at(6, 7, y: 4mm, formula-rows(gap: 7mm,
    ([$bold(B) = B bold(e)_z$], $dif v_x \/ dif t = omega_c v_y, quad dif v_y \/ dif t = -omega_c v_x$),
    ([], $dif v_z \/ dif t = 0$),
    ([$dif \/ dif t$], $dif^2 v_x \/ dif t^2 = omega_c dif v_y \/ dif t = -omega_c^2 v_x$),
    ([solution], $v_x = v_perp cos(omega_c t + phi.alt)$),
    ([], $v_y = -v_perp sin(omega_c t + phi.alt)$),
    ([integrate], $x = x_0 + (v_perp \/ omega_c) sin(omega_c t + phi.alt)$),
    ([], $y = y_0 + (v_perp \/ omega_c) cos(omega_c t + phi.alt)$),
    ([along $bold(B)$], $z = z_0 + v_parallel t$),
  ))
  #at(1, 12, y: 124mm, note[$phi.alt$ gyrophase, $(x_0, y_0)$ guiding centre, $rho_L = v_perp\/abs(omega_c)$, $v_parallel$ speed along $bold(B)$])
  #at(1, 12, y: 134mm, note[$bold(B)$ out of the page: ions ($omega_c > 0$) clockwise, electrons ($omega_c < 0$) counterclockwise])
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
      rows.push(([#name], [#int(b) T], freq(pick(10.0).f), length(pick(10.0).rho_L), length(pick(10000.0).rho_L)))
    }
  }
  #at(2, 10, y: 8mm, align(center, data-table(
    ($alpha$, $B$, $abs(omega_c)\/2 pi$, [$rho_L$, $k_B T = 10$ eV], [$rho_L$, $k_B T = 10$ keV]), rows)))
  #at(1, 12, y: 104mm, align(center)[$rho_L = v_"th" \/ abs(omega_c), quad v_"th" = sqrt(2 k_B T\/m_alpha)$ #h(1.5em) #note[$T$ temperature, $k_B$ Boltzmann constant]])
  #at(1, 12, y: 122mm, align(center, note[$rho_(L i) \/ rho_(L e) = sqrt(m_i\/m_e) approx 43$ at equal $T$, #h(0.5em) $abs(omega_(c e)\/omega_(c i)) = m_i\/m_e approx 1836$]))
]
#slide(section: "motion-lorentz", title: [Thermonuclear scales])[
  #let f = gyro.fusion
  #at(1, 12, y: 0mm, align(center, note[hydrogen, $n_e = 10^20 "m"^(-3)$, $T_e = T_i = 10^8 "K"$ ($k_B T approx 8.6$ keV), $B = 5$ T]))
  #at(1, 6, y: 18mm, align(center, data-table(([frequency], [$"s"^(-1)$]), (
    ($abs(omega_(c e))$, sci(f.omega_ce)), ($omega_(p e)$, sci(f.omega_pe)), ($omega_(c i)$, sci(f.omega_ci))))))
  #at(7, 6, y: 18mm, align(center, data-table(([length], [m]), (
    ($rho_(L i)$, sci(f.rho_Li)), ($lambda_D$, sci(f.lambda_D)), ($rho_(L e)$, sci(f.rho_Le))))))
  #at(1, 12, y: 100mm, align(center)[$abs(omega_(c e)) tilde omega_(p e) >> omega_(c i), quad rho_(L e) tilde lambda_D << rho_(L i) << "machine size"$])
  #at(1, 12, y: 122mm, align(center, note[$omega_(p e) = sqrt(n_e e^2\/(epsilon_0 m_e))$ plasma frequency, $lambda_D = sqrt(epsilon_0 k_B T_e\/(n_e e^2))$ Debye length]))
]
#slide(section: "motion-lorentz", title: [Magnetized plasma])[
  #let item(f, name) = align(center)[#text(size: result-size, f) #v(6mm) #note(name)]
  #at(1, 12, y: 20mm, grid(columns: (1fr, 1fr), column-gutter: gutter,
    item($rho_L << L$, [orbit small against the gradient length $L$]),
    item($abs(omega_c) tau >> 1$, [many turns between collisions, $tau$ collision time]),
  ))
  #at(2, 10, y: 92mm, align(center, note[fusion: $rho_(L i) approx 3$ mm against minor radius $a approx 1$ m; equal $T$: $abs(omega_(c e)) tau_e > omega_(c i) tau_i$]))
]
// ------------------------------------------------------------ 2 E x B
#slide(section: "motion-exb", title: [$E times B$ drift])[
  #at(1, 6, y: 10mm, exb-picture(unit: 11mm))
  #at(7, 6, y: 0mm, formula-rows(gap: 7mm,
    ([ansatz], $bold(v) = v_parallel bold(b) + bold(v)_perp (t) + bold(v)_D$),
    ([gyration], $dif bold(v)_perp \/ dif t = (q_alpha \/ m_alpha) bold(v)_perp times bold(B)$),
    ([remainder], $0 = bold(E)_perp + bold(v)_D times bold(B)$),
    ([$times bold(B)$], $0 = bold(E) times bold(B) - B^2 bold(v)_D$),
  ))
  #at(7, 6, y: 60mm, result-box($bold(v)_D = (bold(E) times bold(B))/B^2$, [independent of $q_alpha$ and $m_alpha$]))
  #at(1, 12, y: 108mm, formula-rows(gap: 6mm,
    ([drift frame], [$bold(E)' = bold(E) + bold(v)_D times bold(B) = 0$ #h(0.6em) #note[exact: gyration + uniform drift ($bold(E) perp bold(B)$, $E\/B << c$)]]),
    ([along $bold(b)$], [$m_alpha dif v_parallel \/ dif t = q_alpha E_parallel$ #h(0.6em) #note[free acceleration]]),
  ))
  #at(1, 12, y: 140mm, note[$bold(b) = bold(B)\/B$, $bold(v)_D$ drift velocity, $bold(v)_perp (t)$ gyration, $bold(E)_perp$, $E_parallel$ field across and along $bold(B)$])
]
#animation-page("exb-drift", "exb_drift", section: "motion-exb")
#animation-page("exb-frame-change", "exb_frame_change", section: "motion-exb")
#slide(section: "motion-exb", title: [General force drift])[
  #at(1, 12, y: 6mm, formula-rows(gap: 10mm,
    ([force $bold(F) perp bold(B)$], $bold(F) + q_alpha bold(v)_D times bold(B) = 0$),
    ([$times bold(B)$], $bold(v)_D = bold(F)/q_alpha times bold(B)/B^2$),
    ([$bold(F) = q_alpha bold(E)$], [$bold(v)_D = (bold(E) times bold(B))\/B^2$ #h(0.6em) #note[same for all species: no charge separation]]),
    ([$bold(F) = m_alpha bold(g)$], [$bold(v)_D = m_alpha/q_alpha (bold(g) times bold(B))/B^2$ #h(0.6em) #note[ions and electrons opposite]]),
    ([current], $bold(j) = sum_alpha n_alpha q_alpha bold(v)_D = n (m_i + m_e) (bold(g) times bold(B))/B^2$),
  ))
  #at(1, 12, y: 134mm, note[$bold(F)$ constant force, $bold(g)$ gravitational acceleration, $n_alpha$ density of species $alpha$, hydrogen $n_i = n_e = n$])
  #at(1, 12, y: 148mm, note[#link("https://krystophny.github.io/plasma-skript/notebooks/orbits.html")[notebook: particle orbits and drifts]])
]
#animation-page("gravity-drift", "gravity_drift", section: "motion-exb")
// ------------------------------------ Leading-order guiding-centre motion
#slide(section: "motion-guiding-center", title: [Guiding centre])[
  #at(1, 12, y: 2mm, guiding-centre-picture(unit: 10.5mm))
  #at(1, 12, y: 74mm, lrows(size: 23pt, gap: 13mm,
    ([position], $bold(r) = bold(R) + bold(rho), quad bold(rho) = (bold(b) times bold(v)) \/ omega_c$),
    ([uniform $bold(B)$], $dot(bold(rho)) = bold(v)_perp quad => quad dot(bold(R)) = v_parallel bold(b)$),
    ([slow variation], $epsilon = v \/ (abs(omega_c) L) << 1$),
  ))
  #symbols[$bold(R)$ guiding centre, $bold(rho)$ gyration vector, $L$ field variation length, $v$ characteristic particle speed]
]
#slide(section: "motion-guiding-center", title: [Why follow magnetic field lines?])[
  #at(1, 12, y: 0mm, pad(left: 14mm, field-line-picture(unit: 10mm)))
  #at(1, 12, y: 59mm, lrows(size: 20pt, label-width: 42mm, gap: 12mm,
    ([differentiate], $dot(bold(R)) = v_parallel bold(b) - (dif (bold(b) \/ omega_c) \/ dif t) times bold(v)$),
    ([field varies over $L$], $dif (bold(b) \/ omega_c) \/ dif t = O(v \/ (abs(omega_c) L))$),
  ))
  #at(1, 12, y: 111mm, result-box($dot(bold(R)) = v_parallel bold(b) + O(epsilon v)$, [field-line following at leading order]))
  #symbols[$epsilon = v \/ (abs(omega_c)L) << 1$; for $v_parallel sim v_perp$, this is of order $rho_L \/ L$]
]
// ---------------------------------- Curvature: centrifugal force then drift
#slide(section: "motion-guiding-center", title: [Curvature drift])[
  #at(7, 5, y: 8mm, curvature-picture(unit: 12mm))
  #at(1, 7, y: rows-y, lrows(size: 22pt, label-width: 34mm, gap: 14mm,
    ([centrifugal force], $bold(F)_c = (m_alpha v_parallel^2) \/ R_c thin bold(e)_R$),
    ([general force drift], $bold(v)_D = (bold(F) times bold(B)) \/ (q_alpha B^2)$),
  ))
  #at(1, 8, y: result-y, result-box($bold(v)_D^"curv" = (m_alpha v_parallel^2) \/ (q_alpha B R_c) thin bold(e)_R times bold(b)$, [first-order drift]))
  #symbols[$R_c$ field-line radius of curvature, $bold(e)_R$ outward; $v_D^"curv"\/v = O(epsilon)$ when $R_c sim L$]
]
#animation-page("curvature-drift", "curvature_drift", section: "motion-guiding-center")
// ------------------------------------------- Magnetic moment of the gyro-orbit
#slide(section: "motion-guiding-center", title: [Magnetic moment])[
  #at(8, 5, y: 14mm, gyration-picture(unit: 10.2mm))
  #at(1, 6, y: 10mm, lrows(size: 24pt, label-width: 40mm,
    ([orbit current], $I = abs(q_alpha) abs(omega_c) \/ (2 pi)$),
    ([orbit area], $S = pi rho_L^2$),
  ))
  #at(1, 7, y: result-y, result-box($mu = I S = (m_alpha v_perp^2)\/(2 B), quad bold(mu) = -mu bold(b)$, [diamagnetic]))
  #symbols[$bold(mu)$ magnetic moment of the orbit; the circulating charge produces a moment opposite to $bold(B)$]
]
#slide(section: "motion-guiding-center", title: [Why is $mu$ nearly constant?])[
  #at(8, 4, y: 12mm, gyration-picture(unit: 9mm))
  #at(1, 8, y: rows-y, lrows(size: 22pt, label-width: 35mm, gap: 15mm,
    ([fast gyration], $T_c = 2 pi \/ abs(omega_c)$),
    ([gyroaction], $J = E_perp \/ abs(omega_c) = (m_alpha \/ abs(q_alpha)) mu$),
  ))
  #at(1, 8, y: result-y, result-box($J approx "const." quad => quad mu approx "const."$, [adiabatic invariant of a fast periodic motion]))
  #symbols[The magnetic field must vary little during one gyroperiod; the instantaneous particle moment may have small oscillations.]
]
#animation-page("mu-ramp", "mu_ramp", section: "motion-guiding-center")
#slide(section: "motion-guiding-center", title: [Adiabatic invariance: numerical example])[
  #at(3, 8, y: 0mm, plot("mu_ramp", columns: 8))
  #at(1, 12, y: 119mm, align(center)[Slower field variation $=>$ better conservation of $mu$])
  #symbols[Illustration: field strength doubles; $mu_i$ and $mu_f$ are the moments before and after the ramp.]
]
// ------------------------------------------ Mirror: effective one-dimensional potential
#slide(section: "motion-guiding-center", title: [Mirror force from the Hamiltonian])[
  #at(8, 5, y: 4mm, mirror-force-picture(unit: 12.5mm))
  #at(1, 8, y: rows-y, lrows(size: 22pt, label-width: 39mm, gap: 15mm,
    ([effective energy], $H_parallel = p_parallel^2 \/ (2 m_alpha) + mu B(s)$),
    ([Hamilton's equation], $dot(p)_parallel = - dif H_parallel \/ dif s$),
  ))
  #at(1, 8, y: result-y, result-box($m_alpha dot(v)_parallel = -mu thin dif B \/ dif s$, [mirror force toward weaker field]))
  #symbols[$s$ arc length along $bold(B)$, $p_parallel = m_alpha v_parallel$, $mu$ held constant to leading order; static field, $bold(E) = 0$]
]
#slide(section: "motion-guiding-center", title: [Magnetic mirror: reflection])[
  #at(8, 5, y: 4mm, mirror-picture(unit: 11.5mm))
  #at(1, 8, y: rows-y, lrows(size: 22pt, label-width: 40mm, gap: 15mm,
    ([energy], $W = (m_alpha v_parallel^2)\/2 + mu B = "const."$),
    ([turning point], $v_parallel = 0$),
  ))
  #at(1, 8, y: result-y, result-box($B_m = W \/ mu$, [parallel energy converted into perpendicular energy]))
  #symbols[$B_m$ magnetic field at reflection, $W$ conserved kinetic energy, $mu$ adiabatically invariant]
]
#slide(section: "motion-nonuniform-fields", title: [Mirror ratio and loss cone])[
  #at(8, 5, y: 8mm, loss-cone-picture(unit: 13mm))
  #at(1, 7, y: rows-y, lrows(label-width: 44mm,
    ([pitch angle], $sin theta.alt = v_perp \/ v$),
    ([$mu$ const., $bold(E) = 0$], $sin^2 theta.alt \/ B = "const."$),
    ([trapped], $B_0 \/ sin^2 theta.alt_0 < B_max$),
  ))
  #at(1, 7, y: result-y, result-box($sin^2 theta.alt_c = 1 \/ R_m$, [$R_m = B_max \/ B_0$ mirror ratio]))
  #symbols[$theta.alt_0$ pitch angle at the midplane, $theta.alt_c$ loss-cone angle; speed $v$ constant in a static magnetic field]
]
#animation-page("magnetic-mirror", "magnetic_mirror", section: "motion-nonuniform-fields")
#slide(section: "motion-nonuniform-fields", title: [Loss cone in velocity space])[
  #at(1, 12, y: 0mm, align(center, plot("loss_cone", columns: 11)))
  #at(1, 12, y: 114mm, align(center)[$v_parallel^2 (z) = v^2 - v_(perp 0)^2 B(z) \/ B_0$])
  #at(1, 12, y: 128mm, align(center)[lost $= 1 - cos theta.alt_c = 1 - sqrt(1 - 1 \/ R_m)$ #h(1em) #note[isotropic velocity distribution]])
  #symbols[$v_(perp 0)$ at midplane, $R_m = B_max \/ B_0$, $L_m$ mirror half-length]
]
// --------------------------------------- Grad-B: same moment, perpendicular force
#slide(section: "motion-nonuniform-fields", title: [Grad-$B$ drift])[
  #at(6, 7, y: 0mm, gradb-picture(unit: 12mm))
  #at(1, 6, y: rows-y, lrows(size: 23pt, label-width: 31mm, gap: 15mm,
    ([effective energy], $U_mu = mu B$),
    ([moment force], $bold(F)_mu = -mu grad B$),
  ))
  #at(1, 6, y: 90mm, result-box($bold(v)_D^(grad B) = (mu \/ q_alpha) (bold(B) times grad B)\/B^2$, [perpendicular force drift]))
  #symbols[The parallel part of $-mu grad B$ is the mirror force; the perpendicular part causes this first-order drift.]
]
#animation-page("grad-b-drift", "grad_b_drift", section: "motion-nonuniform-fields")
// ---------------------------------------------------- 13 polarization
#slide(section: "motion-polarization", title: [Polarization drift])[
  #at(1, 12, y: 6mm, formula-rows(gap: 12mm,
    ([slow $bold(E)_perp (t)$], $bold(v) = v_parallel bold(b) + (bold(E) times bold(B))/B^2 + bold(v)_D^"pol" + bold(v)_perp$),
    ([drift], $bold(v)_D^"pol" = m_alpha/(q_alpha B^2) pdv(bold(E)_perp, t)$),
    ([current], $bold(j)_"pol" = sum_alpha n_alpha q_alpha bold(v)_D^"pol" = (sum_alpha n_alpha m_alpha)/B^2 pdv(bold(E)_perp, t)$),
    ([validity], $omega << abs(omega_c)$),
  ))
  #at(1, 12, y: 128mm, note[$bold(E)_perp$ field across $bold(B)$, $omega$ its rate of change, $n_alpha$ density of species $alpha$; carried mainly by ions])
]
#animation-page("polarization-drift", "polarization_drift", section: "motion-polarization")
// ---------------------------------------------------------- 14 table
#slide(title: [Drifts])[
  #at(1, 12, y: 4mm, align(center, data-table(
    ([drift], $bold(v)_D$, [ions vs electrons], [mass]),
    (
      ([$E times B$], $(bold(E) times bold(B))\/B^2$, [same], [none]),
      ([gravity], $(m_alpha\/q_alpha) (bold(g) times bold(B))\/B^2$, [opposite], [$prop m_alpha$]),
      ([grad-$B$], $(mu\/q_alpha) (bold(B) times grad B)\/B^2$, [opposite], [$prop m_alpha v_perp^2$]),
      ([curvature], $m_alpha v_parallel^2 (bold(e)_R times bold(b))\/(q_alpha B R_c)$, [opposite], [$prop m_alpha v_parallel^2$]),
      ([polarization], $(m_alpha\/(q_alpha B^2)) thin partial bold(E)_perp \/ partial t$, [opposite], [$prop m_alpha$]),
    ),
    align: left)))
  #at(1, 12, y: 112mm, align(center)[#note[vacuum field:] #h(0.6em) $bold(v)_D^"curv" + bold(v)_D^(grad B) = m_alpha/(q_alpha B R_c) (v_parallel^2 + v_perp^2/2) bold(e)_R times bold(b)$])
  #at(1, 12, y: 134mm, align(center, note[$bold(v)_D = (bold(F)\/q_alpha) times bold(B)\/B^2$ for a force $bold(F)$; opposite drifts carry currents]))
]
// ---------------------------------------------- 15 cyclotron resonance
#slide(section: "motion-cyclotron-resonance", title: [Cyclotron resonance])[
  #at(1, 12, y: 2mm, formula-rows(gap: 8mm,
    ([rotating $bold(E)$], [$E_"cw" = E_x + i E_y = E_0 e^(-i s omega t)$ #h(0.6em) #note[$s = +1$ clockwise, $s = -1$ counterclockwise]]),
    ([$v_"cw" = v_x + i v_y$], $dif v_"cw" \/ dif t = -i omega_c v_"cw" + (q_alpha \/ m_alpha) E_"cw"$),
    ([from rest], $v_"cw" = (q_alpha E_0)/m_alpha e^(-i omega_c t) (e^(i Delta t) - 1)/(i Delta), quad Delta = omega_c - s omega$),
    ([modulus], $v_perp = abs(v_"cw") = (abs(q_alpha) E_0)/m_alpha abs((2 sin(Delta t\/2))/Delta)$),
  ))
  #at(2, 10, y: 72mm, result-box(align(center, $Delta = 0: quad v_perp = (abs(q_alpha) E_0)/m_alpha t, quad W = (q_alpha^2 E_0^2)/(2 m_alpha) t^2$),
    [resonance $s omega = omega_c$: ions clockwise, electrons counterclockwise]))
  #at(1, 12, y: 134mm, note[$bold(B) = B bold(e)_z$ out of the page, $omega_c = q_alpha B\/m_alpha$ signed, $Delta$ detuning: off resonance $v_perp$ beats with period $2 pi\/abs(Delta)$; $W$ kinetic energy])
]
#animation-page("cyclotron-resonance", "cyclotron_resonance", section: "motion-cyclotron-resonance")
