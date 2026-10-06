# Temperature, entropy, and thermal ionization

LOOK deck; THINK derivations take place in the separate Goodnotes notebook.
No blank or titled writing pages. Stable script labels resolve through the outline.

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
| 8 | Drifting Maxwellian | static | thermal-boltzmann | Fixed total momentum sets mean flow. |
| 9 | Thermal particle slots | static | thermal-saha | Count translational and internal choices. |
| 10 | Adding and removing | static | thermal-saha | Factorials encode indistinguishability. |
| 11 | One ionization | static | thermal-saha | Three particle factors and one reservoir penalty. |
| 12 | Heavy particle cancellation | static | thermal-saha | Neutral and ion masses nearly coincide. |
| 13 | Saha composition balance | static | thermal-saha | New electron freedom is the large factor. |
| 14 | Ionization fraction | static | thermal-ionization | Nucleus conservation and neutrality. |
| 15 | Competing statistical factors | static | thermal-ionization | Equal factors give x=0.618; half needs A=0.5. |
| 16 | Thermal ionization threshold | static | thermal-ionization | Exact logarithm, computed table, qualified 10⁴ K. |
| 17 | Equilibrium validity | static | thermal-ionization | LTE versus coronal and rate balance. |
| 18 | Source credits | static | thermal-equilibrium | Sources and AI disclosure. |

## Scientific inputs

Lecturer notes, 2026-10-06, rendered pages 1–3; chosen dilute slot-counting route.
Thermal speed: v_th,s = sqrt(2 k_B T_s/m_s), as in intro-speed-energy-temperature.
Equations: thermal-ionization-ratio, thermal-saha-equation,
thermal-fraction-solution, thermal-half-temperature.
Oracle and figures: derivations/chapters/ch02_thermal_equilibrium.py.
The brief's rough 6,000–15,000 K range is replaced by the oracle's 3,226–26,230 K
over 10⁶–10²⁶ m⁻³. Exact half ionization requires ln(4/(n lambda_e³)).
