#let ink = rgb("#17202A")
#let muted = rgb("#526175")
#let accent = rgb("#126E82")
#let accent-light = rgb("#D8F0F0")
#let paper = rgb("#F7F9FC")

#set text(font: "Libertinus Serif", size: 11pt, fill: ink)
#set par(leading: 0.72em)

#let lead(body) = context {
  if target() == "paged" {
    block(width: 100%, inset: (top: 0.2em, bottom: 0.7em))[#text(size: 14pt, fill: muted)[#body]]
  } else {
    html.p(class: "lede")[#body]
  }
}

#let page-title(body) = context {
  if target() == "paged" {
    heading(level: 1)[#body]
  } else {
    html.h1(body)
  }
}

#let section-title(body) = context {
  if target() == "paged" {
    heading(level: 2)[#body]
  } else {
    html.h2(body)
  }
}

#let page-shell(body, stylesheet: "styles.css") = context {
  if target() == "paged" {
    body
  } else {
    html.div(class: "site-shell")[
      #html.link(rel: "stylesheet", href: stylesheet)
      #html.header(class: "site-header")[
        #html.div(class: "brand")[
          #html.span(class: "brand-mark")[PL]
          #html.span[Plasma physics]
        ]
        #html.nav(class: "site-nav")[
          #link(<home>)[Overview]
          #link(<orbits>)[Charged-particle motion]
        ]
      ]
      #html.main(class: "site-main")[#body]
      #html.footer(class: "site-footer")[
        Lecture notes in Typst, visualizations rendered with Manim.
      ]
    ]
  }
}

#let callout(title, body) = context {
  if target() == "paged" {
    block(
      width: 100%,
      inset: 1em,
      radius: 0.5em,
      fill: accent-light,
      stroke: (left: 3pt + accent),
    )[
      #strong(title) \
      #body
    ]
  } else {
    html.aside(class: "callout")[
      #html.strong[#title]
      #body
    ]
  }
}

#let animation(path, description) = context {
  if target() == "paged" {
    figure(
      caption: [#description],
    )[
      #block(
        width: 100%,
        inset: 1em,
        radius: 0.5em,
        fill: paper,
        stroke: 1pt + muted,
      )[
        #emph[Animation available in the website build.] \
        #description
      ]
    ]
  } else {
    html.figure(class: "animation-figure")[
      #html.video(
        class: "animation-video",
        controls: true,
        loop: true,
        muted: true,
        playsinline: true,
        preload: "metadata",
        src: path,
        width: 960,
      )[
        #description
      ]
      #html.figcaption[#description]
    ]
  }
}
