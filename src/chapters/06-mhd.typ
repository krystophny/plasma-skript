#import "../theme.typ": planned-chapter

#let chapter = planned-chapter(
  6,
  [Single-fluid theory and magnetohydrodynamics],
  [This chapter will combine species equations into conservation laws for
  mass, charge, momentum, and magnetic flux, while tracking the approximations
  behind generalized Ohm's law.],
  (
    [Single-fluid mass density, charge density, current, pressure, and velocity],
    [Linearized single-fluid MHD equations],
    [Generalized Ohm's law, resistivity, and simplified limits],
    [Frozen-in flux and magnetic-field diffusion],
    [Static MHD equilibrium, pressure balance, and pinch configurations],
  ),
  previous: (href: "05-multiple-fluids.html", title: [Multiple fluids]),
  next: (href: "07-collisions-conductivity.html", title: [Collisions and conductivity]),
)
