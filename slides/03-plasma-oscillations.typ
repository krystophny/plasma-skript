// Plasma Physics live deck, script chapter 3. Level-2 plan and lecturer
// cues: 03-plasma-oscillations.md. Build: scripts/build-slides.sh.
#import "theme.typ": *

#show: deck.with(chapter: 3)

// 3.1 Electron plasma oscillations: animation, LIVE, summary.
#animation-page("plasma-oscillation", "plasma_oscillation",
  section: "intro-plasma-oscillations")
#blanks(2)
#summary(
  assumptions: (
    ([immobile ions], $n_i = n_0$),
    ([cold electrons], $k_B T_e -> 0$),
    ([small displacement $xi$], $abs(xi) << L$),
    ([no collisions, no field], $omega_(p e) tau >> 1$),
  ),
  symbols: [$n_0$~density, $T_e$~electron temperature, $L$~slab width,
    $tau$~collision time],
  derivation: (
    ([sheet charge], $sigma = e n_0 xi$),
    (step[Gauss], $E = display((e n_0 xi)/epsilon_0)$),
    (step[Newton], $m_e dot.double(xi) = -e E = -display((n_0 e^2)/epsilon_0) xi$),
    (step[divide by $m_e$], $dot.double(xi) + omega_(p e)^2 xi = 0$),
    (step[solve], $xi = xi_0 cos(omega_(p e) t + delta)$),
  ),
  result: $omega_(p e) = sqrt(display((n_0 e^2)/(epsilon_0 m_e)))$,
  result-name: [$omega_(p e)$~electron plasma frequency],
  below-result: [$f_(p e) = display(omega_(p e)/(2 pi)) approx 8.98 thin sqrt(n_0 slash "m"^(-3)) thin "Hz"$],
  plot-name: "plasma_frequency",
)
