#import "theme.typ": *
#import "chapters/01-introduction.typ": chapter as introduction
#import "chapters/02-thermal-equilibrium.typ": chapter as thermal-equilibrium
#import "chapters/03-debye-shielding.typ": chapter as debye-shielding
#import "chapters/04-plasma-oscillations.typ": chapter as plasma-oscillations
#import "chapters/05-single-particle-motion.typ": chapter as motion
#import "chapters/06-kinetic-theory.typ": chapter as kinetic
#import "chapters/07-moments.typ": chapter as moments
#import "chapters/08-multiple-fluids.typ": chapter as multiple-fluids
#import "chapters/09-mhd.typ": chapter as mhd
#import "chapters/10-collisions-conductivity.typ": chapter as collisions
#import "chapters/11-diffusion.typ": chapter as diffusion
#import "chapters/12-introduction-waves.typ": chapter as introduction-waves
#import "chapters/13-cold-magnetized-waves.typ": chapter as cold-waves
#import "chapters/14-finite-temperature-waves.typ": chapter as finite-temperature-waves
#import "chapters/15-hot-plasma-waves.typ": chapter as hot-waves
#import "chapters/16-sheaths-probes.typ": chapter as sheaths
#import "appendices/mathematical-toolkit.typ": appendix as mathematical-toolkit
#import "appendices/cgs-translation.typ": appendix as cgs-translation

#show: frame-style(styles.boxy)

#set page(paper: "a4", margin: 2.2cm)
#set par(justify: true)
// Text in STIX Two Text and maths in STIX Two Math, as in the lecture slides,
// the plots and the animations (fonts/, SIL OFL; compile with --font-path
// fonts).
#set text(font: "STIX Two Text", size: 11pt)
#show math.equation: set text(font: "STIX Two Math")
// Inline maths: Typst sizes a line by the text edges (cap height to
// baseline), so inline fractions overlapped the neighbouring lines. Tall
// inline equations (fractions, stacked scripts) take their glyph bounds as
// edges, so only their lines grow; equations still break across lines.
#show math.equation.where(block: false): it => context {
  let bounds(body) = {
    set text(top-edge: "bounds", bottom-edge: "bounds")
    body
  }
  if measure(bounds(it)).height > 1.3 * text.size { bounds(it) } else { it }
}

#align(center)[
  #text(size: 24pt, weight: "bold")[Plasma Physics]
  #v(0.5em)
  #text(fill: muted)[Christopher Albert, TU Graz]
  #v(0.5em)
  #text(size: 9pt, fill: muted)[SI units throughout, with $epsilon_0$ and $mu_0$; CGS forms are collected in the appendix.]
]

#v(1.5em)
#introduction
#pagebreak()
#thermal-equilibrium
#pagebreak()
#debye-shielding
#pagebreak()
#plasma-oscillations
#pagebreak()
#motion
#pagebreak()
#kinetic
#pagebreak()
#moments
#pagebreak()
#multiple-fluids
#pagebreak()
#mhd
#pagebreak()
#collisions
#pagebreak()
#diffusion
#pagebreak()
#introduction-waves
#pagebreak()
#cold-waves
#pagebreak()
#finite-temperature-waves
#pagebreak()
#hot-waves
#pagebreak()
#sheaths
#pagebreak()
#mathematical-toolkit
#pagebreak()
#cgs-translation
#pagebreak()
#bibliography(
  "sources.bib",
  style: "american-physics-society",
  title: [Bibliography],
  full: true,
)
