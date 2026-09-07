#import "theme.typ": *
#import "chapters/01-introduction.typ": chapter as introduction
#import "chapters/02-single-particle-motion.typ": chapter as motion

#show: frame-style(styles.boxy)

#set page(paper: "a4", margin: 2.2cm)
#set par(justify: true)

#align(center)[
  #text(size: 24pt, weight: "bold")[Plasma Physics]
  #v(0.5em)
  #text(fill: muted)[Graduate lecture script foundation]
  #v(0.5em)
  #text(size: 9pt, fill: muted)[Website-first source with a paged fallback]
]

#v(1.5em)
#introduction
#pagebreak()
#motion
