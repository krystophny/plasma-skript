# Temperature, entropy, and thermal ionization

LOOK deck; THINK derivations take place in the separate Goodnotes notebook.
No blank or titled writing pages. Stable script labels resolve through the outline.

Online deck: [present/02-thermal-equilibrium/](https://krystophny.github.io/plasma-skript/present/02-thermal-equilibrium/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

| Page | Title | Kind | Script section label | Lecturer cue |
|---|---|---|---|---|
| 1 | Title | static | thermal-equilibrium | Entropy pays an energy cost. |
| 2 | Temperature meaning | static | thermal-temperature | Distinguish energy from entropy slope. |
| 3 | Microstate counting | static | thermal-microstates | Enumerate every binary configuration. |
| 4 | Additive entropy | static | thermal-microstates | Multiply counts, then take a logarithm. |
| 5 | Two exchanging boxes | static | thermal-temperature | A gains what B loses. |
| 6 | Entropy slope | static | thermal-temperature | Hold volume, number, and momentum fixed. |
| 7 | Reservoir weight | static | thermal-boltzmann | First-order entropy expansion. |
| 8 | Boltzmann factor by counting | plot | thermal-boltzmann | One oscillator against an Einstein solid of N oscillators sharing Q = N quanta: count reservoir states, P(E) falls on exp(-E/k_B T) with k_B T = eps/ln 2; the deviation falls as 1/N (14 %, 1.3 %, 0.13 % at E = eps for N = 4, 40, 400). |
| 9 | Hard disks relax to the Maxwellian | animation | thermal-boltzmann | Predict first: all disks at one speed. Collisions alone spread the histogram onto 2v exp(-v^2/v_0^2)/v_0^2 within about four collisions per disk; entropy rises, then flat at 1 + ln pi; energy exact. Then the drifting Maxwellian. |
| 10 | Drifting Maxwellian | static | thermal-boltzmann | Fixed total momentum sets mean flow. |
| 11 | Thermal particle slots | static | thermal-saha | Count translational and internal choices. |
| 12 | Adding and removing | static | thermal-saha | Factorials encode indistinguishability. |
| 13 | One ionization | static | thermal-saha | Three particle factors and one reservoir penalty. |
| 14 | Heavy particle cancellation | static | thermal-saha | Neutral and ion masses nearly coincide. |
| 15 | Saha composition balance | static | thermal-saha | New electron freedom is the large factor. |
| 16 | Ionization fraction | static | thermal-ionization | Nucleus conservation and neutrality. |
| 17 | Competing statistical factors | static | thermal-ionization | Equal factors give x=0.618; half needs A=0.5. |
| 18 | Thermal ionization threshold | static | thermal-ionization | Exact logarithm, computed table, qualified 10⁴ K. |
| 19 | Equilibrium validity | static | thermal-ionization | LTE versus coronal and rate balance. |
| 20 | Source credits | static | thermal-equilibrium | Sources and AI disclosure. |

## Scientific inputs

Lecturer notes, 2026-10-06, rendered pages 1–3; chosen dilute slot-counting route.
Thermal speed: v_th,s = sqrt(2 k_B T_s/m_s), as in intro-speed-energy-temperature.
Equations: thermal-ionization-ratio, thermal-saha-equation,
thermal-fraction-solution, thermal-half-temperature.
Oracle and figures: derivations/chapters/ch02_thermal_equilibrium.py.
The brief's rough 6,000–15,000 K range is replaced by the oracle's 3,226–26,230 K
over 10⁶–10²⁶ m⁻³. Exact half ionization requires ln(4/(n lambda_e³)).

## Counting and relaxation visuals (2026-10-26)

`derivations/plot_boltzmann_counting.py` writes `boltzmann_counting` (page 8):
exact P(n) = W_rest(N, Q - n)/W_total for one oscillator and an N-oscillator
Einstein solid with Q = N quanta, against 2^-(n+1) = exp(-n eps/k_B T)(1 - e^(-eps/k_B T)).
Brute-force enumeration (N = 3, 4) and the 1/N convergence are checked in
`scripts/check-physics.py` (`BoltzmannCountingPhysics`).

`animations/hard_sphere_relaxation.py` (`hard-sphere-relaxation`, 20 s, page 9):
600 elastic hard disks of radius 0.005 L in a box of side L, all at speed v_0
in random directions; speed histogram against the 2D Maxwellian at the same
energy (k_B T = m v_0^2/2); entropy -int F ln F d^2v from the histogram
(Miller-Madow corrected) against 1 + ln pi = 2.145. Checks
(`HardSphereRelaxationPhysics`): energy to 2e-16, late KS distance to the
Maxwellian at most 0.057 per 600-disk frame, late entropy 2.139 +- 0.006.
