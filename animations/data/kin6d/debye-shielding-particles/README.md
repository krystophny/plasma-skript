# debye-shielding-particles (kin6d C4, periodic OCP)

Classical electron one-component plasma, periodic cube L = 4 λ_D, uniform
neutralizing background, bare Coulomb (PME), Λ = nλ_D³ = 100 (N = 6400),
fixed repulsive point charge Q = −κ 4πΛ e at the origin (κ = 0.05,
nonlinear radius κλ_D), 5/ω_p thermostat equilibration (then off), 40/ω_p
Hamiltonian sampling at 0.2/ω_p (200 frames), 8 independent members.
`positions`: all electrons of member 1, 16-bit over [−L/2, L/2] (minimum
image around Q). `dn_running`: δn/n in 20 shells, ensemble mean of the time
average up to each frame; `dn_interval`: final mean and 95 % Student-t
interval over members (statistical, not a certificate). References per unit
κ, bin-averaged: `periodic` (linear response with the periodic
screened-Poisson Green function), `yukawa` (isolated −e^{−r}/r), `bare`
(unscreened −1/r). Config: kin6d `benchmarks/ocp/shielding-animation.nml`.
Scene: `animations/debye_shielding_particles.py`.

Format: raw little-endian arrays in Fortran (column-major) order; dtype,
shape, units and, for quantized arrays, the decode rule are in
`provenance.json` (schema `kin6d-animation-export-v1`), together with the
kin6d commit, command line, literal and resolved namelist and the declared
parameters. `animations/kin6d_data.py` reads them. kin6d is the scientific
source; the Manim scene only draws these arrays. Regenerate with the command
recorded in `provenance.json` (run from a scratch directory: the demo also
writes its own `output/`); equal inputs give byte-identical files.
