#import "@preview/frame-it:2.0.0": frames, frame-style, styles
#import "@preview/unify:0.8.1": num, qty, unit

// Scientific visual labels use [1] for a dimensionless unit. Keeping the
// suffix in one component makes normalized axes and legends consistent across
// figures and their paged fallbacks.
#let normalized-label(body) = [#body #h(0.25em) #text("[1]")]
#let normalized-axis(body) = normalized-label(body)

// Chapter links target a section in HTML and the same label in the print PDF.
#let chapter-link(anchor, body) = link(label(anchor), body)

#let ink = rgb("#17202A")
#let muted = rgb("#526175")
#let accent = rgb("#126E82")
#let accent-light = rgb("#D8F0F0")
#let blue = rgb("#356AA0")
#let orange = rgb("#B86418")
#let paper = rgb("#F7F9FC")

#set text(font: "Libertinus Serif", size: 11pt, fill: ink)
#set par(leading: 0.72em)

// Frame-It supplies the shared visual grammar for the teaching blocks. The
// labels remain meaningful without color, and the CSS gives them a matching
// presentation in the typed HTML output.
#let frame-set = frames(
  keyidea: ("Key idea", accent),
  definition: ("Definition", blue),
  assumption: ("Assumptions", orange),
  law: ("Governing law", accent),
  interpretation: ("Interpretation", blue),
  example: ("Rechenbeispiel", orange),
  summary: ("Summary", accent),
  knowledge: ("Knowledge check", blue),
)

#let keyidea-frame = frame-set.keyidea
#let definition-frame = frame-set.definition
#let assumption-frame = frame-set.assumption
#let law-frame = frame-set.law
#let interpretation-frame = frame-set.interpretation
#let example-frame = frame-set.example
#let summary-frame = frame-set.summary
#let knowledge-frame = frame-set.knowledge

#let keep-frame(frame) = context {
  if target() == "paged" {
    block(breakable: false)[#frame]
  } else {
    frame
  }
}

#show: frame-style(styles.boxy)

#let lead(body) = context {
  if target() == "paged" {
    block(width: 100%, inset: (top: 0.2em, bottom: 0.7em))[
      #text(size: 14pt, fill: muted)[#body]
    ]
  } else {
    html.p(class: "lede")[#body]
  }
}

// Chapter and section numbers. `page-title(number: N)` starts chapter N and
// `section-title` numbers its sections N.1, N.2, ...; appendix titles carry
// no number, and neither do their sections. Each title also records its
// number, plain-text title, and label as metadata (<script-chapter>,
// <script-section>), the single source from which the lecture slides in
// slides/ take their section titles (scripts/build-slides.sh queries it).
#let chapter-number = state("script-chapter-number", none)
#let section-number = counter("script-section-number")

#let plain-text(it) = {
  if it == none { "" }
  else if type(it) == str { it }
  else if it.has("text") { plain-text(it.text) }
  else if it.has("children") { it.children.map(plain-text).join("") }
  else if it.func() == math.attach { plain-text(it.base) }
  else if it.has("body") { plain-text(it.body) }
  else if it.func() == [ ].func() { " " }
  else { "" }
}

// The label written after a title call, e.g. `#section-title[...] <x>`,
// sits on the context element that renders the title.
#let own-label() = {
  let found = query(here())
  if found.len() > 0 and found.first().has("label") { str(found.first().label) }
}

