#import "../theme.typ": planned-chapter

#let chapter = planned-chapter(
  11,
  [Collisions, ions, and finite-temperature effects on magnetized waves],
  [This chapter will extend the cold response by adding collisions, ion
  inertia, and thermal corrections while keeping the wave branches separate.],
  (
    [Collisional dielectric response and damping],
    [Ion motion and low-frequency branches],
    [Warm-fluid pressure corrections],
    [Finite-temperature magnetized-wave ordering],
    [Connecting collisional and collisionless limits],
  ),
  previous: (href: "10-cold-magnetized-waves.html", title: [Cold magnetized waves]),
  next: (href: "12-hot-plasma-waves.html", title: [Hot plasma waves]),
)
