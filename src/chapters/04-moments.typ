#import "../theme.typ": planned-chapter

#let chapter = planned-chapter(
  4,
  [Moments of the Boltzmann equation],
  [This chapter will derive the hierarchy from kinetic theory to fluid
  variables and make closure assumptions explicit at each moment.],
  (
    [Zeroth moment: number, mass, and charge density],
    [First moment: species velocity and momentum transport],
    [Second central moment: pressure tensor and scalar pressure],
    [Continuity, momentum, and heat-transport equations],
    [Cold and warm closures and the role of the collision term],
  ),
  previous: (href: "03-kinetic-theory.html", title: [Kinetic theory]),
  next: (href: "05-multiple-fluids.html", title: [Multiple fluids]),
)
