// Shared layout of the live lecture decks (slides/<stem>.typ).
//
// Page: A4 landscape, white, 20 mm margins on all sides. Layout grid: twelve
// 15 mm columns with a 7 mm gutter across the 257 mm text width; every
// element starts and ends on a column edge. Content starts at the top margin;
// on the first page of a section it starts below the section title.
//
// Type: Libertinus Serif and Libertinus Math, the typefaces of the script.
// Two text sizes: 26 pt for the section and chapter title, 18 pt for
// everything else, formulas included. Page numbers, the photo credit lines
// and the title page's transparency line are page furniture at 11 pt.
// Derived plots are the script's figures, scaled by 1.8 so their 10 pt labels
// match the 18 pt body (derivations/si.py: SLIDE_SCALE, slide_width).
//
// Section numbers and titles come from the script: scripts/build-slides.sh
// queries the <script-section> metadata of src/print.typ into
// slides/build/script-outline.json before compiling the decks, and copies the
// animation posters to slides/build/media/.
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#let ink = rgb("#17202A")
#let muted = rgb("#526175")
#let rule = rgb("#9AA5B1")
#let plot-blue = rgb("#0072B2")
#let plot-orange = rgb("#D55E00")

#let title-size = 26pt
#let body-size = 18pt
#let small-size = 11pt

#let margin = 20mm
#let text-width = 257mm
#let text-height = 170mm
#let column = 15mm
#let gutter = 7mm
// Width of n grid columns and the left edge of column c (1-based).
#let cols(n) = n * column + (n - 1) * gutter
#let col-x(c) = (c - 1) * (column + gutter)
// Content top on the first page of a section (below the section title).
#let title-band = 20mm
// Fixed baseline of the page furniture in the bottom margin.
#let furniture-y = 11mm

// Plots of derived results: derivations/build/fig/<name>.svg, scaled so the
// labels equal the body size. `plot-size` is the natural size divided out.
#let plot-scale = 1.8
#let plot-path(name) = "/derivations/build/fig/" + name + ".svg"
#let plot(name, columns: 6) = image(plot-path(name), width: cols(columns))
#let poster-path(slug) = "/slides/build/media/" + slug + ".png"
#let animation-url(name) = (
  "https://cloud.tugraz.at/public.php/dav/files/S4bwLaYWgXtHQak/animations/"
  + name + ".mp4"
)

// Script outline: chapter and section numbers and titles.
#let script-outline = json("/slides/build/script-outline.json")
#let chapter-info(number) = {
  let found = script-outline.chapters.filter(c => c.number == number)
  assert(found.len() == 1, message: "no script chapter " + str(number))
  found.first()
}
#let section-info(label) = {
  let found = script-outline.sections.filter(s => s.label == label)
  assert(found.len() == 1, message: "no script section <" + label + ">")
  found.first()
}
#let section-heading(label) = {
  let info = section-info(label)
  text(size: title-size)[#info.number#h(0.6em)#info.title]
}

#let ai-line = [Transparenzhinweis: Mit Unterstützung von Claude- und
  GPT-Modellen erstellt; Inhalt, Auswahl und fachliche Prüfung verantwortet
  der Autor.]

// Place `body` on the grid: columns c .. c+n-1, `y` below the content top.
#let at(c, n, y: 0mm, body) = place(top + left, dx: col-x(c), dy: y,
  block(width: cols(n), body))

#let page-number = context {
  place(bottom + right, dx: -margin, dy: -furniture-y,
    text(size: small-size, fill: muted, counter(page).display()))
}

// The play mark: a small muted triangle at a fixed place, bottom left in the
// margin, linked to the animation like the poster itself.
#let play-mark(url) = place(bottom + left, dx: margin, dy: -furniture-y,
  link(url, polygon(fill: muted, (0mm, 0mm), (3.2mm, -1.6mm), (0mm, -3.2mm))))

// ---------------------------------------------------------------- pages ---

