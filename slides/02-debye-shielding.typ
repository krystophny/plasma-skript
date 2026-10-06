// Plasma Physics live deck, script chapter 2. Level-2 plan and lecturer
// cues: 02-debye-shielding.md. Build: scripts/build-slides.sh.
#import "theme.typ": *
#import "@preview/physica:0.9.8": laplacian

#show: deck.with(chapter: 2)

// 2.1 Debye shielding. Point charge: animation, LIVE, summary.
#animation-page("debye-shielding", "debye_shielding", section: "intro-debye-shielding")
#blanks(2)
#summary(
  assumptions: (
    ([immobile ions], $n_i = n_0$),
    ([Boltzmann electrons], $n_e = n_0 exp(e phi slash k_B T_e)$),
    ([weak potential], $e abs(phi) << k_B T_e$),
    ([point charge $Q$], $phi -> display(Q/(4 pi epsilon_0 r)), quad r -> 0$),
  ),
  symbols: [$n_0$~density, $phi$~potential, $T_e$~electron temperature,
    $r$~distance from the charge],
  derivation: (
    ([Poisson], $laplacian phi = -rho_q slash epsilon_0$),
    ([charge density], $rho_q = e (n_i - n_e)$),
    (step[linearize], $rho_q approx -display((e^2 n_0)/(k_B T_e)) phi$),
    (step[substitute], $laplacian phi = phi slash lambda_D^2$),
    (step[$phi = w slash r$], $w'' = w slash lambda_D^2$),
    (step[decay], $w prop e^(-r slash lambda_D)$),
  ),
  result: $phi = display(Q/(4 pi epsilon_0 r)) e^(-r slash lambda_D), quad
    lambda_D = sqrt(display((epsilon_0 k_B T_e)/(n_0 e^2)))$,
  result-name: [$lambda_D$~Debye length],
  plot-name: "debye_potential",
)

// 2.2 Finite charge distribution: the script's comparison pair, then LIVE.
#plot-pair("debye_potential", "debye_sphere_potential",
  section: "debye-finite-source",
  right-caption: [$R$~radius of the charged sphere])
#blanks(2)

// Particle evidence (kin6d): the screening cloud is an ensemble average.
#animation-page("debye-shielding-particles", "debye_shielding_particles", section: "debye-finite-source")

// 2.3 Plasma parameter: illustration, LIVE, summary, regime map.
#slide(section: "debye-collective-validity")[
  #at(1, 6, align(center)[$N_D approx 3$])
  #at(7, 6, align(center)[$N_D approx 300$])
  #at(1, 6, y: 14mm, debye-sphere(3, 11, 3.4mm, exact: true))
  #at(7, 6, y: 14mm, debye-sphere(300, 5, 1.5mm))
  #at(1, 12, y: 14mm + cols(6) + 4mm, text(fill: muted)[$N_D$ electrons
    in a sphere of radius $lambda_D$])
]
#blanks(2)
#summary(
  assumptions: (
    ([uniform density], $n_e = n_0$),
    ([Debye sphere], $r <= lambda_D$),
    ([mean spacing $a$], $display((4 pi)/3) a^3 n_0 = 1$),
  ),
  derivation: (
    ([count], $N_D = display(integral_0^(lambda_D)) 4 pi r^2 n_0 dif r$),
    (step[integrate], $N_D = display((4 pi)/3) n_0 lambda_D^3$),
    ([coupling], $Gamma = display(e^2/(4 pi epsilon_0 a k_B T_e))$),
    (step[insert $a$, $lambda_D$], $Gamma N_D^(2 slash 3) = display(1/3)$),
  ),
  result: $N_D >> 1 quad <==> quad Gamma << 1$,
  result-name: [$N_D$~plasma parameter \ $Gamma$~coupling parameter],
  plot-name: "debye_number",
)
#plot-page("nt_map", columns: 10,
  below: grid(columns: (1fr, 1fr),
    align(left)[$lambda_D << L, quad N_D >> 1$],
    align(right, text(fill: muted)[$L$ system size])))
