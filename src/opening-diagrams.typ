#import "@preview/cetz:0.5.2": canvas, draw

// Cold uniform slab at positive displacement; charge signs are explicit.
#let electron-slab() = canvas(length: 14mm, {
  import draw: *
  rect((0,0),(6,2), stroke: 0.8pt)
  rect((0.8,0),(6.8,2), stroke: (paint: rgb("#0072B2"), dash: "dashed"))
  for y in (0.4,1,1.6) {
    content((0.4,y), [+])
    content((6.4,y), [−])
  }
  content((3.4,1), [neutral overlap])
  content((3,2.6), [fixed ions; displaced electrons])
  line((0,-0.5),(0.8,-0.5), mark: (end: ">"))
  content((0.4,-0.9), [$xi$])
  line((2,-0.5),(5,-0.5), mark: (end: ">"))
  content((3.5,-0.9), [$bold(E)$])
  line((5,-1.4),(2,-1.4), mark: (end: ">"))
  content((3.5,-1.8), [$bold(F)_e=-e bold(E)$])
})
