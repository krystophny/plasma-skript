#import "theme.typ": page-shell, frame-style, styles, normalized-label, unit
#import "@preview/physica:0.9.8": laplacian, dv

#show: frame-style(styles.boxy)
// SVG frames in the HTML (CeTZ, Fletcher, Lilaq) use the script's typefaces,
// STIX Two Text and STIX Two Math (fonts/, compile with --font-path fonts).
#set text(font: "STIX Two Text")
#show math.equation: set text(font: "STIX Two Math")
#import "chapters/01-introduction.typ": chapter as introduction
#import "chapters/02-thermal-equilibrium.typ": chapter as thermal-equilibrium
#import "chapters/03-debye-shielding.typ": chapter as debye-shielding
#import "chapters/04-plasma-oscillations.typ": chapter as plasma-oscillations
#import "chapters/05-single-particle-motion.typ": chapter as motion
#import "chapters/06-kinetic-theory.typ": chapter as kinetic
#import "chapters/07-moments.typ": chapter as moments
#import "chapters/08-multiple-fluids.typ": chapter as multiple-fluids
#import "chapters/09-mhd.typ": chapter as mhd
#import "chapters/10-collisions-conductivity.typ": chapter as collisions
#import "chapters/11-diffusion.typ": chapter as diffusion
#import "chapters/12-introduction-waves.typ": chapter as introduction-waves
#import "chapters/13-cold-magnetized-waves.typ": chapter as cold-waves
#import "chapters/14-finite-temperature-waves.typ": chapter as finite-temperature-waves
#import "chapters/15-hot-plasma-waves.typ": chapter as hot-waves
#import "chapters/16-sheaths-probes.typ": chapter as sheaths
#import "appendices/mathematical-toolkit.typ": appendix as mathematical-toolkit
#import "appendices/cgs-translation.typ": appendix as cgs-translation

#let chapters = (
  (
    number: 1,
    title: [Introduction, plasma state, and model hierarchy],
    slug: "01-introduction",
    status: "drafted",
    summary: [Plasma examples, temperature, characteristic lengths and times, and model selection.],
  ),
  (
    number: 2,
    title: [Temperature, entropy, and thermal ionization],
    slug: "02-thermal-equilibrium",
    status: "drafted",
    summary: [Counted entropy, temperature, Boltzmann weights, and thermal ionization.],
  ),
  (
    number: 3,
    title: [Debye shielding],
    slug: "03-debye-shielding",
    status: "drafted",
    summary: [Boltzmann response, the Debye length, screened potentials, and finite spherical sources.],
  ),
  (
    number: 4,
    title: [Plasma oscillations],
    slug: "04-plasma-oscillations",
    status: "drafted",
    summary: [Electron displacement, the restoring electric field, and the cold plasma frequency.],
  ),
  (
    number: 5,
    title: [Single-particle motion],
    slug: "05-single-particle-motion",
    status: "drafted",
    summary: [Gyromotion, homogeneous-force drifts, guiding centers, mirrors, polarization drift, and cyclotron resonance.],
  ),
  (
    number: 6,
    title: [Kinetic theory of plasmas],
    slug: "06-kinetic-theory",
    status: "drafted",
    summary: [Collisions, distribution functions, phase space, kinetic balance, and model limits.],
  ),
  (
    number: 7,
    title: [Moments of the Boltzmann equation],
    slug: "07-moments",
    status: "drafted",
    summary: [Velocity moments, continuity, momentum and energy transport, and closure.],
  ),
  (
    number: 8,
    title: [Multiple-fluid theory of plasmas],
    slug: "08-multiple-fluids",
    status: "drafted",
    summary: [Two-fluid hydrogen plasma, species forces, and diamagnetic current.],
  ),
  (
    number: 9,
    title: [Single-fluid theory and magnetohydrodynamics],
    slug: "09-mhd",
    status: "drafted",
    summary: [MHD variables, Ohm's law, frozen flux, diffusion, and equilibrium.],
  ),
  (
    number: 10,
    title: [Collisions and plasma conductivity],
    slug: "10-collisions-conductivity",
    status: "drafted",
    summary: [Neutral and Coulomb collisions, Spitzer resistivity, and DC or AC conductivity tensors.],
  ),
  (
    number: 11,
    title: [Plasma diffusion],
    slug: "11-diffusion",
    status: "drafted",
    summary: [Random walks, ambipolar transport, cross-field diffusion, and classical or Bohm-like limits.],
  ),
  (
    number: 12,
    title: [Introduction to waves in plasmas],
    slug: "12-introduction-waves",
    status: "drafted",
    summary: [Linearization, plasma oscillations, electromagnetic dispersion, and kinetic limits.],
  ),
  (
    number: 13,
    title: [Waves in cold magnetized plasmas],
    slug: "13-cold-magnetized-waves",
    status: "drafted",
    summary: [Cold dielectric tensor, circular and principal modes, oblique propagation, cutoffs, and resonances.],
  ),
  (
    number: 14,
    title: [Collisions, ions, and finite-temperature effects on magnetized waves],
    slug: "14-finite-temperature-waves",
    status: "drafted",
    summary: [Collisional damping, ion-cyclotron and Alfvén branches, warm dispersion, and model ordering.],
  ),
  (
    number: 15,
    title: [Waves in hot plasmas],
    slug: "15-hot-plasma-waves",
    status: "drafted",
    summary: [Vlasov response, velocity-space resonances, Landau damping, two-stream growth, and hot magnetized harmonics.],
  ),
  (
    number: 16,
    title: [Plasma sheaths and Langmuir probes],
    slug: "16-sheaths-probes",
    status: "drafted",
    summary: [Particle flux, Bohm sheath entry, floating surfaces, and Langmuir-probe diagnostics.],
  ),
)