// One numbered page. With `section` (a script section label) the section
// title sits at the top and the content starts at the title band.
#let slide(section: none, link-to: none, body) = page(
  foreground: {
    page-number
    if link-to != none { play-mark(link-to) }
  },
)[
  #if section != none { place(top + left, section-heading(section)) }
  #let y0 = if section != none { title-band } else { 0mm }
  #place(top + left, dy: y0,
    block(width: text-width, height: text-height - y0, body))
]

// A blank writing page: no number, and it does not advance the page count.
#let blank() = page(foreground: none)[#counter(page).update(n => n - 1)]
#let blanks(n) = range(n).map(_ => blank()).join()

#let title-page(chapter) = page(foreground: none)[
  #let info = chapter-info(chapter)
  #at(1, 9, y: 42mm)[
    #text(fill: muted)[Plasma Physics]
    #v(1.0em)
    #text(fill: muted)[Chapter #chapter]
    #v(1.6em)
    #text(size: title-size)[#info.title]
  ]
  #at(1, 9, y: 112mm)[
    Christopher Albert
    #v(0.5em)
    #text(fill: muted)[TU Graz#h(1.2em)WS 2026/27]
  ]
  #place(bottom + left,
    block(width: cols(8), text(size: small-size, fill: muted, ai-line)))
]

// Deck setup: page geometry, type, document metadata, and the title page.
#let deck(chapter: none, body) = {
  let info = chapter-info(chapter)
  set document(
    title: "Plasma Physics, Chapter " + str(chapter) + ": " + info.title,
    author: "Christopher Albert",
  )
  set page(width: 297mm, height: 210mm, margin: margin, fill: white)
  set text(font: "Libertinus Serif", size: body-size, fill: ink, lang: "en",
    top-edge: "cap-height", bottom-edge: "baseline")
  show math.equation: set text(font: "Libertinus Math")
  set par(leading: 0.62em, spacing: 0.62em)
  title-page(chapter)
  body
}

// An animation poster on the media band, linked to the video; the play mark
// sits at the same place on every linked page. The 16:9 poster spans all
// twelve columns (257 mm x 144.6 mm), within the band's 150 mm height.
#let animation-page(slug, name, section: none) = {
  let url = animation-url(name)
  slide(section: section, link-to: url)[
    #place(top + left, dy: if section == none { title-band } else { 0mm },
      link(url, image(poster-path(slug), width: text-width)))
  ]
}

// A photo on the media band (same place on every photo page) with a small
// credit line under its right edge. `key` labels the page for the credits.
#let photo-page(file, credit, key, section: none) = slide(section: section)[
  #let dy = if section == none { title-band } else { 0mm }
  #place(top + left, dx: col-x(2), dy: dy, stack(spacing: 4.5mm,
    image("/slides/photos/" + file, width: cols(10)),
    align(right, block(width: cols(10), text(size: small-size, fill: muted, credit)))))
  #metadata(file) #label(key)
]

// One derived plot spanning `columns` grid columns, centred on the grid, with
// an optional line of formulas underneath.
#let plot-page(name, columns: 8, section: none, below: none) = slide(section: section)[
  #let start = 1 + int((12 - columns) / 2)
  #at(start, columns)[
    #plot(name, columns: columns)
    #if below != none {
      v(9mm)
      align(center, below)
    }
  ]
]

// Two derived plots side by side, six columns each, with optional muted
// lines naming the symbols of each plot.
#let plot-pair(left, right, section: none, left-caption: none,
  right-caption: none) = slide(section: section)[
  #for (start, name, caption) in ((1, left, left-caption), (7, right, right-caption)) {
    at(start, 6)[
      #plot(name)
      #if caption != none {
        v(4mm, weak: true)
        text(fill: muted, caption)
      }
    ]
  }
]

// A section start without a picture: the title over an empty writing area.
#let section-page(section) = slide(section: section)[]

// --------------------------------------------------------------- summary ---

