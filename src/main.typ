#import "theme.typ": page-shell
#import "chapters/01-orbits.typ": chapter

#document("index.html", title: [Plasma Physics])[
  #page-shell(stylesheet: "styles.css")[
    #html.div(class: "hero")[
      #html.p(class: "eyebrow")[Lecture notes]
      #html.h1[Plasma Physics]
      #html.p(class: "lede")[
        A Typst-based script for learning the geometry, scales, and models of
        magnetized plasmas.
      ]
      #html.div(class: "hero-actions")[
        #link(<orbits>)[Start with charged-particle motion →]
      ]
    ]

    #html.section(class: "card-grid")[
      #html.article(class: "card")[
        #html.p(class: "card-kicker")[Chapter 01]
        #html.h2[Charged-particle motion]
        The Lorentz force, cyclotron motion, and the crossed-field drift.
        #link(<orbits>)[Open chapter →]
      ]
      #html.article(class: "card card-muted")[
        #html.p(class: "card-kicker")[Next]
        #html.h2[Collective behavior]
        Add Debye shielding, plasma oscillations, and the first kinetic model.
        This card marks the next content boundary for the script.
      ]
    ]

    #html.section(class: "roadmap")[
      #html.h2[Roadmap]
      #html.ol[
        #html.li[Single-particle motion]
        #html.li[Collective scales and shielding]
        #html.li[Fluid and kinetic descriptions]
        #html.li[Waves, instabilities, and transport]
      ]
    ]
  ]
] <home>

#document("chapters/01-orbits.html", title: [Charged-particle motion])[
  #page-shell(stylesheet: "../styles.css")[
    #chapter
  ]
] <orbits>

#asset("styles.css", read("styles.css"))
