#import "theme.typ": *
#import "chapters/01-introduction.typ": chapter as introduction
#import "chapters/02-debye-shielding.typ": chapter as debye-shielding
#import "chapters/03-plasma-oscillations.typ": chapter as plasma-oscillations
#import "chapters/04-single-particle-motion.typ": chapter as motion
#import "chapters/05-kinetic-theory.typ": chapter as kinetic
#import "chapters/06-moments.typ": chapter as moments
#import "chapters/07-multiple-fluids.typ": chapter as multiple-fluids
#import "chapters/08-mhd.typ": chapter as mhd
#import "chapters/09-collisions-conductivity.typ": chapter as collisions
#import "chapters/10-diffusion.typ": chapter as diffusion
#import "chapters/11-introduction-waves.typ": chapter as introduction-waves
#import "chapters/12-cold-magnetized-waves.typ": chapter as cold-waves
#import "chapters/13-finite-temperature-waves.typ": chapter as finite-temperature-waves
#import "chapters/14-hot-plasma-waves.typ": chapter as hot-waves
#import "chapters/15-sheaths-probes.typ": chapter as sheaths
#import "appendices/mathematical-toolkit.typ": appendix as mathematical-toolkit
#import "appendices/cgs-translation.typ": appendix as cgs-translation

#show: frame-style(styles.boxy)

#set page(paper: "a4", margin: 2.2cm)
#set par(justify: true)

#align(center)[
  #text(size: 24pt, weight: "bold")[Plasma Physics]
  #v(0.5em)
  #text(fill: muted)[Graduate lecture script foundation]
  #v(0.5em)
  #text(size: 9pt, fill: muted)[Website-first source with a paged fallback]
]

#v(1.5em)
#introduction
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
