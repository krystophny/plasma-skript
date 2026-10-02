// Plasma Physics live deck, script chapter 1. Level-2 plan and lecturer
// cues: 01-introduction.md. Photo credits: photos/credits.md.
// Build: scripts/build-slides.sh.
#import "theme.typ": *

#show: deck.with(chapter: 1)

// 1.1 Plasma as a collective state. Photo story, then collective response
// (animation, LIVE, summary) and the empty n-T plane (LIVE).
#photo-page("sun_flare_sdo.jpg", [NASA/SDO, public domain], "photo-sun",
  section: "intro-plasma-state")
#photo-page("aurora_iss.jpg", [NASA, ISS Expedition 23, public domain], "photo-aurora")
#photo-page("carina_eso.jpg", [ESO, CC BY 4.0], "photo-carina")
#photo-page("hall_thruster_jpl.jpg", [NASA/JPL-Caltech, public domain], "photo-thruster")

#animation-page("collective-response", "collective_response")
#blanks(2)
#summary(
  assumptions: (
    ([species $s$], $rho_q = sum_s q_s n_s$),
    ([electrons, ions], $q_e = -e, quad q_i = Z_i e$),
    ([screened charge $Q$], $phi = display(Q/(4 pi epsilon_0 r)) e^(-r slash lambda_D)$),
  ),
  symbols: [$rho_q$~charge density, $q_s$~charge, $n_s$~density,
    $e$~elementary charge, $Z_i$~ion charge state, $phi$~potential,
    $r$~distance,
    $lambda_D$~Debye length (chapter~2)],
  derivation: (
    ([insert charges], $rho_q = e (sum_i Z_i n_i - n_e)$),
    (step[Gauss], $Q_"enc" = -4 pi epsilon_0 r^2 display((dif phi)/(dif r))$),
    ([], $Q_"enc" = Q (1 + r slash lambda_D) e^(-r slash lambda_D)$),
    (step[$r >> lambda_D$], $Q_"enc" -> 0, quad rho_q approx 0$),
  ),
  result: $n_e approx sum_i Z_i n_i$,
  result-name: [quasineutrality],
  plot-name: "enclosed_charge",
  caption: [$Q_"enc"$~net charge inside radius $r$],
)
#plot-page("nt_plane", columns: 10)
#blanks(2)

// 1.2 Speed, energy, and temperature: heating widens, acceleration shifts
// the Maxwellian; LIVE; summary; thermal speeds in eV and K.
#plot-pair("maxwellian_heating", "maxwellian_drift",
  section: "intro-speed-energy-temperature")
#blanks(2)
#summary(
  assumptions: (
    ([kinetic energy], $epsilon_("kin",s) = m_s v^2 slash 2$),
    ([thermal energy], $epsilon_("th",s) = k_B T_s$),
    ([Maxwellian], $f prop exp(-(v_x - u_s)^2 slash v_"th"^2)$),
    ([temperatures], $T_e != T_i$),
  ),
  symbols: [$m_s$~mass, $v$~speed, $v_x$~velocity component, $u_s$~drift,
    $T_s$~temperature, $k_B$~Boltzmann constant, $f$~distribution function],
  derivation: (
    ([convention], $m_s v_"th"^2 slash 2 = k_B T_s$),
    (step[variance], $chevron.l (v_x - u_s)^2 chevron.r = k_B T_s slash m_s$),
    (step[speeds], $v_"peak" = v_"th"$),
    ([], $chevron.l v chevron.r = display(2/sqrt(pi)) thin v_"th"$),
    ([], $v_"rms" = sqrt(3 slash 2) thin v_"th"$),
  ),
  result: $v_("th",s) = sqrt(display((2 k_B T_s)/m_s))$,
  result-name: [$v_"th"$~thermal speed],
  plot-name: "maxwell_speed",
  caption: [$F$~speed distribution, $chevron.l v chevron.r$~mean speed],
)
#plot-page("thermal_speed", columns: 8,
  below: [$k_B T = 1 "eV" quad <-> quad T approx 1.16 dot 10^4 "K"$])

// 1.3 Characteristic scales and ordering: LIVE from the titled page, then
// the summary over the full-width plot.
#section-page("intro-scales")
#blanks(1)
#summary-wide(
  assumptions: (
    ([density], $n_e$),
    ([temperature], $k_B T_e$),
    ([magnetic field], $B$),
    ([system size], $L$),
  ),
  derivation: (
    ([Debye length], $lambda_D = sqrt(epsilon_0 k_B T_e slash (n_e e^2))$),
    ([plasma frequency], $omega_(p e) = sqrt(n_e e^2 slash (epsilon_0 m_e))$),
    ([cyclotron frequency], $omega_(c e) = e B slash m_e$),
    ([gyroradius], $rho_e = v_("th",e) slash omega_(c e)$),
    ([mean free path], $lambda_"mfp" = chevron.l v chevron.r slash nu_(e i)$),
  ),
  result: $ ell &<< L quad &&"average" \ ell &gt.tilde L quad &&"resolve" $,
  result-name: none,
  notes: [$ell$~any length scale],
  derivation-notes: [$nu_(e i)$~electron–ion collision rate],
  plot-name: "scale_ordering",
)

// 1.4 From microscopic particles to a model: animation and model ladder.
#animation-page("particles-to-moments", "particles_to_moments",
  section: "intro-model-hierarchy")
#slide[
  #align(center, model-ladder())
]

#credits-page(
  (
    ("photo-sun",
      [NASA/SDO (Scientific Visualization Studio), X5.8 flare, 11 May 2024, public domain.],
      "svs.gsfc.nasa.gov/14589"),
    ("photo-aurora",
      [NASA, ISS Expedition 23, aurora australis, 29 May 2010, public domain.],
      "commons.wikimedia.org/wiki/File:Aurora_Australis_From_ISS.JPG"),
    ("photo-carina",
      [ESO, Carina Nebula (eso0905a), CC BY 4.0 (creativecommons.org/licenses/by/4.0).],
      "eso.org/public/images/eso0905a"),
    ("photo-thruster",
      [NASA/JPL-Caltech, 6 kW xenon Hall thruster, 2007, public domain.],
      "commons.wikimedia.org/wiki/File:Xenon_hall_thruster.jpg"),
  ),
  [Plots, diagrams and animations: Christopher Albert, CC BY 4.0.],
)
