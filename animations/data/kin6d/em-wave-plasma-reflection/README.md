# em-wave-plasma-reflection (kin6d em_slab_demo)

Plane electromagnetic wave at normal incidence on a cold electron plasma with
a sharp edge at x = 0, uniform density n0 for x > 0, fixed neutralizing ions.
Relativistic Vlasov–Maxwell in one dimension: E_x, E_y, B_z on a staggered
Yee grid (Δx = 0.04 c/ω_pe, cΔt = 0.95 Δx), first-order Mur boundaries,
soft sheet-current source at x = −18 c/ω_pe with a sin² rise over 25/ω_pe;
cold electron macroparticle sheets (8 per cell, CIC, relativistic Boris,
charge-conserving J_x). Incident amplitude E0 = 0.005 m c ω_pe/e for both
runs, so a0 = eE0/(m ω c) = 0.01 (low) and 0.0025 (high). The plasma reaches
x = 135 c/ω_pe, beyond any signal during the run (effectively semi-infinite).

Runs on the same plasma: `low` ω = 0.5 ω_pe (total reflection, evanescent
field), `high` ω = 2 ω_pe (Fresnel transmission). Arrays: `x` display grid
(x − x_edge, [−15, 10] c/ω_pe), `t_<run>` frame times (1/ω_pe), `ey_<run>`
E_y/E0 per frame, `x0` initial positions of 50 sample electron sheets in
[0, 4] c/ω_pe, `y_<run>` their transverse displacement and `xdisp_<run>` their
longitudinal displacement (c/ω_pe), `envelope_<run>` the steady linear-theory
|E_y|/E0 and `lockin_<run>` the measured steady |E_y|/E0 from the lock-in
window. Measured vs linear theory (declared parameters): |R| = 0.99959 vs 1,
arg R = −2.09484 vs −2.09440 rad, skin depth 1.15480 vs 1.15470 c/ω_pe (low);
R = 0.07213 vs 0.07180, T = 1.07237 vs 1.07180, wavelength 3.62760 vs
3.62760 c/ω_pe (high); energy-balance residual −4e−5 (low), −8e−4 (high).
Status: candidate PIC dynamics checked by the kin6d CTests `em_slab_*`, not
certificates. At ω = ω_pe/2 the second-harmonic v×B force resonantly drives
a small longitudinal Langmuir motion near the surface (`xdisp_low`, O(a0²));
the scene shows the transverse motion only. Derivation and verification:
kin6d `docs/em-slab-reflection.md`. Scene: `animations/em_wave_plasma.py`.

Format: raw little-endian arrays in Fortran (column-major) order; dtype,
shape, units are in `provenance.json` (schema `kin6d-animation-export-v1`),
together with the kin6d commit, command line, resolved namelist and the
declared parameters. `animations/kin6d_data.py` reads them. kin6d is the
scientific source; the Manim scene only draws these arrays. Regenerate with
the command recorded in `provenance.json` (all defaults, run from a scratch
directory with `OMP_NUM_THREADS=4`; the demo also writes its own `output/`);
equal inputs and thread count give byte-identical files.
