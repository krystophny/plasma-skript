#import "theme.typ": page-shell, frame-style, styles, register-cgs-units

#register-cgs-units

#show: frame-style(styles.boxy)
#import "chapters/01-introduction.typ": chapter as introduction
#import "chapters/02-single-particle-motion.typ": chapter as motion
#import "chapters/03-kinetic-theory.typ": chapter as kinetic
#import "chapters/04-moments.typ": chapter as moments
#import "chapters/05-multiple-fluids.typ": chapter as multiple-fluids
#import "chapters/06-mhd.typ": chapter as mhd
#import "chapters/07-collisions-conductivity.typ": chapter as collisions
#import "chapters/08-diffusion.typ": chapter as diffusion
#import "chapters/09-introduction-waves.typ": chapter as introduction-waves
#import "chapters/10-cold-magnetized-waves.typ": chapter as cold-waves
#import "chapters/11-finite-temperature-waves.typ": chapter as finite-temperature-waves
#import "chapters/12-hot-plasma-waves.typ": chapter as hot-waves
#import "chapters/13-sheaths-probes.typ": chapter as sheaths
#import "appendices/mathematical-toolkit.typ": appendix as mathematical-toolkit

#let chapters = (
  (
    number: 1,
    title: [Introduction, plasma state, and model hierarchy],
    slug: "01-introduction",
    status: "drafted",
    summary: [Scales, collective behavior, Debye shielding, oscillations, and model selection.],
  ),
  (
    number: 2,
    title: [Single-particle motion],
    slug: "02-single-particle-motion",
    status: "drafted",
    summary: [Gyromotion, homogeneous-force drifts, guiding centers, mirrors, and curvature.],
  ),
  (
    number: 3,
    title: [Kinetic theory of plasmas],
    slug: "03-kinetic-theory",
    status: "drafted",
    summary: [Collisions, distribution functions, phase space, kinetic balance, and model limits.],
  ),
  (
    number: 4,
    title: [Moments of the Boltzmann equation],
    slug: "04-moments",
    status: "drafted",
    summary: [Velocity moments, continuity, momentum and energy transport, and closure.],
  ),
  (
    number: 5,
    title: [Multiple-fluid theory of plasmas],
    slug: "05-multiple-fluids",
    status: "drafted",
    summary: [Two-fluid hydrogen plasma, species forces, and diamagnetic current.],
  ),
  (
    number: 6,
    title: [Single-fluid theory and magnetohydrodynamics],
    slug: "06-mhd",
    status: "drafted",
    summary: [MHD variables, Ohm's law, frozen flux, diffusion, and equilibrium.],
  ),
  (
    number: 7,
    title: [Collisions and plasma conductivity],
    slug: "07-collisions-conductivity",
    status: "drafted",
    summary: [Neutral and Coulomb collisions, Spitzer resistivity, and DC or AC conductivity tensors.],
  ),
  (
    number: 8,
    title: [Plasma diffusion],
    slug: "08-diffusion",
    status: "drafted",
    summary: [Random walks, ambipolar transport, cross-field diffusion, and classical or Bohm-like limits.],
  ),
  (
    number: 9,
    title: [Introduction to waves in plasmas],
    slug: "09-introduction-waves",
    status: "drafted",
    summary: [Linearization, plasma oscillations, electromagnetic dispersion, and kinetic limits.],
  ),
  (
    number: 10,
    title: [Waves in cold magnetized plasmas],
    slug: "10-cold-magnetized-waves",
    status: "drafted",
    summary: [Cold dielectric tensor, circular and principal modes, oblique propagation, cutoffs, and resonances.],
  ),
  (
    number: 11,
    title: [Collisions, ions, and finite-temperature effects on magnetized waves],
    slug: "11-finite-temperature-waves",
    status: "drafted",
    summary: [Collisional damping, ion-cyclotron and Alfvén branches, warm dispersion, and model ordering.],
  ),
  (
    number: 12,
    title: [Waves in hot plasmas],
    slug: "12-hot-plasma-waves",
    status: "drafted",
    summary: [Vlasov response, velocity-space resonances, Landau damping, two-stream growth, and hot magnetized harmonics.],
  ),
  (
    number: 13,
    title: [Plasma sheaths and Langmuir probes],
    slug: "13-sheaths-probes",
    status: "drafted",
    summary: [Particle flux, Bohm sheath entry, floating surfaces, and Langmuir-probe diagnostics.],
  ),
)