#document("index.html", title: [Plasma Physics])[
  #page-shell(stylesheet: "styles.css", root: true)[
    #html.div(class: "hero")[
      #html.p(class: "eyebrow")[Graduate lecture notes]
      #html.h1[Plasma Physics]
      #html.p(class: "lede")[
        From single-particle orbits to collective waves, transport, and
        plasma sheaths.
      ]
      #html.div(class: "hero-actions")[
        #link("chapters/01-introduction.html")[Start reading]
        #link("#contents")[Contents]
        #link("present/")[Lecture decks]
      ]
    ]

    #html.section(class: "catalog", id: "contents")[
      #html.h2[Contents]
      #html.p[
        Each section states its question, assumptions, and units, and ends
        with a short knowledge check. Optional derivations are collapsed.
      ]
      #html.ol(class: "chapter-list")[
        #for item in chapters [
          #html.li(class: "chapter-item")[
            #html.div(class: "chapter-number")[#item.number]
            #html.div(class: "chapter-copy")[
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
      #html.h2[Gaussian CGS translation]
      #html.p[
        A one-table dictionary from the equations of this script to the
        Gaussian CGS forms used in much of the older plasma literature.
      ]
      #link("appendices/cgs-translation.html")[Open the CGS translation →]
    ]

    #html.section(class: "content-sections", id: "glossary")[
      #html.p(class: "eyebrow")[Glossary]
      #html.h2[Notation and conventions]
      #html.dl[
        #html.dt[SI units]
        #html.dd[
          This script uses SI units throughout, with vacuum permittivity
          $epsilon_0$ and permeability $mu_0$. For a charge $q$, the Lorentz force is
          $bold(F)=q (bold(E) + bold(v) times bold(B))$, and electrostatic
          Poisson's equation for charge density $rho_q$ is
          $laplacian(phi) = -rho_q/epsilon_0$. The symbol $rho$ without the
          subscript denotes mass density. Gaussian CGS equivalents are listed
          only in the #link("appendices/cgs-translation.html")[CGS translation appendix].
        ]
        #html.dt[Normalized quantity]
        #html.dd[
          A dimensionless quantity formed by dividing by a stated reference
          scale, such as #normalized-label[$x/lambda_D$] or
          #normalized-label[$t omega_p$]. Dimensional reconstruction is given
          where the quantity is used.
        ]
        #html.dt[Statistical notation]
        #html.dd[
          Multiplicity is $W$ (a dimensionless microstate count), never $Omega$.
          Entropy is $S=k_B ln W$ in #unit("J/K"). The ionization energy $chi$
          is in #unit("J") or #unit("eV"); scattering angles use $theta_("sc")$.
          Chemical potential $mu$ is an energy per particle; mechanical mobility
          is $mu_("mob")$, and magnetic moment is $mu_("mag")$ in #unit("J/T").
          Total kinetic-energy density is $E_("kin",s)$ in #unit("J/m^3"),
          keeping $W_s$ available for species multiplicity.
          Slots $M_s$ and internal degeneracies $g_s$ are
          dimensionless counts. Neutral, ion, and electron densities are
          $n_n$, $n_i$, and $n_e$ in #unit("m^-3"). The thermal de Broglie
          wavelength is $lambda_("th",s)=h/sqrt(2 pi m_s k_B T)$ in #unit("m"),
          with Planck's constant $h$ in #unit("J.s"). For electrons,
          $lambda_("th",e)=h/(sqrt(pi) m_e v_("th",e))$.
          Thermal momentum $p_("th",s)=sqrt(2 m_s k_B T)$ is in #unit("kg.m/s").
          A sharp momentum cutoff $p_s$ is in #unit("kg.m/s"); its estimate
          $lambda_s=h/p_s$ is in #unit("m") and is distinct from
          $lambda_("th",s)$, which uses the Maxwellian-weighted momentum states.
          Normalized wave frequency uses $hat(omega)$, reserving $W$ for multiplicity.
        ]
        #html.dt[Gyrofrequency]
        #html.dd[
          The positive rate $omega_c = (abs(q) B)/m$. The
          signed quantity $Omega = (q B)/m$ retains charge orientation.
        ]
        #html.dt[Debye length]
        #html.dd[
          The electron screening length when ions do not respond and the
          electrons have thermodynamic temperature $T_e$ is
          $lambda_D = sqrt((epsilon_0 k_B T_e)/(n_e e^2))$.
          If several classical species respond with Boltzmann densities,
          $lambda_D^(-2)=sum_s (n_s q_s^2)/(epsilon_0 k_B T_s)$.
        ]
        #html.dt[Thermal speed and distribution]
        #html.dd[
          The convention is $v_("th,s")=sqrt((2 k_B T_s)/m_s)$;
          a centered Maxwellian varies as $exp(-v^2/v_("th,s")^2)$.
          The three-velocity distribution satisfies
          $integral f_(s) dif^3 bold(v)=n_s$. A one-velocity marginal
          integrates over the other two velocity components; it is not a slice.
        ]
        #html.dt[Wave convention]
        #html.dd[
          Perturbations use $exp(i (bold(k) dot bold(r)-omega t))$.
          With $omega=omega_r+i gamma$, positive $gamma$ means temporal
          growth. For real frequency and propagation toward increasing $z$,
          $k=k_r+i k_i$ with $k_i>0$ means spatial attenuation.
        ]
        #html.dt[Wave-number normalization]
        #html.dd[
          The refractive index is #normalized-label[$N=(k c)/omega$].
          A different coordinate is #normalized-label[$K=(k c)/omega_p$],
          with #normalized-label[$hat(omega)=omega/omega_p$] and $K=N hat(omega)$.
          In vacuum $N=1$, equivalently $hat(omega)=K$; these axes are not interchangeable.
        ]
        #html.dt[Gyroangle]
        #html.dd[
          With $bold(B)_0=B_0 bold(e)_z$, the usual counterclockwise angle
          defined by $v_x=v_perp cos(theta)$ and $v_y=v_perp sin(theta)$
          obeys $dv(theta,t)=-Omega_s$. The hot-plasma harmonic expansion
          explicitly uses the opposite orientation; its signed frequency
          and harmonic labels must be read with that definition.
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
        Citations are numeric and are generated from the public BibLaTeX
        database. The Typst reference @typst-reference and typed-HTML
        reference @typst-html describe the authoring and web output. Scientific
        notation and unit-bearing quantities use @physica and @unify;
        diagrams, plots, and highlighted teaching blocks use @cetz @fletcher
        @lilaq and @frame-it. The Manim documentation @manim describes the
        animation workflow. The books and course PDFs used for reference remain
        private and are not copied into the public site.
      ]
      #bibliography(
        "sources.bib",
        title: none,
        full: true,
        style: "american-physics-society",
      )
    ]

    #html.section(class: "content-sections contributors")[
      #html.p(class: "eyebrow")[Contributors and license]
      #html.h2[Contributing]
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