// Block labels have the body size; small capitals set them apart.
#let block-label(body) = text(tracking: 0.02em, smallcaps(body))
// Step label of a derivation chain: "Gauss ⇒".
#let step(body) = [#body#h(0.3em)#sym.arrow.r.double]
#let label-gap = 5mm
#let row-gap = 7mm

// Rows of (label, formula): labels right-aligned in a column of width `lw`,
// formulas left-aligned from the common axis lw + label-gap. Each row is one
// line, so label and formula share the baseline.
#let rows(items, lw, gap: row-gap) = for (label, formula) in items {
  block(above: gap, below: gap)[
    #box(width: lw, align(right, text(fill: muted, label)))#h(label-gap)#box(formula)
  ]
}
#let label-width(..groups) = calc.max(0pt, ..groups.pos().flatten()
  .chunks(2).map(r => measure(text(fill: muted, r.first())).width))

// The thin-ruled result box: the formula, then its name in muted text.
#let result-box(formula, name) = block(width: 100%,
  stroke: 0.6pt + plot-blue, inset: (x: 6mm, top: 6mm, bottom: 6mm))[
  #set math.equation(numbering: none)
  #show math.equation.where(block: true): set align(left)
  #show math.equation.where(block: true): set block(above: 0pt, below: 0pt)
  #formula
  #if name != none {
    v(4.5mm)
    text(fill: muted, name)
  }
]

#let labelled(title, body) = [
  #block-label(title)
  #v(7mm, weak: true)
  #body
]

// Summary page: Assumptions and Derivation on columns 1-6, Result above the
// plot on columns 7-12. `symbols` names the symbols at first use (muted,
// under the assumptions); `caption` names the plot's own symbols.
#let summary(assumptions: (), symbols: none, derivation: (), result: none,
  result-name: none, plot-name: none, caption: none, below-result: none,
  section: none) = slide(section: section)[
  #context {
    let lw = label-width(assumptions, derivation)
    at(1, 6)[
      #labelled[Assumptions][#rows(assumptions, lw)]
      #if symbols != none {
        v(6mm, weak: true)
        text(fill: muted, symbols)
      }
      #v(15mm, weak: true)
      #labelled[Derivation][#rows(derivation, lw)]
    ]
  }
  #at(7, 6)[
    #labelled[Result][#result-box(result, result-name)]
    #if below-result != none {
      v(6mm, weak: true)
      below-result
    }
    #v(9mm, weak: true)
    #plot(plot-name)
    #if caption != none {
      v(4mm, weak: true)
      text(fill: muted, caption)
    }
  ]
]

// Summary page over a full-width plot: three blocks on columns 1-3, 4-9 and
// 10-12, the plot on all twelve columns at the bottom of the page.
#let summary-wide(assumptions: (), derivation: (), result: none,
  result-name: none, notes: none, derivation-notes: none, plot-name: none) = slide[
  #context {
    // Tighter rows: the blocks share the page with a full-width plot.
    let rows = rows.with(gap: 5mm)
    let lw-a = label-width(assumptions)
    let lw-d = label-width(derivation)
    at(1, 3, labelled[Assumptions][#rows(assumptions, lw-a)])
    at(4, 6)[
      #labelled[Derivation][#rows(derivation, lw-d)]
      #if derivation-notes != none {
        v(6mm, weak: true)
        text(fill: muted, derivation-notes)
      }
    ]
  }
  #at(10, 3)[
    #labelled[Result][#result-box(result, result-name)]
    #if notes != none {
      v(6mm, weak: true)
      text(fill: muted, notes)
    }
  ]
  #place(bottom + left, plot(plot-name, columns: 12))
]

// ---------------------------------------------------------- illustrations ---

