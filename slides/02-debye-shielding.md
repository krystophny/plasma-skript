# 02-debye-shielding — level 2

Live deck for script chapter 2 (`src/chapters/02-debye-shielding.typ`). Its
start (point charge, λ_D) closes lecture 1; the rest opens lecture 2 (course
`PLAN.md`, "Lecture Format"). One new idea: mobile electrons screen a charge
over λ_D, and the statistical picture needs many particles per Debye sphere.

Source `slides/02-debye-shielding.typ` (layout `slides/theme.typ`), built by
`scripts/build-slides.sh` to `public/slides/02-debye-shielding.pdf` (13 pages,
7 numbered). LIVE mode (iPad on blank pages). SI throughout, k_B T in eV on
plots. Page rules: see `01-introduction.md`. The script chapter has one
section (2.1 Debye shielding), so only page 2 carries a title; the finite
source and the plasma parameter follow without titles.

## Sequence (script order: point charge → finite source → N_D → map)

| p. | Section title (script) | Page | Content |
|---|---|---|---|
| 1 | — | title | Plasma Physics / Chapter 2 / Debye shielding / C. Albert / TU Graz WS 2026/27 / AI line |
| 2 | 2.1 Debye shielding | animation | `debye-shielding` poster, linked MP4 |
| — | | LIVE | two blank pages: Debye derivation, point charge |
| 3 | | summary | see below; plot `debye_potential` |
| 4 | | plot pair | `debye_potential` \| `debye_sphere_potential` (the script's comparison) |
| — | | LIVE | two blank pages: finite permeable source |
| 5 | | illustration | Debye spheres, N_D ≈ 3 vs 300 (`slides/theme.typ: debye-sphere`) |
| — | | LIVE | two blank pages: Debye number, coupling |
| 6 | | summary | see below; plot `debye_number` |
| 7 | | plot | `nt_map` with λ_D ≪ L, N_D ≫ 1 (ω_pe τ ≫ 1 follows in chapter 3) |

## Summary pages

- **Debye shielding (3).** Assumptions: immobile ions n_i = n₀; Boltzmann
  electrons n_e = n₀ exp(eφ/k_BT_e); weak potential e|φ| ≪ k_BT_e; point
  charge Q, φ → Q/(4πε₀r) for r → 0. Derivation: Poisson ∇²φ = −ρ_q/ε₀ →
  charge density ρ_q = e(n_i − n_e) → linearize ρ_q ≈ −(e²n₀/k_BT_e)φ →
  substitute ∇²φ = φ/λ_D² → φ = w/r: w'' = w/λ_D² → decay w ∝ e^{−r/λ_D}.
  Result: φ = Q e^{−r/λ_D}/(4πε₀r), λ_D = √(ε₀k_BT_e/(n₀e²)). Sources:
  script 02:81–158, `ch02_debye_shielding.py` "Debye length", "Screened point
  charge".
- **Plasma parameter (6).** Assumptions: uniform density n_e = n₀; Debye
  sphere r ≤ λ_D; mean spacing a, (4π/3)a³n₀ = 1. Derivation: count
  N_D = ∫₀^{λ_D} 4πr²n₀ dr → integrate N_D = (4π/3)n₀λ_D³; coupling
  Γ = e²/(4πε₀ a k_BT_e) → insert a, λ_D: Γ N_D^{2/3} = 1/3. Result:
  N_D ≫ 1 ⇔ Γ ≪ 1. Source: `ch02_debye_shielding.py` "Debye number and
  coupling".

## LIVE routes (lecturer cues)

- **Debye, point charge (after p. 2).** Test charge Q in quasi-neutral n₀ →
  Boltzmann electrons n_e = n₀ exp(eΦ/k_BT_e), ions frozen (m_i → ∞) →
  ρ = e(n_i − n_e) → linearize e|Φ| ≪ k_BT_e → Poisson ∇²Φ = Φ/λ_D² + point
  source → Φ = Q e^{−r/λ_D}/(4πε₀r) → λ_D = √(ε₀k_BT_e/(ne²)). Numbers:
  corona, tokamak. Condition 1: λ_D ≪ L.
- **Finite source (after p. 4).** Uniform permeable sphere, R = λ_D/2 (the
  source in the animation) → bare potential by Gauss: Q(3 − r²/R²)/(8πε₀R)
  inside, Coulomb outside → geometry removes the singularity, screening is a
  separate effect → Debye–Hückel with source inside, homogeneous outside,
  match at R → same e^{−r/λ_D} tail outside. Small-source condition
  3eQ/(8πε₀Rk_BT_e) ≪ 1.
- **Debye number (after p. 5).** Boltzmann ansatz is statistical → needs
  many particles in a Debye sphere → N_D = (4π/3)nλ_D³ ∝ T^{3/2}/n^{1/2} →
  mean spacing a = (3/(4πn))^{1/3} → Γ = potential/kinetic energy
  = a²/(3λ_D²) = N_D^{−2/3}/3 → weak coupling ⇔ N_D ≫ 1. Condition 2.
- **Map (7)** is discussed, not derived: place the five example plasmas.

## Figures

| File | Source | Note |
|---|---|---|
| `debye_potential` | `derivations/chapters/ch02_debye_shielding.py` | bare vs screened point charge (left panel of the script pair) |
| `debye_sphere_potential` | same | bare vs screened uniform sphere, R = λ_D/2 (right panel) |
| `debye_number` | same | N_D(n_e) for 0.1 eV, 10 eV, 10 keV |
| `nt_map` | same | λ_D = L for 1 µm, 1 cm, 100 m; N_D = 1; five example plasmas (script `debye-regime-map`) |
| Debye spheres | `slides/theme.typ: debye-sphere` | illustration in Typst: uniform random points (fixed seed), 2-D projection |
| poster `debye-shielding` | `animations/debye_shielding.py` | copied from the current render by `build-slides.sh` |

Example-plasma parameter sources: `01-introduction.md`.