#document("chapters/02-thermal-equilibrium.html", title: [Thermal equilibrium])[
  #page-shell(stylesheet: "../styles.css")[#thermal-equilibrium]
]

#document("chapters/03-debye-shielding.html", title: [Debye shielding])[
  #page-shell(stylesheet: "../styles.css")[#debye-shielding]
]

#document("chapters/04-plasma-oscillations.html", title: [Plasma oscillations])[
  #page-shell(stylesheet: "../styles.css")[#plasma-oscillations]
]

#document("chapters/05-single-particle-motion.html", title: [Single-particle motion])[
  #page-shell(stylesheet: "../styles.css")[#motion]
]

#document("chapters/06-kinetic-theory.html", title: [Kinetic theory])[
  #page-shell(stylesheet: "../styles.css")[#kinetic]
]

#document("chapters/07-moments.html", title: [Moments])[
  #page-shell(stylesheet: "../styles.css")[#moments]
]

#document("chapters/08-multiple-fluids.html", title: [Multiple fluids])[
  #page-shell(stylesheet: "../styles.css")[#multiple-fluids]
]

#document("chapters/09-mhd.html", title: [Single-fluid MHD])[
  #page-shell(stylesheet: "../styles.css")[#mhd]
]

#document("chapters/10-collisions-conductivity.html", title: [Collisions and conductivity])[
  #page-shell(stylesheet: "../styles.css")[#collisions]
]

