# coulomb-encounter-offaxis (kin6d Q1 two-electron encounter)

Two equal-mass electrons, bare Coulomb repulsion, relative coordinate
r = x₁ − x₂, partial-wave FEM-DVR propagation; η = 3, σ = 3ƛ = r₀/2, kb = 2, z₀ = 20ƛ, ƛ = 1/k.
`log10_density` (z, x, panel, frame): 120 × 120 grid on [−34, 34]ƛ, 132
frames, panels 1 classical Wigner ensemble (8 × 10⁵ pairs, spin-unresolved,
slab |y| < ƛ/2), 2 spin-unresolved product (distinguishable), 3 singlet,
4 triplet; y = 0 slice of the sector-normalized density times ƛ³, log10 as
8-bit codes over a four-decade range. `t`: physical time t v/z₀ per frame
(slow motion up to 4× around closest approach, `slow_motion`). The
finite-space state bound, radial unknowns and l_max are in the parameters.
Visualization path: no pointwise bound; the classical histogram carries
counting noise (one count ≈ 2 × 10⁻⁶ ƛ⁻³). Scene:
`animations/coulomb_encounter.py`.

Format: raw little-endian arrays in Fortran (column-major) order; dtype,
shape, units and, for quantized arrays, the decode rule are in
`provenance.json` (schema `kin6d-animation-export-v1`), together with the
kin6d commit, command line, literal and resolved namelist and the declared
parameters. `animations/kin6d_data.py` reads them. kin6d is the scientific
source; the Manim scene only draws these arrays. Regenerate with the command
recorded in `provenance.json` (run from a scratch directory: the demo also
writes its own `output/`); equal inputs give byte-identical files.
