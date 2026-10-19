# thermal-charge-fluctuations (kin6d C4, periodic OCP, no impurity)

Classical electron one-component plasma, periodic cube L = 6 λ_D, uniform
neutralizing background, bare Coulomb (PME), Λ = nλ_D³ = 30 (N = 6480), no
impurity and no test charge (κ = 0): thermal charge-density fluctuations
only. 5/ω_p thermostat equilibration (then off), 40/ω_p Hamiltonian
sampling at 0.2/ω_p (200 frames), 2 members (the scene uses member 1).
`positions`: all electrons of member 1, 16-bit over [−L/2, L/2] (minimum
image around the origin). `dn_running`, `dn_interval`: δn/n in 20 shells
around the arbitrary origin (reference 0; not used by the scene). The run
also reports S(2π/L) = 0.57 ± 0.72 (95 %, 2 members) against the
Debye–Hückel 0.523; statistical, not a certificate. Config: kin6d
`benchmarks/ocp/fluctuation-animation.nml` (kin6d branch
`ocp-fluctuation-export`, commit 6686890). Scene:
`animations/thermal_charge_fluctuations.py`, which smooths these positions
with a Gaussian of width 0.4 λ_D into ρ/(e n₀); `scripts/check-physics.py`
checks its variance against the Debye–Hückel structure factor.

Format: raw little-endian arrays in Fortran (column-major) order; dtype,
shape, units and, for quantized arrays, the decode rule are in
`provenance.json` (schema `kin6d-animation-export-v1`), together with the
kin6d commit, command line, literal and resolved namelist and the declared
parameters. `animations/kin6d_data.py` reads them. kin6d is the scientific
source; the Manim scene only draws these arrays. Regenerate with
`ocp_shielding_demo --config benchmarks/ocp/fluctuation-animation.nml
--export DIR` (run from a scratch directory: the demo also writes its own
`output/`); two runs gave byte-identical arrays (only the recorded export
path in `provenance.json` differed).