// Two Debye spheres of equal radius λ_D holding N_D ≈ 3 and N_D ≈ 300
// electrons: uniform random points in a cube of half-width 1.6 λ_D, in 2-D
// projection. Points inside the sphere are blue; the rest of the plasma is
// grey and drawn only outside the projected disk. For the small sphere the
// draw is repeated until it holds exactly three points, none of them on the
// radius line or its label. Deterministic (linear congruential generator).
#let lcg(s) = calc.rem(s * 1103515245 + 12345, 2147483648)
#let debye-points(n, seed, exact: false) = {
  let half = 1.6
  let count = int(n * calc.pow(2 * half, 3) / (4 * calc.pi / 3))
  let s = seed
  let result = none
  while result == none {
    let points = ()
    for _ in range(count) {
      let p = ()
      for _ in range(3) {
        s = lcg(s)
        p.push((s / 2147483648 * 2 - 1) * half)
      }
      points.push(p)
    }
    let inside = points.filter(p => p.map(x => x * x).sum() < 1)
    let clear = inside.all(p => not (calc.abs(p.at(1)) < 0.2 and p.at(0) > -0.1))
    if not exact or (inside.len() == n and clear) {
      let outside = points.filter(p => p.at(0) * p.at(0) + p.at(1) * p.at(1) > 1)
      result = (inside: inside, outside: outside)
    }
  }
  result
}

#let debye-sphere(n, seed, dot, exact: false) = {
  let size = cols(6)
  let unit = (size - dot) / 3.2
  let pts = debye-points(n, seed, exact: exact)
  let pos(p) = (size / 2 + p.at(0) * unit - dot / 2, size / 2 - p.at(1) * unit - dot / 2)
  block(width: size, height: size)[
    #for p in pts.outside {
      let (x, y) = pos(p)
      place(dx: x, dy: y, circle(radius: dot / 2, fill: rgb("#C8CED6"), stroke: none))
    }
    #for p in pts.inside {
      let (x, y) = pos(p)
      place(dx: x, dy: y, circle(radius: dot / 2, fill: plot-blue, stroke: none))
    }
    #place(dx: size / 2 - unit, dy: size / 2 - unit,
      circle(radius: unit, stroke: 0.9pt + ink))
    #place(dx: size / 2, dy: size / 2, line(length: unit, stroke: 0.7pt + ink))
    #place(dx: size / 2, dy: size / 2 - 8.5mm, box(width: unit,
      align(center, box(fill: white, outset: (x: 1mm, y: 1.5mm), $lambda_D$))))
  ]
}

// The model ladder from particles to magnetohydrodynamics.
#let model-ladder() = {
  let w = cols(4)
  set text(size: body-size)
  diagram(
    spacing: 18mm,
    node-stroke: 0.6pt + ink,
    node-corner-radius: 1.5mm,
    node-inset: 5mm,
    edge-stroke: 0.6pt + ink,
    node((0, 0), [$N$ particles], width: w),
    edge("-|>", text(fill: muted, $chevron.l dot chevron.r$), label-side: left, label-sep: 5mm),
    node((0, 1), $f(bold(x), bold(v), t)$, width: w),
    edge("-|>", text(fill: muted, $integral bold(v)^k f dif^3 v$), label-side: left, label-sep: 5mm),
    node((0, 2), [moments], width: w),
    edge("-|>"),
    node((0, 3), [fluids], width: w),
    edge("-|>", text(fill: muted, $sum_s$), label-side: left, label-sep: 5mm),
    node((0, 4), [magnetohydrodynamics], width: w),
  )
}

// ---------------------------------------------------------------- credits ---

// Credits: one row per photo with the number of its page, then a closing line.
#let credits-page(entries, closing) = slide[
  #at(1, 12, grid(
    columns: (cols(1), 1fr), column-gutter: gutter, row-gutter: 10mm,
    ..for (key, body, source) in entries {
      (
        align(right, text(fill: muted, context counter(page).at(label(key)).first())),
        [#body#v(4mm, weak: true)#text(fill: muted, source)],
      )
    },
    [], block(above: 4mm, closing),
  ))
]
