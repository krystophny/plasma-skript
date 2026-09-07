#import "../theme.typ": planned-chapter

#let chapter = planned-chapter(
  5,
  [Multiple-fluid theory of plasmas],
  [This chapter will retain separate species fluids so that electron--ion
  dynamics, pressure forces, and species-dependent drifts remain visible.],
  (
    [Two-fluid equations for a hydrogen plasma],
    [Species continuity, momentum, and energy balances],
    [Pressure-gradient and diamagnetic drifts],
    [Diamagnetic current and its physical interpretation],
    [Parallel force balance and the route to one-fluid variables],
  ),
  previous: (href: "04-moments.html", title: [Moments]),
  next: (href: "06-mhd.html", title: [Single-fluid MHD]),
)
