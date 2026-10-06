# kin6d media — cues for decks without a plan yet

Data-driven animations whose scientific source is kin6d (data and provenance
in `animations/data/kin6d/<slug>/`). Cues for chapters that already have a
deck live in their `<stem>.md` (`02-debye-shielding.md`,
`03-plasma-oscillations.md`). This note holds the cue for chapter 9 until
`09-collisions-conductivity.md` exists; move it there then.

## Chapter 9 — collisions and conductivity

Section: script §9.3 "Fully ionized plasmas: Coulomb collisions"
(`coulomb-collisions`), at the lower cutoff of the Coulomb logarithm
(`ln(lambda_D/b_90) = ln Lambda_cut`, "strong deflection or a quantum
correction").

| Slug | Scene | Content |
|---|---|---|
| `coulomb-encounter-headon` | `animations/coulomb_encounter.py: CoulombEncounterHeadOn` | η = 3, σ = r₀/2, b = 0 |
| `coulomb-encounter-offaxis` | `CoulombEncounterOffAxis` | η = 3, σ = r₀/2, kb = 2 |
| `coulomb-encounter-hot` | `CoulombEncounterHot` | η = 0.03 (10 keV electrons), σ = 4ƛ, b = 0 |

All three: 2 × 2 grid of one encounter (same axes kx, kz [1], clock and
log colour scale): classical Wigner ensemble | distinguishable (spin-
unresolved product); singlet | triplet. Looping, full-slide dark
animation pages before the derivation.

Route cue: η = 3 (cold electrons ~1 eV or ions) vs η = 0.03 (10 keV
electrons): trajectory picture valid vs diffraction; statistics stay
Rutherford, cutoff b₉₀ → ƛ (ln Λ 20.1 → 17.1 at n = 10²⁰ m⁻³).

Suggested order: headon (exchange fringes, classical hole r < r₀) →
offaxis (same, with impact parameter) → hot (r₀ ≪ ƛ: almost undeflected
packet and a faint diffracted wave; the classical ensemble keeps rare
large deflections) → LIVE derivation of b_min = max(b₉₀, ƛ).