#document("chapters/11-diffusion.html", title: [Diffusion])[
  #page-shell(stylesheet: "../styles.css")[#diffusion]
]

#document("chapters/12-introduction-waves.html", title: [Introduction to waves])[
  #page-shell(stylesheet: "../styles.css")[#introduction-waves]
]

#document("chapters/13-cold-magnetized-waves.html", title: [Cold magnetized waves])[
  #page-shell(stylesheet: "../styles.css")[#cold-waves]
]

#document("chapters/14-finite-temperature-waves.html", title: [Finite-temperature waves])[
  #page-shell(stylesheet: "../styles.css")[#finite-temperature-waves]
]

#document("chapters/15-hot-plasma-waves.html", title: [Hot plasma waves])[
  #page-shell(stylesheet: "../styles.css")[#hot-waves]
]

#document("chapters/16-sheaths-probes.html", title: [Sheaths and probes])[
  #page-shell(stylesheet: "../styles.css")[#sheaths]
]

#document("appendices/mathematical-toolkit.html", title: [Mathematical toolkit])[
  #page-shell(stylesheet: "../styles.css")[#mathematical-toolkit]
]

#document("appendices/cgs-translation.html", title: [Gaussian CGS translation])[
  #page-shell(stylesheet: "../styles.css")[#cgs-translation]
]

#asset("styles.css", read("styles.css"))
#for name in ("STIXTwoMath-Regular", "STIXTwoText-Regular",
    "STIXTwoText-Italic", "STIXTwoText-Bold", "STIXTwoText-BoldItalic") {
  asset("fonts/" + name + ".otf",
    read("../fonts/" + name + ".otf", encoding: none))
}
#asset("fonts/OFL.txt", read("../fonts/OFL.txt"))