#document("index.html", title: [Plasma Physics])[
  #page-shell(stylesheet: "styles.css", root: true)[
    #html.div(class: "hero")[
      #html.p(class: "eyebrow")[Graduate lecture script]
      #html.h1[Plasma Physics]
      #html.p(class: "lede")[
        A Typst-based, web-first script for reasoning from single-particle
        orbits to collective waves, transport, and plasma sheaths.
      ]
      #html.div(class: "hero-actions")[
        #link("chapters/01-introduction.html")[Start with the introduction →]
        #link("chapters/02-single-particle-motion.html")[Open motion chapter →]
      ]
    ]

    #html.section(class: "project-note")[
      #html.strong[Reading contract]
      Each section states its physical question, learning objectives,
      definitions, Gaussian-CGS unit convention, derivation, visual or
      Rechenbeispiel, limits, summary, exam connection, and four-question
      knowledge check. Optional derivations are collapsed in the website.
      Animations have controls, captions, and alternative descriptions.
    ]

    #html.section(class: "catalog", id: "contents")[
      #html.p(class: "eyebrow")[Contents]
      #html.h2[Chronological course map]
      #html.p[
        The order follows the rendered course-material sequence. Waves and
        plasma sheaths are separate top-level chapters. A supplemental
        mathematical toolkit follows the course map without changing its
        chronology.
      ]
      #html.ol(class: "chapter-list")[
        #for item in chapters [
          #html.li(class: "chapter-item")[
            #html.div(class: "chapter-number")[#item.number]
            #html.div(class: "chapter-copy")[
              #html.p(class: "card-kicker")[Chapter #item.number · #item.status]
              #html.h3[
                #link("chapters/" + item.slug + ".html")[#item.title]
              ]
              #html.p[#item.summary]
            ]
          ]
        ]
      ]
    ]

    #html.section(class: "content-sections supplemental", id: "appendices")[
      #html.p(class: "eyebrow")[Supplemental reference]
      #html.h2[Mathematical toolkit]
      #html.p[
        A compact reference for the energy-weighted second moment of the
        kinetic equation and vector operators in common coordinate systems.
        Full derivation routes are available as collapsed supplemental detail.
      ]
      #link("appendices/mathematical-toolkit.html")[Open the mathematical toolkit →]
    ]

    #html.section(class: "content-sections", id: "glossary")[
      #html.p(class: "eyebrow")[Glossary]
      #html.h2[Notation and conventions]
      #html.dl[
        #html.dt[Gaussian CGS]
        #html.dd[
          The default electromagnetic unit convention. In particular, the
          magnetic part of the Lorentz force contains $bold(v) times bold(B)/c$
          and electrostatic Poisson's equation contains $4 pi$.
        ]
        #html.dt[Normalized quantity]
        #html.dd[
          A dimensionless quantity formed by dividing by a stated reference
          scale, such as $x/lambda_D$ or $t omega_p$. Dimensional reconstruction
          is given where the quantity is used.
        ]
        #html.dt[Gyrofrequency]
        #html.dd[
          The positive rate $omega_c = abs(q)B/(m c)$ in Gaussian CGS. The
          signed quantity $Omega = q B/(m c)$ retains charge orientation.
        ]
        #html.dt[Debye length]
        #html.dd[
          The equilibrium electrostatic response length. For a simple
          electron--ion plasma, $lambda_D = sqrt(k_B T_e/(4 pi n_e e^2))$ in
          Gaussian CGS.
        ]
        #html.dt[Closure]
        #html.dd[
          An additional constitutive assumption that terminates a moment or
          reduced-model hierarchy.
        ]
      ]
    ]

    #html.section(class: "content-sections", id: "bibliography")[
      #html.p(class: "eyebrow")[Bibliography]
      #html.h2[Sources and implementation references]
      #html.p[
        Citations are numeric. The books and course PDFs used for reference
        remain private and are not copied into the public site.
      ]
      #html.ol(class: "bibliography")[
        #html.li[
          F. F. Chen, #html.em[Introduction to Plasma Physics and Controlled
          Fusion], 3rd ed., Springer, 2016.
        ]
        #html.li[
          J. A. Bittencourt, #html.em[Fundamentals of Plasma Physics], 3rd ed.,
          Springer, 2004.
        ]
        #html.li[
          Plasma Physics Exam catalogue, PHT.512UF, private course material,
          p. 1–3.
        ]
        #html.li[
          Typst reference and package manuals, accessed through the local
          resource set. The current package versions are declared in
          #html.code[flake.nix].
        ]
        #html.li[
          #html.a(href: "https://typst.app/docs/reference/html/typed/")[Typst
          typed HTML reference], for the disclosure component and semantic
          HTML.
        ]
        #html.li[
          #html.a(href: "https://typst.app/universe/package/unify")[unify
          unit package documentation], version 0.8.1, for unit-bearing
          quantities and numerical results.
        ]
      ]
    ]

    #html.section(class: "content-sections contributors")[
      #html.p(class: "eyebrow")[Contributors and license]
      #html.h2[Build this with us]
      #html.p[
        Original teaching content is released under CC BY 4.0. Source code,
        Typst components, CSS, Nix expressions, build scripts, and Manim source
        are released under the MIT license. Contributions are recorded in the
        public contributors list with their role or changed area.
      ]
      #html.p[
        Initial authors: Christopher Albert and Maximilian Philipp.
        See #html.code[CONTRIBUTORS.md] and #html.code[CONTRIBUTING.md] for
        contribution terms.
      ]
    ]
  ]
] <home>

