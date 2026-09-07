#import "../theme.typ": planned-chapter

#let chapter = planned-chapter(
  3,
  [Kinetic theory of plasmas],
  [This chapter will make the one-particle distribution function the central
  dynamical variable and distinguish collisional from collisionless plasma
  kinetics.],
  (
    [Gas versus plasma collisions: mean free path, collision frequency, and long-range Coulomb scattering],
    [Distribution functions in physical and phase space],
    [Convective derivatives and the Vlasov or Boltzmann equation],
    [Conservative and convective forms of kinetic balance],
    [Maxwell--Boltzmann equilibrium and non-equilibrium distributions],
  ),
  previous: (href: "02-single-particle-motion.html", title: [Single-particle motion]),
  next: (href: "04-moments.html", title: [Moments]),
)
