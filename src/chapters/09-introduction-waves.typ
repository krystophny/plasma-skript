#import "../theme.typ": planned-chapter

#let chapter = planned-chapter(
  9,
  [Introduction to waves in plasmas],
  [This chapter will introduce small-amplitude perturbations, normal modes,
  dispersion, and the distinction between electrostatic and electromagnetic
  plasma waves.],
  (
    [Equilibrium, perturbation, and linearization assumptions],
    [Nonmagnetized plasma response and plasma oscillations],
    [Phase velocity, group velocity, and dispersion],
    [Cold-fluid wave equations and their kinetic limits],
    [Reading dispersion diagrams and checking limiting cases],
  ),
  previous: (href: "08-diffusion.html", title: [Diffusion]),
  next: (href: "10-cold-magnetized-waves.html", title: [Cold magnetized waves]),
)
