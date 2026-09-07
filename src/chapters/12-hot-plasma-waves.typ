#import "../theme.typ": planned-chapter

#let chapter = planned-chapter(
  12,
  [Waves in hot plasmas],
  [This chapter will use kinetic response to explain hot isotropic and
  magnetized waves, resonances, Landau effects, and the two-stream instability.],
  (
    [Hot isotropic plasma dispersion],
    [Resonant particles and velocity-space response],
    [Landau damping and growth],
    [Two-stream instability],
    [Hot magnetized waves and branch interpretation],
  ),
  previous: (href: "11-finite-temperature-waves.html", title: [Finite-temperature effects]),
  next: (href: "13-sheaths-probes.html", title: [Sheaths and probes]),
)