#let page-title(number: none, body) = context {
  let title = if number == none { body } else { [#number. #body] }
  chapter-number.update(number)
  section-number.update(0)
  [#metadata((number: number, title: plain-text(body), label: own-label())) <script-chapter>]
  if target() == "paged" {
    heading(level: 1)[#title]
  } else {
    html.h1(title)
  }
}

#let section-title(body) = context {
  let chapter = chapter-number.get()
  let number = if chapter != none {
    str(chapter) + "." + str(section-number.get().first() + 1)
  }
  let title = if number == none { body } else { [#number#sym.space.en#body] }
  section-number.step()
  [#metadata((number: number, title: plain-text(body), label: own-label())) <script-section>]
  if target() == "paged" {
    heading(level: 2)[#title]
  } else {
    html.h2(title)
  }
}

#let page-shell(body, stylesheet: "styles.css", root: false) = context {
  if target() == "paged" {
    body
  } else {
    let overview = if root { "index.html" } else { "../index.html" }
    let contents = if root { "#contents" } else { "../index.html#contents" }
    let glossary = if root { "#glossary" } else { "../index.html#glossary" }
    let bibliography = if root { "#bibliography" } else { "../index.html#bibliography" }
    html.div(class: "site-shell")[
      #html.link(rel: "stylesheet", href: stylesheet)
      #html.header(class: "site-header")[
        #html.div(class: "brand")[
          #link(overview)[Plasma Physics]
        ]
        #html.nav(class: "site-nav", aria-label: "Primary navigation")[
          #link(overview)[Overview]
          #link(contents)[Contents]
          #link(glossary)[Glossary]
          #link(bibliography)[Bibliography]
        ]
      ]
      // Each web page is read on its own, so frame numbers restart per page.
      #html.main(class: "site-main")[
        #counter(figure.where(kind: "frame")).update(0)
        #body
      ]
      #html.footer(class: "site-footer")[
        Lecture notes in Typst, visualizations rendered with Manim. Authors:
        Christopher Albert and Maximilian Philipp.
      ]
    ]
  }
}

#let callout(title, body) = keep-frame(keyidea-frame[#title][][#body])

#let definition(title, body) = keep-frame(definition-frame[#title][][#body])

#let assumption(title, body) = keep-frame(assumption-frame[#title][][#body])

#let governing-law(title, body) = keep-frame(law-frame[#title][][#body])

#let interpretation(title, body) = keep-frame(interpretation-frame[#title][][#body])

#let summary(body) = keep-frame(summary-frame[Summary][][#body])

#let equation-note(body) = context {
  if target() == "paged" {
    block(
      width: 100%,
      inset: (top: 0.35em, bottom: 0.7em),
    )[
      #text(size: 8pt, fill: muted)[#body]
    ]
  } else {
    html.p(class: "equation-note")[#body]
  }
}

#let details(title, body) = context {
  if target() == "paged" {
    block(
      width: 100%,
      inset: 0.9em,
      radius: 0.45em,
      fill: paper,
      stroke: 0.8pt + muted,
      breakable: false,
    )[
      #strong(title) \
      #body
    ]
  } else {
    html.details(open: false, class: "disclosure")[
      #html.summary[#title]
      #html.div(class: "disclosure-body")[#body]
    ]
  }
}

// Use a short step label when a derivation has several conceptual turns. The
// label is part of the expanded explanation and does not hide any required
// result in the interactive target.
#let derivation-step(body) = context {
  if target() == "paged" {
    block(
      width: 100%,
      inset: (top: 0.55em, bottom: 0.15em),
    )[
      #strong[Step: #body]
    ]
  } else {
    html.p(class: "derivation-step-label")[
      #html.strong[Step: #body]
    ]
  }
}

#let objectives(items) = context {
  if target() == "paged" {
    block(
      width: 100%,
      inset: 0.9em,
      radius: 0.45em,
      fill: accent-light,
      stroke: 0.8pt + accent,
      breakable: false,
    )[
      #strong[Learning objectives] \
      #list(tight: true, ..items.map(item => [#item]))
    ]
  } else {
    html.section(class: "objectives")[
      #html.h3[Learning objectives]
      #html.ul[
        #for item in items [
          #html.li[#item]
        ]
      ]
    ]
  }
}

#let unit-ledger(body) = context {
  if target() == "paged" {
    block(
      width: 100%,
      inset: 0.9em,
      radius: 0.45em,
      fill: rgb("#FFF3E5"),
      stroke: 0.8pt + orange,
    )[
      #strong[Unit ledger] \
      #body
    ]
  } else {
    html.aside(class: "unit-ledger")[
      #html.strong[Unit ledger]
      #body
    ]
  }
}

