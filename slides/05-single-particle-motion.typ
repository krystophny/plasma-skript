#import "theme.typ": *
#import "@preview/physica:0.9.8": dv, pdv, grad
#import "motion-drawings.typ": gyration-picture, exb-picture, curvature-picture, loss-cone-picture, guiding-centre-picture, mirror-force-picture, faraday-picture
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
// ------------------------------------------------------------ 1 gyration
#slide(section: "motion-lorentz", title: [Gyration: force balance])[
  #at(1, 6, y: 6mm, gyration-picture(electron: false))
  #at(7, 6, y: 6mm, formula-rows(
    ([Lorentz force], $bold(F) = q_alpha bold(v) times bold(B)$),
    ([$bold(v) perp bold(B)$], $abs(bold(F)) = abs(q_alpha) v_perp B$),
    ([centrifugal = Lorentz], $(m_alpha v_perp^2)/rho_L = abs(q_alpha) v_perp B$),
  ))
  #at(7, 6, y: 76mm, result-box($abs(omega_c) = (abs(q_alpha) B)/m_alpha, quad rho_L = v_perp/abs(omega_c)$, [gyrofrequency, Larmor radius]))
  #at(1, 12, y: 134mm, note[$q_alpha$, $m_alpha$ charge and mass of species $alpha$; $omega_c = q_alpha B\/m_alpha$ signed; $B = abs(bold(B))$; $v_perp$ speed across $bold(B)$])
]
#slide(section: "motion-lorentz", title: [Equations of motion])[
  #at(1, 5, y: 6mm, gyration-picture(electron: false, force: false, axes: true, unit: 10mm))
  #at(6, 7, y: 4mm, formula-rows(gap: 7mm,
    ([$bold(B) = B bold(e)_z$], $dif v_x \/ dif t = omega_c v_y, quad dif v_y \/ dif t = -omega_c v_x$),
    ([], $dif v_z \/ dif t = 0$),
    ([$dif \/ dif t$], $dif^2 v_x \/ dif t^2 = omega_c dif v_y \/ dif t = -omega_c^2 v_x$),
    ([solution], $v_x = v_perp cos(omega_c t + phi)$),
    ([], $v_y = -v_perp sin(omega_c t + phi)$),
    ([integrate], $x = x_0 + (v_perp \/ omega_c) sin(omega_c t + phi)$),
    ([], $y = y_0 + (v_perp \/ omega_c) cos(omega_c t + phi)$),
    ([along $bold(B)$], $z = z_0 + v_parallel t$),
  ))
  #at(1, 12, y: 124mm, note[$phi$ gyrophase, $(x_0, y_0)$ guiding centre, $abs(v_perp\/omega_c) = rho_L$, $v_parallel$ speed along $bold(B)$])
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
]
#animation-page("gravity-drift", "gravity_drift", section: "motion-exb")
// ------------------------------------------------- 4 guiding centre
#slide(section: "motion-guiding-center", title: [Guiding centre])[
  #at(1, 6, y: 10mm, guiding-centre-picture())
  #at(7, 6, y: 6mm, formula-rows(gap: 8mm,
    ([split], $bold(r) = bold(R) + bold(rho), quad abs(bold(rho)) = rho_L$),
    ([velocity], $bold(v) = v_parallel bold(b) + bold(v)_D + bold(v)_perp$),
    ([space], $rho_L \/ L << 1$),
    ([time], $omega \/ abs(omega_c) << 1$),
  ))
  #at(1, 12, y: 118mm, note[$bold(R)$ guiding centre, $bold(rho)$ gyration vector, $bold(v)_perp$ fast gyration velocity, $L$ field-variation length, $omega$ rate of change of the fields])
]
// ------------------------------------------------------- 5 curvature
#slide(section: "motion-nonuniform-fields", title: [Curvature drift])[
  #at(1, 5, y: 4mm, curvature-picture())
  #at(6, 7, y: 0mm, formula-rows(gap: 9mm,
    ([field line], $(bold(b) dot grad) bold(b) = -bold(e)_R / R_c$),
    ([guiding centre], $bold(a) = -v_parallel^2/R_c bold(e)_R$),
    ([centrifugal], $bold(F) = (m_alpha v_parallel^2)/R_c bold(e)_R$),
    ([force drift], $bold(v)_D^"curv" = (m_alpha v_parallel^2)/(q_alpha B R_c) bold(e)_R times bold(b)$),
  ))
  #at(6, 7, y: 92mm, result-box($bold(v)_D^"curv" = rho_parallel Omega_parallel bold(e)_R times bold(b)$, [$rho_parallel = v_parallel\/omega_c$, #h(0.4em) $Omega_parallel = v_parallel\/R_c$]))
  #at(1, 12, y: 140mm, note[$R_c$ radius of curvature, $bold(e)_R$ unit vector away from the centre of curvature, $bold(a)$ acceleration])
]
#animation-page("curvature-drift", "curvature_drift", section: "motion-nonuniform-fields")
// ------------------------------------------------- 6 magnetic moment
#slide(section: "motion-guiding-center", title: [Magnetic moment])[
  #at(1, 7, y: 4mm, gyration-picture(unit: 9mm))
  #at(8, 5, y: 4mm, formula-rows(gap: 7mm,
    ([current], $I = (abs(q_alpha) abs(omega_c))/(2 pi)$),
    ([area], $S = pi rho_L^2$),
    ([direction], $bold(mu) = -mu bold(b)$),
  ))
  #at(8, 5, y: 70mm, result-box($mu = I S = (m_alpha v_perp^2)/(2 B)$, [perpendicular kinetic energy / $B$]))
  #at(1, 12, y: 130mm, note[orbit current left-handed about $bold(B)$ for ions and electrons: diamagnetic, $bold(mu)$ against $bold(B)$])
]
// ---------------------------------------------- 7 mirror force, grad-B
#slide(section: "motion-nonuniform-fields", title: [Mirror force and grad-$B$ drift])[
  #at(1, 5, y: 4mm, mirror-force-picture())
  #at(6, 7, y: 0mm, formula-rows(gap: 7mm,
    ([$grad dot bold(B) = 0$], $(1\/r) thin partial (r B_r) \/ partial r = -partial B_z \/ partial z$),
    ([axis, $B_z (z)$], $B_r = -(r\/2) thin partial B_z \/ partial z$),
    ([average, $r = rho_L$], $⟨ q_alpha (bold(v) times bold(B))_z ⟩ = abs(q_alpha) v_perp B_r$),
    ([], $= -abs(q_alpha) v_perp (rho_L\/2) thin partial B \/ partial z$),
    ([$abs(q_alpha) v_perp rho_L \/ 2 = mu$], $F_parallel = -mu thin partial B \/ partial s$),
  ))
  #at(1, 12, y: 86mm, formula-rows(gap: 9mm,
    ([general], $bold(F) = -mu grad B = -grad(mu B)$),
    ([$perp$ part], $bold(v)_D^(grad B) = bold(F)_perp/q_alpha times bold(B)/B^2 = mu/q_alpha (bold(B) times grad B)/B^2$),
  ))
  #at(1, 12, y: 140mm, note[$r$, $z$ cylinder coordinates about the orbit axis, $s$ arc length along $bold(B)$, $⟨ dot ⟩$ average over one gyration])
]
#animation-page("grad-b-drift", "grad_b_drift", section: "motion-nonuniform-fields")
// ------------------------------------------------- 8 conservation laws
#slide(section: "motion-guiding-center", title: [Energy conservation])[
  #at(1, 12, y: 6mm, formula-rows(gap: 9mm,
    ([magnetic force], $q_alpha (bold(v) times bold(B)) dot bold(v) = 0$),
    ([static $bold(E) = -grad Phi$], $dv(, t) ((m_alpha v^2)/2 + q_alpha Phi) = 0$),
    ([$v^2 = v_parallel^2 + v_perp^2$], $(m_alpha v_perp^2)/2 = mu B$),
  ))
  #at(3, 8, y: 84mm, result-box(align(center, $(m_alpha v_parallel^2)/2 + mu B + q_alpha Phi = W = "const."$), [exact in static fields, $mu$ and $B$ at the particle]))
  #at(1, 12, y: 140mm, note[$Phi$ electrostatic potential, $W$ total energy])
]
#slide(section: "motion-guiding-center", title: [$mu$ from Faraday's law])[
  #at(1, 5, y: 4mm, faraday-picture())
  #at(6, 7, y: 0mm, formula-rows(gap: 6mm,
    ([one turn], $delta ((m_alpha v_perp^2)/2) = q_alpha integral.cont bold(E) dot dif bold(l)$),
    ([Stokes], $q_alpha integral.cont bold(E) dot dif bold(l) = abs(q_alpha) pi rho_L^2 pdv(B, t)$),
    ([per turn], $delta B = pdv(B, t) (2 pi)/abs(omega_c)$),
    ([$=>$], $delta ((m_alpha v_perp^2)/2) = mu delta B$),
  ))
  #at(6, 7, y: 92mm, result-box($delta mu = delta(m_alpha v_perp^2\/2)/B - mu (delta B)/B = 0$, none))
  #at(1, 12, y: 136mm, note[$integral.cont$ along the orbit, left-handed about $bold(B)$ for $q_alpha > 0$; slow change $abs(partial B\/partial t) << abs(omega_c) B$, $E_parallel = 0$, no $E times B$ drift of the guiding centre])
]
#animation-page("mu-ramp", "mu_ramp", section: "motion-guiding-center")
#slide(section: "motion-guiding-center", title: [$mu$ from the mirror force])[
  #at(1, 12, y: 4mm, formula-rows(gap: 8mm,
    ([along $bold(b)$], $m_alpha thin dif v_parallel \/ dif t = -mu thin partial B \/ partial s$),
    ([$times v_parallel$, #h(0.3em) $dif s\/dif t = v_parallel$], $dif (m_alpha v_parallel^2 \/ 2) \/ dif t = -mu thin dif B \/ dif t$),
    ([energy, $Phi = 0$], $dif (m_alpha v_parallel^2 \/ 2 + mu B) \/ dif t = 0$),
    ([subtract], $B thin dif mu \/ dif t = 0$),
  ))
  #at(2, 10, y: 80mm, result-box(align(center, $mu = "const." quad => quad v_parallel = 0 "where" B = W\/mu$), [mirror point]))
  #at(1, 12, y: 132mm, note[adiabatic invariant: constant to leading order in $epsilon = rho_L\/L$ or $1\/(abs(omega_c) tau)$, $tau$ time of change])
  #at(1, 12, y: 142mm, note[uniform fields, also uniform $bold(E) perp bold(B)$ with $mu$ in the drift frame: exactly constant])
]
#slide(section: "motion-guiding-center", title: [$mu$ in the Hamiltonian picture])[
  #at(1, 12, y: 2mm, formula-rows(gap: 9mm,
    ([action of the gyration], $J = integral.cont bold(p)_perp dot dif bold(l) = integral.cont (m_alpha bold(v)_perp + q_alpha bold(A)) dot dif bold(l)$),
    ([$bold(A) = bold(B) times bold(r) \/ 2$], $J = 2 pi m_alpha v_perp rho_L - pi abs(q_alpha) B rho_L^2 = (2 pi m_alpha \/ abs(q_alpha)) mu = abs(q_alpha) pi rho_L^2 B$),
    ([periodic motion], [action $=$ adiabatic invariant #h(0.6em) #note[slowly shortened pendulum, Solvay 1911]]),
    ([guiding centre], $H = m_alpha v_parallel^2 \/ 2 + mu B(bold(R)) + q_alpha Phi(bold(R))$),
    ([$phi$ ignorable], [$p_phi = (m_alpha \/ q_alpha) mu = "const."$ #h(0.6em) #note[Noether]]),
    ([potential $mu B$], $m_alpha dif v_parallel \/ dif t = -mu thin partial B\/partial s - q_alpha thin partial Phi \/ partial s, quad bold(F)_perp = -grad_perp (mu B) -> bold(v)_D^(grad B)$),
  ))
  #at(1, 12, y: 108mm, note[$bold(p)_perp$ canonical momentum across $bold(B)$, $bold(A)$ vector potential, $bold(r)$ from the orbit centre])
  #at(1, 12, y: 118mm, note[$dif bold(l)$ along the orbit, $pi rho_L^2 B$ flux through it, $bold(R)$ guiding centre, $p_phi$ conjugate to $phi$])
  #at(1, 12, y: 138mm, note[exact for the guiding centre, an expansion in $epsilon = rho_L\/L$: $mu$ adiabatic invariant])
]
// --------------------------------------------- 9 adiabatic invariance
#slide(section: "motion-guiding-center", title: [Adiabatic invariance])[
  #at(3, 8, y: 0mm, plot("mu_ramp", columns: 8))
  #at(1, 12, y: 110mm, align(center)[$B: B_0 -> 2 B_0, quad bold(E) = -(1\/2) (partial B \/ partial t) thin bold(e)_z times bold(r)$])
  #at(1, 12, y: 122mm, align(center)[tanh: $B\/B_0 = 3\/2 + tanh(t\/tau)\/2$ #h(2em) linear: kinks at $t = plus.minus tau$])
  #at(1, 12, y: 140mm, note[$tau$ ramp time, $omega_(c 0) = q_alpha B_0\/m_alpha$, $bold(r)$ position from the axis; Boris integration])
]
// ---------------------------------------------------------- 10 mirror
#animation-page("magnetic-mirror", "magnetic_mirror", section: "motion-nonuniform-fields")
#slide(section: "motion-nonuniform-fields", title: [Mirror ratio and loss cone])[
  #at(1, 6, y: 10mm, loss-cone-picture())
  #at(7, 6, y: 0mm, formula-rows(gap: 6mm,
    ([pitch angle], $sin alpha = v_perp \/ v$),
    ([$mu$, $W$ const.], $mu = m_alpha v^2 sin^2 alpha \/ (2 B) quad => quad sin^2 alpha \/ B = "const."$),
    ([mirror point], $alpha = 90 degree "at" B = B_0 \/ sin^2 alpha_0$),
    ([trapped], $B_0 \/ sin^2 alpha_0 < B_max$),
  ))
  #at(7, 6, y: 86mm, result-box($sin^2 alpha_c = 1/R_m$, [$R_m = B_max\/B_0$ mirror ratio]))
  #at(1, 12, y: 144mm, note[$alpha$ angle between $bold(v)$ and $bold(B)$, $alpha_0$ at the midplane field $B_0$, $B_max$ at the throat, $v$ speed])
]
#slide(section: "motion-nonuniform-fields", title: [Loss cone in velocity space])[
  #at(1, 12, y: 0mm, align(center, plot("loss_cone", columns: 11)))
  #at(1, 12, y: 116mm, align(center)[trapped if $v_parallel^2 (z) = v^2 - v_(perp 0)^2 B(z)\/B_0$ reaches 0 before the throat #h(1.5em) lost: $1 - sqrt(1 - 1\/R_m)$])
  #at(1, 12, y: 132mm, note[isotropic Maxwellian at the midplane ($v_(perp 0)$), $v_"th" = sqrt(2 k_B T\/m_alpha)$])
  #at(1, 12, y: 142mm, note[field $B(z)\/B_0 = 1 + (R_m - 1)(z\/L)^2$, throat at $z = L$])
]
// ---------------------------------------------------- 11 polarization
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
// ---------------------------------------------------------- 12 table
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
