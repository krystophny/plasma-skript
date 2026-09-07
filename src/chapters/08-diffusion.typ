#import "../theme.typ": planned-chapter

#let chapter = planned-chapter(
  8,
  [Plasma diffusion],
  [This chapter will develop diffusion from random walks and then separate
  weakly ionized, ambipolar, magnetized, and fully ionized limits.],
  (
    [Random-walk motivation and the diffusion coefficient],
    [Diffusion in weakly ionized plasmas],
    [Ambipolar diffusion and ambipolar electric fields],
    [Cross-field diffusion in a magnetic field],
    [Fully ionized diffusion and characteristic timescales],
  ),
  previous: (href: "07-collisions-conductivity.html", title: [Collisions and conductivity]),
  next: (href: "09-introduction-waves.html", title: [Introduction to waves]),
)
