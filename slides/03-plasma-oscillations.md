# 03-plasma-oscillations — level 2

Live deck for script chapter 3 (`src/chapters/03-plasma-oscillations.typ`).
One new idea: electron inertia plus charge separation give an oscillation at
ω_pe, the fastest collective time scale.

Source `slides/03-plasma-oscillations.typ` (layout `slides/theme.typ`), built
by `scripts/build-slides.sh` to `public/slides/03-plasma-oscillations.pdf`
(5 pages, 3 numbered). LIVE mode (iPad on blank pages). SI throughout. Page
rules: see `01-introduction.md`.

## Sequence (script order: cold slab → ω_pe → collisions as damping caveat)

| p. | Section title (script) | Page | Content |
|---|---|---|---|
| 1 | — | title | Plasma Physics / Chapter 3 / Plasma oscillations / C. Albert / TU Graz WS 2026/27 / AI line |
| 2 | 3.1 Electron plasma oscillations | animation | `plasma-oscillation` poster, linked MP4 |
| — | | LIVE | two blank pages: plasma oscillation |
| 3 | | summary | see below; plot `plasma_frequency` |

## Summary page

- **Electron plasma oscillations (3).** Assumptions: immobile ions n_i = n₀;
  cold electrons k_BT_e → 0; small displacement |ξ| ≪ L; no collisions, no
  field: ω_pe τ ≫ 1. Derivation: sheet charge σ = e n₀ ξ → Gauss
  E = e n₀ ξ/ε₀ → Newton m_e ξ̈ = −eE = −(n₀e²/ε₀)ξ → divide by m_e:
  ξ̈ + ω_pe² ξ = 0 → solve ξ = ξ₀ cos(ω_pe t + δ). Result:
  ω_pe = √(n₀e²/(ε₀m_e)); below it f_pe = ω_pe/2π ≈ 8.98 √(n₀/m⁻³) Hz.
  Sources: script §3.1 Electron plasma oscillations, `ch03_plasma_oscillations.py` "Charge-separation
  field", "Electron plasma oscillation". ω_pe τ ≫ 1 is not a script
  equation; it is the collisionless condition of the LIVE route below.

## LIVE route (lecturer cues)

- **Plasma oscillation (after p. 2).** Displace electron slab by ξ, ions
  fixed → surface charge, E = neξ/ε₀ → m_e ξ̈ = −(ne²/ε₀)ξ → ω_pe → numeric
  f_pe ≈ 8.98 √n Hz (ionosphere: MHz, radio reflection). Collisions with
  neutrals at rate 1/τ damp it → condition 3: ω_pe τ ≫ 1. Close with the
  three conditions on the chapter-2 regime map if time allows.

## Figures

| File | Source | Note |
|---|---|---|
| `plasma_frequency` | `derivations/chapters/ch03_plasma_oscillations.py` | f_pe(n_e) with the five example plasmas (script `plasma-frequency-scale`) |
| poster `plasma-oscillation` | `animations/plasma_oscillation.py` | copied from the current render by `build-slides.sh` |

Example-plasma parameter sources: `01-introduction.md`.
