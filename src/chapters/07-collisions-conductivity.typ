#import "../theme.typ": planned-chapter

#let chapter = planned-chapter(
  7,
  [Collisions and plasma conductivity],
  [This chapter will connect Coulomb collisions and collisional drag to
  resistivity and the frequency-dependent conductivity of a plasma.],
  (
    [Weakly and fully ionized plasma collision regimes],
    [Coulomb collisions and collision frequencies],
    [Specific resistivity and Spitzer scaling],
    [DC and AC conductivity],
    [Ion motion and the limits of electron-only transport models],
  ),
  previous: (href: "06-mhd.html", title: [Single-fluid MHD]),
  next: (href: "08-diffusion.html", title: [Diffusion]),
)