#document("chapters/01-introduction.html", title: [Introduction])[
  #page-shell(stylesheet: "../styles.css")[#introduction]
]

#document("chapters/02-single-particle-motion.html", title: [Single-particle motion])[
  #page-shell(stylesheet: "../styles.css")[#motion]
]

#document("chapters/03-kinetic-theory.html", title: [Kinetic theory])[
  #page-shell(stylesheet: "../styles.css")[#kinetic]
]

#document("chapters/04-moments.html", title: [Moments])[
  #page-shell(stylesheet: "../styles.css")[#moments]
]

#document("chapters/05-multiple-fluids.html", title: [Multiple fluids])[
  #page-shell(stylesheet: "../styles.css")[#multiple-fluids]
]

#document("chapters/06-mhd.html", title: [Single-fluid MHD])[
  #page-shell(stylesheet: "../styles.css")[#mhd]
]

#document("chapters/07-collisions-conductivity.html", title: [Collisions and conductivity])[
  #page-shell(stylesheet: "../styles.css")[#collisions]
]

#document("chapters/08-diffusion.html", title: [Diffusion])[
  #page-shell(stylesheet: "../styles.css")[#diffusion]
]

#document("chapters/09-introduction-waves.html", title: [Introduction to waves])[
  #page-shell(stylesheet: "../styles.css")[#introduction-waves]
]

#document("chapters/10-cold-magnetized-waves.html", title: [Cold magnetized waves])[
  #page-shell(stylesheet: "../styles.css")[#cold-waves]
]

#document("chapters/11-finite-temperature-waves.html", title: [Finite-temperature waves])[
  #page-shell(stylesheet: "../styles.css")[#finite-temperature-waves]
]

#document("chapters/12-hot-plasma-waves.html", title: [Hot plasma waves])[
  #page-shell(stylesheet: "../styles.css")[#hot-waves]
]

#document("chapters/13-sheaths-probes.html", title: [Sheaths and probes])[
  #page-shell(stylesheet: "../styles.css")[#sheaths]
]

#document("appendices/mathematical-toolkit.html", title: [Mathematical toolkit])[
  #page-shell(stylesheet: "../styles.css")[#mathematical-toolkit]
]

#asset("styles.css", read("styles.css"))
