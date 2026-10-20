# coupling-regions (kin6d C4, periodic OCP, no impurity, two temperatures)

Two classical electron one-component plasma runs with the same density and
different temperature, for `animations/coupling_regions.py`. Both: periodic
cube of edge 18 a (a = n₀^(-1/3)), N = 5832 electrons, uniform neutralizing
background, bare Coulomb (PME), no impurity and no test charge (κ = 0),
5/ω_p thermostat equilibration (then off), 12/ω_p Hamiltonian sampling at
0.1/ω_p (120 frames), 2 members (the scene uses member 1).

| run | T_e | Λ = nλ_D³ | λ_D | Γ_e = a²/(4πλ_D²) | box | dt |
|---|---|---|---|---|---|---|
| `strong/` | T₀ | 1 | a | 0.080 | 18 λ_D | 0.050/ω_p |
| `weak/` | 9 T₀ | 27 | 3a | 0.0088 | 6 λ_D | 0.0167/ω_p |

kin6d works in λ_D, so the temperature enters through Λ = (λ_D/a)³ at fixed
n₀; ω_p is the same in both runs. Run gates (kin6d output, statistical, not
certificates): S(2π/L) = 0.19 ± 0.10 against the Debye–Hückel 0.11 (strong),
0.52 ± 0.28 against 0.52 (weak); maximum energy defect per particle
0.016 k_BT (strong) and 0.0012 k_BT (weak). `scripts/check-physics.py` checks the kinetic temperature of the
exported positions and the variance of the smoothed charge density against
the Debye–Hückel structure factor.

Each directory holds the export of `ocp_shielding_demo --config config.nml
--export DIR` (kin6d branch `ocp-fluctuation-export`, commit 6686890; the
demo names the export `thermal-charge-fluctuations` for κ = 0, renamed
here), with `provenance.json` (schema `kin6d-animation-export-v1`: commit,
command line, literal and resolved namelist, parameters, decode rules). The
scene reads `positions` and `t`; `dn_*` and `r` are not used.
