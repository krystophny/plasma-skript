# Saha comparison: Alcator C-Mod detached divertor

## What the plotted measurements are

The main panel uses deuterium Balmer-level populations measured in a detached, recombining Alcator C-Mod divertor. Lumma, Terry, and Lipschultz fit the Balmer-line brightnesses and converted them to excited-state populations N⁰ₙ; Fig. 7b uses an emitting-layer thickness ΔL = 0.033 m, obtained from their continuum analysis. The plotted measurements are the seven symbols actually present in that panel: n = 3 and n = 5 through 10. There is no n = 4 measurement in the panel.

The Saha inputs came from different diagnostics in the same analysis. The electron temperature was inferred from the shape of the recombination continuum; their best fit for panel 7b is kBTₑ = 1.2 eV. Their continuum and Balmer analysis together allows roughly 0.8–1.5 eV, and the paper estimates a maximum continuum-temperature inaccuracy of about ±0.5 eV. Electron density was obtained from Stark broadening of the Balmer lines, nₑ = 8.8 × 10²⁰ m⁻³, with about ±20% uncertainty. For the Saha calculation we assume a quasineutral, singly ionized deuterium plasma, so nᵢ = nₑ; the ion density was not an independent measurement.

The level populations are spectroscopic inferences, not direct atom counts. They scale as line brightness divided by ΔL and by the transition energy and spontaneous-emission coefficient. The temperature and density inputs are independently inferred from continuum shape and Stark width, respectively, while the population trend comes from Balmer line brightnesses. The shared line-of-sight volume model means this is a partially independent spectroscopic test, not three unrelated instruments sampling an identical point.

## Digitization and uncertainty

The selected data were digitized from panel (b) of Fig. 7 in the MIT-hosted author manuscript (internal page 39; the source manuscript is available at the MIT handle cited below). The source page image is 2720 × 4480 pixels at 320 dpi. The x-axis is linear in n; the population axis is logarithmic. The calibration uses x(n=2)=617 px, x(n=12)=2244 px, y(10¹⁶ m⁻³)=1415 px, and y(10¹⁵ m⁻³)=1657 px; I read the centers of the open diamonds. data.csv retains digitized x/y-pixel positions, axis calibration pixels, source figure, measurement conditions, and uncertainty fields.

The paper's Fig. 7 has no population error bars, and the text does not give a numerical uncertainty for each plotted population. I have not invented one. The blue bars in our plot are only a conservative ±0.04 dex digitization uncertainty (about 9–10% in population), reflecting finite marker/axis reading precision in the scanned graph. They are not experimental confidence intervals. The source-reported ±20% Stark-density uncertainty and the 0.8–1.5 eV joint temperature range instead appear as the orange Saha-input band; because nᵢ = nₑ, the predicted population scales as nₑ².

## Saha calculation and independent check

plot_saha_cmod.py computes the resolved-level ideal Saha–Boltzmann population

N⁰ₙ = nₑ nᵢ [gₙ/(2gᵢ)] (h²/(2πmₑ kBTₑ))^(3/2) exp(χₙ/(kBTₑ)), with χₙ = 13.6 eV/n².

For deuterium's excited hydrogenic level, the calculation uses gₙ = 2n² (electron spin and orbital degeneracy) and gᵢ = 1, so gₙ/(2gᵢ) = n². Deuterium's nuclear-spin multiplicity cancels between atom and ion. This is the level-resolved form of the lecture's Saha relation; for the lecture's ground-state convention gᵢ = gₙ = 1, the explicit factor 2 remains in nᵢnₑ/nₙ = 2(2πmₑkBTₑ/h²)^(3/2) exp(−χ/kBTₑ). The calculation assumes a Maxwellian electron distribution and partial LTE for the high excited levels. It uses exact SI constants and no ionization-potential-depression or Debye-lowering correction.

The script includes an independent half-ionization check. For total hydrogen-nuclei density nH = 10²⁰ m⁻³, it solves nₑ = nᵢ = n₀ = nH/2 with the lecture's ground-state statistical-weight convention and obtains 8684 K. Richardson's 2019 NRL Plasma Formulary, Eq. (17), gives the approximate coefficient 6.0 × 10²¹ Tₑ^(3/2) exp(−13.6/Tₑ) cm⁻³ for Tₑ in eV; solving that form gives 8687 K, a 0.03% difference. This checks the constants, units, and root solve independently of the plotted excited-state calculation.

## Agreement and interpretation

At the paper's central kBTₑ = 1.2 eV and nₑ = nᵢ = 8.8 × 10²⁰ m⁻³, the digitized n = 5–10 measurements are 1.01, 1.11, 1.25, 1.40, 1.47, and 1.30 times the ideal Saha–Boltzmann values. Thus the central curve is within 0–47% of these six measured populations (median ratio 1.28); the source-reported density and temperature uncertainties make this an order-unity agreement, not a precision test at the 10% level. The article separately states that its recombination-only collisional-radiative prediction is within 10% of Saha–Boltzmann for n > 3; that is a model-to-model comparison, not a claim that every measured population lies within 10% of our central Saha curve.

The n = 3 point comes from the spatially averaged Dα diode-array brightness, while the higher Balmer lines come from the spectrometer. The authors flag this level separately: their recombination-only prediction is about 25–30% below the measured n = 3 population and outside their estimated relative-intensity calibration error; they discuss excitation from ground-state neutrals and molecular recombination as possible contributors. It is shown as context, while the quantitative agreement statement above is restricted to n = 5–10.

This is a useful fusion example of high-level partial LTE in a dense, detached divertor. It does not establish Saha balance of ground-state neutrals, or LTE for the whole divertor. The analysis assumes a uniform, isothermal emitting volume of thickness ΔL; neutral density and ion density are not independently measured, and transport can compete with local recombination. High-n states lie near the continuum and can be affected by Stark dissolution and continuum lowering, neither of which is included in our ideal Saha curve. The plotted band shows the published Tₑ and nₑ constraints only; it does not represent every systematic uncertainty in the volume model or level-population inference.

The QUEST edge comparison has been dropped. A Saha mismatch there would mainly reflect recycled neutrals outside local equilibrium, not a clean test of the equation.

## Citation and reuse

Bibliographic metadata were verified against Crossref: D. Lumma, J. L. Terry, and B. Lipschultz, “Radiative and three-body recombination in the Alcator C-Mod divertor,” Physics of Plasmas 4(7), 2555–2566 (July 1997), https://doi.org/10.1063/1.872234. The article is available as an author manuscript from MIT's DSpace repository: http://hdl.handle.net/1721.1/95301. The bibliographic entry is retained in sources.bib.

The published article carries AIP copyright/reuse terms. AIP's permissions guidance covers republication of figures and tables; its author guide distinguishes raw-data use that does not duplicate the original figure or analysis. This slide uses digitized point values to make a new plot and copies no figure artwork: AIP permissions guidance, https://publishing.aip.org/resources/researchers/rights-and-permissions/permissions/; AIP author guide, https://publishing.aip.org/wp-content/uploads/2021/12/AIPP-Books_Author-Guide_December-2021.pdf.

## Student takeaway

In this dense, recombining tokamak divertor, the populations of excited deuterium atoms lie within about 50% of the Saha–Boltzmann prediction when Tₑ and nₑ are taken from continuum shape and Stark broadening. That supports the 10⁴ K rule of thumb as an order-of-magnitude guide: this case has kBTₑ = 1.2 eV (about 1.4 × 10⁴ K), where high-level populations are strongly thermalized, but the agreement applies to high-n levels and depends on density and local-equilibrium conditions rather than defining a universal hydrogen ionization temperature.
