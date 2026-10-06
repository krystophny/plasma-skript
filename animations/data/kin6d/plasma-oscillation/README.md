# plasma-oscillation (kin6d slab oscillation)

Cold planar electron slab with fixed ions, q = ξ/ξ₀, τ = ω_pe t:
q'' = −q, q(0) = 1, q'(0) = 0, two plasma periods, 193 frames. Candidate:
FortNum Cash–Karp RK5(4), 128 fixed steps. `q_lower`/`q_upper`: connected
certified band (continuous Hermite/Bernstein residual radius, certified-
continuous, plus the candidate chord margin). `q_analytical` = cos τ is the
independent oracle. `edges`: x/a of the left/right slab edges and their
enclosures at the display ratio ξ₀/a = 0.1; `field_force`: E/E₀, F/F₀.
Scene: `animations/plasma_oscillation.py`.

Format: raw little-endian arrays in Fortran (column-major) order; dtype,
shape, units and, for quantized arrays, the decode rule are in
`provenance.json` (schema `kin6d-animation-export-v1`), together with the
kin6d commit, command line, literal and resolved namelist and the declared
parameters. `animations/kin6d_data.py` reads them. kin6d is the scientific
source; the Manim scene only draws these arrays. Regenerate with the command
recorded in `provenance.json` (run from a scratch directory: the demo also
writes its own `output/`); equal inputs give byte-identical files.