#let rechenbeispiel(body) = keep-frame(example-frame[Rechenbeispiel][][#body])

#let exam-prompts(prompts, source) = context {
  if target() == "paged" {
    block(
      width: 100%,
      inset: 0.9em,
      radius: 0.45em,
      fill: rgb("#FFF3E5"),
      stroke: 0.8pt + orange,
      breakable: false,
    )[
      #strong[Exam questions] \
      #for prompt in prompts [
        #block[#prompt]
      ]
      #text(size: 8pt, fill: muted)[Verbatim from #source]
    ]
  } else {
    html.aside(class: "exam-prompt")[
      #html.h3[Exam questions]
      #html.ul(class: "exam-prompts-list")[
        #for prompt in prompts [
          #html.li[#prompt]
        ]
      ]
      #html.p(class: "source-note")[Verbatim from #source]
    ]
  }
}

#let knowledge-check(items) = context {
  if target() == "paged" {
    keep-frame(knowledge-frame[Knowledge check][][
      #list(..items.map(item => [#item.question]))
      #details([Answers], [
        #for item in items [
          #strong[#item.question] \
          #item.answer \
        ]
      ])
    ])
  } else {
    html.section(class: "knowledge-check")[
      #html.h3[Knowledge check]
      #html.ol[
        #for item in items [
          #html.li[
            #item.question
            #html.details(open: false)[
              #html.summary[Answer]
              #item.answer
            ]
          ]
        ]
      ]
    ]
  }
}

#let animation(path, alt-description, caption: none, poster: "") = context {
  let visible-caption = if caption == none { alt-description } else { caption }
  if target() == "paged" {
    figure(
      alt: alt-description,
      caption: [#visible-caption],
    )[
      #block(
        width: 100%,
        inset: 1em,
        radius: 0.5em,
        fill: paper,
        stroke: 1pt + muted,
      )[
        #emph[Animation available in the website build.] \
        #visible-caption
      ]
    ]
  } else {
    html.figure(class: "animation-figure")[
      #html.video(
        class: "animation-video",
        aria-label: alt-description,
        controls: true,
        loop: true,
        muted: true,
        playsinline: true,
        preload: "metadata",
        src: path,
        poster: poster,
        width: 960,
      )[
        #alt-description
      ]
      #html.figcaption[#visible-caption]
    ]
  }
}

#let chapter-nav(previous: none, next: none) = context {
  if target() == "paged" {
    // The paged fallback already has explicit chapter breaks and a table of
    // contents. Keeping navigation in the web target avoids orphaning a
    // one-line navigation block onto its own print page.
    []
  } else {
    html.nav(class: "chapter-nav", aria-label: "Chapter navigation")[
      #if previous != none {
        link(previous.href)[← #previous.title]
      }
      #if next != none {
        link(next.href)[#next.title →]
      }
    ]
  }
}

#let planned-chapter(number, title, role, sections, previous: none, next: none) = [
  #page-title[#number. #title]

  #lead[
    Foundation scaffold. This page fixes the chapter boundary, order, and
    notation plan before the full derivations are written.
  ]

  #callout(
    [Chapter status],
    [#role The completed chapter will use the section contract: motivation,
    observable objectives, definitions and units, derivation, visual or
    Rechenbeispiel, limits, summary, exam connection, and four-question
    knowledge check.]
  )

  #section-title[Planned sequence]
  #list(..sections.map(section => [#section]))

  #unit-ledger[
    Each chapter will declare its field and temperature conventions before
    its first dimensional equation and will identify every normalized
    reference scale.
  ]

  #summary[
    This scaffold is intentionally explicit about what remains to be written.
    Waves and plasma sheaths remain separate top-level chapters.
  ]

  #chapter-nav(previous: previous, next: next)
]
