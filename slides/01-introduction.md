# 01-introduction — level 2

Live deck for script chapter 1 (`src/chapters/01-introduction.typ`). Taught in
lecture 1 together with the start of chapter 2 (course `PLAN.md`, "Lecture
Format"). One new idea: a plasma is identified by its collective response, and
the model must match the scales of the observation.

Source `slides/01-introduction.typ` (layout `slides/theme.typ`), built by
`scripts/build-slides.sh` to `public/slides/01-introduction.pdf` (23 pages, 16
numbered; blank writing pages carry no number and do not count). Photo story
+ LIVE mode (iPad on blank pages). SI throughout, k_B T in eV on plots.

Page rules (all decks): the script's section title, with its number, on the
first page of each script section only; no other titles. Summary pages:
Assumptions (formulas with short plain labels), Derivation (chain of the key
equations, one- or two-word step labels), Result (thin-ruled box) above its
plot. Every symbol is named in words at its first use in the deck (muted
line). No prose sentences.

## Sequence

| p. | Section title (script) | Page | Content |
|---|---|---|---|
| 1 | — | title | Plasma Physics / Chapter 1 / Introduction / C. Albert / TU Graz WS 2026/27 / AI line |
| 2–5 | 1.1 Plasma as a collective state (p. 2) | photo story | flare (SDO), aurora (ISS), Carina H II region (ESO), Hall thruster (JPL) |
| 6 | | animation | `collective-response` poster, linked MP4: neutral gas vs plasma |
| — | | LIVE | two blank pages |
| 7 | | summary | quasineutrality; plot `enclosed_charge` |
| 8 | | plot | empty n–T plane `nt_plane` |
| — | | LIVE | two blank pages: place the four photos on the plane |
| 9 | 1.2 Speed, energy, and temperature | plot pair | `maxwellian_heating` \| `maxwellian_drift` |
| — | | LIVE | two blank pages |
| 10 | | summary | thermal speed; plot `maxwell_speed` |
| 11 | | plot | `thermal_speed` (eV and K axes); k_BT = 1 eV ↔ T ≈ 1.16·10⁴ K |
| 12 | 1.3 Characteristic scales and ordering | titled writing page | LIVE starts here |
| — | | LIVE | one blank page |
| 13 | | summary | scale ordering over the full-width plot `scale_ordering` |
| 14 | 1.4 From microscopic particles to a model | animation | `particles-to-moments` poster, linked MP4: particles → f(x,v) → n(x), u(x) |
| 15 | | model ladder | N particles →⟨·⟩→ f(x,v,t) →∫v^k f d³v→ moments → fluids →Σ_s→ magnetohydrodynamics |
| 16 | — | credits | photo credits with the page numbers of the photos |

## Summary pages

- **Quasineutrality (7).** Assumptions: species s, ρ_q = Σ_s q_s n_s;
  electrons, ions q_e = −e, q_i = Z_i e; screened charge Q,
  φ = Q e^{−r/λ_D}/(4πε₀r). Derivation: insert charges
  ρ_q = e(Σ_i Z_i n_i − n_e) → Gauss Q_enc = −4πε₀r² dφ/dr =
  Q(1 + r/λ_D)e^{−r/λ_D} → r ≫ λ_D: Q_enc → 0, ρ_q ≈ 0. Result:
  n_e ≈ Σ_i Z_i n_i, quasineutrality. Sources: script 01:60–98,
  `ch01_introduction.py` "Charge density and quasineutrality", "Net charge
  around a screened point charge".
- **Thermal speed (10).** Assumptions: ε_kin,s = m_s v²/2; ε_th,s = k_BT_s;
  Maxwellian with drift u_s, f ∝ exp(−(v_x−u_s)²/v_th²); T_e ≠ T_i.
  Derivation: convention m_s v_th²/2 = k_BT_s → variance
  ⟨(v_x−u_s)²⟩ = k_BT_s/m_s → speeds v_peak = v_th, ⟨v⟩ = 2v_th/√π,
  v_rms = √(3/2) v_th. Result: v_th,s = √(2k_BT_s/m_s). Sources: script
  01:211–260, `ch01_introduction.py` "Thermal speed", "Heating versus
  acceleration", "Speeds of a Maxwellian".
- **Scale ordering (13).** Three blocks above the full-width plot.
  Assumptions: n_e, k_BT_e, B, L. Derivation (definitions used for the plot):
  λ_D, ω_pe, ω_ce = eB/m_e, ρ_e = v_th,e/ω_ce, λ_mfp = ⟨v⟩/ν_ei. Result:
  ℓ ≪ L average, ℓ ≳ L resolve (script 01:296–345 summary). Source:
  `ch01_introduction.py` "Characteristic scales of five example plasmas".

## LIVE routes (lecturer cues)

- **n–T plane (8).** Photos → rough n, T per object (orders of magnitude) →
  "ionized gas" is not enough: what makes it collective? → open question
  answered in chapters 2 and 3. Ionization: Saha only as a remark.
- **Collective response (6–7).** Play the animation: left, a few sharp
  contact collisions; right, every electron within ~λ_D feels the charge →
  charge density ρ_q = Σ q_s n_s → bulk quasineutrality; λ_D itself is
  chapter 2 (the summary plot only previews the screened net charge).
- **Maxwellian pair (9–10).** Heating widens f, a drift shifts it: k_B T_s
  is the width, not the mean energy of the flow → v_th convention with the
  factor 2 → T_e ≠ T_i allowed. Page 11 converts eV ↔ K and compares
  electron and proton thermal speeds (√(m_p/m_e) ≈ 43).
- **Scales (12).** Name the four responses (screening, oscillation,
  gyromotion, collisions), compare each with size and duration of the
  observation; page 13 shows that one small scale does not justify every
  simplification.
- **Particles → moments (14)** and **ladder (15)** are discussed, not
  derived. Preview chapters 4–8.

## Figures

| File | Source | Note |
|---|---|---|
| `nt_plane` | `derivations/chapters/ch02_debye_shielding.py` | empty axes of `nt_map`: n_e 10⁶–10³² m⁻³, k_BT_e 10⁻²–10⁵ eV |
| `enclosed_charge`, `maxwellian_heating`, `maxwellian_drift`, `maxwell_speed`, `thermal_speed`, `scale_ordering` | `derivations/chapters/ch01_introduction.py` | the script's figures; B and L of `scale_ordering` are sourced in `FIELD_AND_SIZE` |
| posters `collective-response`, `particles-to-moments` | `animations/collective_response.py`, `particles_to_moments.py` | copied from the current render by `build-slides.sh` |
| model ladder | `slides/theme.typ: model-ladder` | Fletcher; the script's `model-hierarchy` figure is a different, web-sized diagram |
| `slides/photos/*.jpg` | see `slides/photos/credits.md` | public domain or CC BY 4.0 |

Derived plots are the script's figures, one source for both: the
`plot_<name>` code in `derivations/chapters/chNN_*.py` writes
`derivations/build/fig/<name>.svg` (`make -C derivations fig`). Their widths
are whole slide-grid columns (`si.slide_width`), so the 10 pt figure text
becomes the 18 pt slide body at the slide scale 1.8.

## Parameter sources (order of magnitude, `derivations/si.py: EXAMPLE_PLASMAS`)

| Plasma | n [m⁻³] | k_BT_e [eV] | Source (verified 2026-10-02) |
|---|---|---|---|
| solar corona | 1e15 | 100 | NRL Plasma Formulary (J. D. Huba, NRL, 2019 ed.), "Approximate magnitudes in some typical plasmas", p. 40: Solar Corona n = 1e9 cm⁻³, T = 1e2 eV. https://library.psfc.mit.edu/catalog/online_pubs/NRL_FORMULARY_19.pdf |
| H II region (gaseous nebula) | 1e9 | 1 | Same NRL table, p. 40: Gaseous nebula n = 1e3 cm⁻³, T = 1 eV. Orion's bright Huygens region is somewhat denser, n_e ≈ 2e9–9e9 m⁻³ at T_e ≈ 9400–9800 K ≈ 0.8 eV (O'Dell, Ferland & Peimbert, ApJ 2017, https://arxiv.org/abs/1610.06595) |
| ionosphere F layer | 1e12 | 0.1 | Daytime F2 peak n_e ≈ 1e12 m⁻³ (f_oF2 ≈ 9 MHz): Kelley, *The Earth's Ionosphere*, 2nd ed. (Academic Press, 2009), ch. 1. F-region T_e ≈ 1000–3000 K = 0.09–0.26 eV: Schunk & Nagy, Rev. Geophys. 16, 355 (1978), https://doi.org/10.1029/RG016i003p00355 |
| Hall thruster channel | 1e18 | 20 | Goebel & Katz, *Fundamentals of Electric Propulsion: Ion and Hall Thrusters* (JPL/Wiley, 2008), SPT-100: T_e ≈ 25 eV in the channel (Sec. 7.3.4, p. 359), peak n_e ≈ 8e17 m⁻³ (Fig. 7-15, p. 374). https://descanso.jpl.nasa.gov/SciTechBook/series1/Goebel__cmprsd_opt.pdf |
| tokamak core (ITER-like) | 1e20 | 1e4 | ITER Q = 10 reference: ⟨n_e⟩ = 1.01e20 m⁻³, ⟨T_e⟩ = 8.8 keV (volume averages; the central T_e is roughly twice that). D. J. Campbell, "The physics of ITER-FEAT", APS-DPP 2000, slide "Device Parameters", https://fire.pppl.gov/ITER_FEAT__Campb_APS.pdf; background: ITER Physics Basis, Nucl. Fusion 39, 2137 (1999) |

All five points agree with these sources to within a factor of about 2. The
same five points appear in `nt_map` (chapter 2) and `plasma_frequency`
(chapter 3).
