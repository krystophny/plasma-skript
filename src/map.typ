// Map of plasma models. The single source is map/plasma-models.yaml; this
// module turns it into the static overview figure (script chapter 1 and its
// slide) and the interactive page map/index.html (graph drawn by map.js from
// the same data, detail entries typeset here).
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "@preview/physica:0.9.8": grad, div, curl, laplacian, pdv, dv, vb

#let map-data = yaml("/map/plasma-models.yaml")
#let edge-id(e) = e.from + "--" + e.to
#let status-ids = map-data.statuses.map(s => s.id)
#let branch-of = map-data.branches.map(b => (b.id, b)).to-dict()
#let node-of = map-data.nodes.map(n => (n.id, n)).to-dict()
#let course-ids = map-data.courses.keys()
#let kin6d-ids = map-data.at("kin6d-states").map(s => s.id)

// Referential integrity: every edge joins known nodes, every status and
// branch is declared, and every SymPy check named as evidence is a section
// of the cited derivation script. A broken reference fails the build.
#for n in map-data.nodes {
  assert(n.branch in branch-of, message: "map: unknown branch of " + n.id)
  assert(n.status in status-ids, message: "map: unknown status of " + n.id)
}
#for e in map-data.edges {
  assert(e.from in node-of and e.to in node-of,
    message: "map: edge joins unknown node: " + edge-id(e))
  assert(e.status in status-ids, message: "map: unknown status of " + edge-id(e))
}
#for item in map-data.nodes + map-data.edges {
  if "kin6d" in item {
    assert(item.kin6d.state in kin6d-ids,
      message: "map: unknown kin6d state of " + item.at("id", default: item.at("from", default: "") + "--" + item.at("to", default: "")))
  }
}
#for item in map-data.nodes + map-data.edges {
  for (course, refs) in item.at("coverage", default: (:)) {
    assert(course in course-ids, message: "map: unknown course " + course)
  }
  for ev in item.at("evidence", default: ()) {
    if "sympy" in ev {
      let source = read("/" + ev.sympy)
      for check in ev.checks {
        assert(source.contains("section(\"" + check + "\""),
          message: "map: no SymPy section '" + check + "' in " + ev.sympy)
      }
    }
  }
}

#let covers(item, course) = item.at("coverage", default: (:)).at(course, default: ()).len() > 0

// The route of a course: the edges it covers and the nodes it covers or
// reaches through a covered edge.
#let route(course) = {
  let edges = map-data.edges.filter(e => covers(e, course)).map(edge-id)
  let ends = map-data.edges.filter(e => covers(e, course)).map(e => (e.from, e.to)).flatten()
  let nodes = map-data.nodes.filter(n => covers(n, course) or n.id in ends).map(n => n.id)
  (nodes: nodes, edges: edges)
}

// ------------------------------------------------------- static figure
// Layout grid of the figure (mm per unit of `pos`), sized so that the map
// fills an A4-landscape slide at a 9 pt label size; the slide and the
// script scale the figure to the space they have. Nodes are at least
// `map-node-width` wide and grow with a longer label line.
#let map-dx = 23mm
#let map-dy = 14mm
#let map-node-width = 17mm
#let map-inset = 2.4pt
#let checked = ("algebra-checked", "limit-checked", "defect-measured",
  "reproduced", "formally-proved")
// kin6d state marks: filled, half-filled and open circle.
#let kin6d-mark = (implemented: "●", partial: "◐", planned: "○")
#let mark-glyph(state) = text(font: "STIX Two Math", size: 6.5pt,
  fill: rgb("#17202B"), kin6d-mark.at(state))

// One-line legend under the figure: line styles, the course route and the
// kin6d marks.
#let map-legend() = {
  set text(size: 9pt, fill: rgb("#3A4654"))
  let sample(dash) = box(baseline: -0.3em,
    line(length: 7mm, stroke: (paint: rgb("#17202B"), thickness: 0.8pt, dash: dash)))
  let route-box = box(baseline: 0.15em, width: 6mm, height: 0.9em, radius: 1pt,
    stroke: 0.9pt + rgb("#0072B2"), fill: rgb("#0072B2").lighten(86%))
  [#sample(none) checked symbolically #h(5mm) #sample("dashed") stated #h(5mm)
    #route-box route of this course #h(5mm)
    kin6d: #mark-glyph("implemented") implemented #h(2mm) #mark-glyph("partial") partial
    #h(2mm) #mark-glyph("planned") planned]
}

#let model-map-diagram(course: "plasma") = context {
  let on = route(course)
  let at(p) = (p.at(0) * map-dx, -p.at(1) * map-dy)
  set text(font: "STIX Two Text", size: 9pt, fill: rgb("#17202B"))
  let width-of(label) = calc.max(map-node-width / 1mm,
    calc.max(..label.split("\n").map(l => measure(text(font: "STIX Two Text", size: 9pt, l)).width / 1mm)) + 2 * map-inset / 1mm + 0.9) * 1mm
  diagram(
    node-inset: map-inset,
    node-corner-radius: 2pt,
    spacing: 0pt,
    // Branch names; a name longer than 40 mm breaks into two balanced lines
    // so that it fits between the boxes.
    ..map-data.branches.map(b => node(at(b.tag),
      block(width: {
        let w = measure(text(size: 9.5pt, smallcaps(b.name))).width / 1mm + 0.5
        (if w > 40 { w / 2 + 5 } else { w }) * 1mm
      },
        align(center, par(justify: false, leading: 0.35em, text(size: 9.5pt, fill: rgb(b.color), smallcaps(b.name))))),
      // A card-coloured ground hides an edge that has to pass under a name.
      stroke: none, fill: rgb("#fefefd"), inset: 0.8pt)),
    // The legend line, centred one row below the lowest box.
    {
      let xs = map-data.nodes.map(n => n.pos.at(0))
      let ymax = calc.max(..map-data.nodes.map(n => n.pos.at(1)))
      node(at(((calc.min(..xs) + calc.max(..xs)) / 2, ymax + 0.95)), map-legend(),
        stroke: none, fill: none, inset: 0pt)
    },
    ..map-data.nodes.map(n => {
      let color = rgb(branch-of.at(n.branch).color)
      let lit = n.id in on.nodes
      let mark = if "kin6d" in n {
        place(top + right, dx: map-inset + 0.6mm, dy: -map-inset - 1.1mm, mark-glyph(n.kin6d.state))
      }
      node(at(n.pos),
        [#mark#text(fill: if lit { rgb("#17202B") } else { luma(45%) },
          weight: if lit { "medium" } else { "regular" },
          n.label.split("\n").join(linebreak()))],
        name: label("map-" + n.id),
        width: width-of(n.label),
        stroke: if lit { 0.9pt + color } else { 0.55pt + color.lighten(45%) },
        fill: if lit { color.lighten(86%) } else { rgb("#fffffe") },
      )
    }),
    ..map-data.edges.map(e => {
      let lit = edge-id(e) in on.edges
      let dash = if e.status in checked { none } else { "dashed" }
      // Optional waypoints `via` route an edge around the boxes between
      // its ends.
      edge(label("map-" + e.from), ..e.at("via", default: ()).map(at),
        label("map-" + e.to), "-|>", corner-radius: 4pt,
        stroke: (paint: if lit { rgb("#17202B") } else { luma(66%) },
          thickness: if lit { 0.8pt } else { 0.5pt }, dash: dash))
    }),
  )
}

// The map scaled to fit a box of the given size (aspect ratio kept).
#let model-map-fit(width, height, course: "plasma") = context {
  let fig = model-map-diagram(course: course)
  let s = measure(fig)
  let k = calc.min(width / s.width, height / s.height)
  scale(k * 100%, reflow: true, fig)
}

// Script figure (chapter 1). The SVG keeps its own light card in both site
// themes: its ink and fills avoid the colours that the build recolours for
// dark mode (scripts/prepare-media.py), so the route stays legible.
#let map-alt = "A layered graph of about sixty-five plasma models. Quantum many-body models are on the left, classical many-body and kinetic models in the middle, magnetized orbit and kinetic models on the right, radiation, reaction and neutral-particle models on the right, and fluid, MHD, wave and equilibrium models at the bottom. Small circles mark the state of the research code kin6d. Arrows point from a parent model to a reduced model. The route of this course is highlighted: particles and fields lead to single-particle orbits and guiding-center drifts, to the Vlasov equation, to moments, multiple-fluid theory and MHD, to collisions and resistivity, and to waves, Landau damping and sheaths. Other models are drawn as lighter, unfilled boxes."

// Link to the interactive map with a course route highlighted: relative on
// the site, absolute in the print PDF and on slides.
#let map-link(body, course: "plasma", absolute: false) = context {
  let path = "map/index.html?course=" + course
  link(if absolute or target() == "paged" { map-data.site + path } else { "../" + path }, body)
}

#let model-map-figure() = context {
  let caption = [
    Map of plasma models, from first principles at the top to reduced
    models at the bottom. Highlighted boxes and arrows form the route of
    this course; solid arrows are reductions whose algebra is checked in the
    SymPy derivations of the script, dashed arrows are stated only. Small
    circles mark the state of the research code kin6d: filled implemented,
    half filled partially implemented, open planned.
    #map-link[Open the interactive map] for the equations, assumptions
    and evidence of every model and reduction.
  ]
  if target() == "paged" {
    figure(alt: map-alt, caption: caption,
      layout(size => model-map-fit(size.width, 10 * size.width)))
  } else {
    html.figure(class: "concept-figure model-map-figure")[
      // Scale the SVG (inline em size from Typst) to the column width.
      #html.style(".model-map-link { display: block; } .model-map-card svg { display: block; width: 100% !important; height: auto !important; }")
      #html.a(href: "../map/index.html?course=plasma", class: "model-map-link",
        aria-label: "Map of plasma models; opens the interactive map")[
        #html.div(class: "model-map-card", role: "img", aria-label: map-alt)[
          #html.frame(block(fill: rgb("#fdfdfb"), inset: 4mm, model-map-diagram()))
        ]
      ]
      #html.figcaption(caption)
    ]
  }
}

// ------------------------------------------------------ interactive page
#let math-scope = (grad: grad, div: div, curl: curl, laplacian: laplacian,
  pdv: pdv, dv: dv, vb: vb, hbar: sym.planck)
#let show-math(s) = math.equation(block: true, eval(s, mode: "math", scope: math-scope))
#let show-text(s) = eval(s, mode: "markup", scope: math-scope)
#let status-name = map-data.statuses.map(s => (s.id, s.name)).to-dict()

// Section labels of the script resolve to "§N.M Title" with a link.
#let section-ref(name) = context {
  let found = query(<script-section>).filter(m => m.value.label == name)
  if found.len() == 0 { return raw(name) }
  let s = found.first().value
  // Link to the stable section id; a label that the script uses twice
  // falls back to the location of the section's metadata.
  let target = if query(label(name)).len() == 1 { label(name) } else { found.first().location() }
  link(target)[§#s.number #s.title]
}

#let coverage-list(item) = {
  let cov = item.at("coverage", default: (:))
  let rows = ()
  for (course, refs) in cov {
    let info = map-data.courses.at(course)
    let units = info.at("units", default: (:))
    let shown = if course == "plasma" { refs.map(section-ref) }
      else { refs.map(r => if r in units [#r #units.at(r)] else [#r]) }
    rows.push(html.li[#html.strong(info.name): #shown.join("; ")])
  }
  if rows.len() > 0 { html.ul(class: "map-coverage", rows.join()) } else [none]
}

#let evidence-list(item) = {
  let ev = item.at("evidence", default: ())
  if ev.len() == 0 { return [none listed] }
  html.ul(class: "map-evidence", ev.map(e => {
    if "sympy" in e {
      html.li[SymPy #link(map-data.repository + e.sympy)[#raw(e.sympy)]: #e.checks.join("; ")]
    } else {
      html.li[Literature: #e.literature]
    }
  }).join())
}

#let field(term, body) = html.div(class: "map-field")[#html.dt(term)#html.dd(body)]
// kin6d state of a node or edge: state, note and the kin6d document named
// as plain text (private repository, no link).
#let kin6d-field(item) = if "kin6d" in item {
  let k = item.kin6d
  field[kin6d][#html.strong(k.state): #show-text(k.note) (#raw(k.ref))]
}
#let anchor(id, body) = html.a(href: "#" + id, body)

#let node-entry(n) = {
  let ins = map-data.edges.filter(e => e.to == n.id)
  let outs = map-data.edges.filter(e => e.from == n.id)
  let edge-links(es, end) = if es.len() == 0 [none] else {
    es.map(e => anchor("edge-" + edge-id(e), node-of.at(e.at(end)).name)).join(", ")
  }
  html.article(id: "node-" + n.id, class: "map-entry map-branch-" + n.branch)[
    #html.h3(n.name)
    #html.p(class: "map-meta")[#branch-of.at(n.branch).name · status: #html.span(class: "map-status")[#status-name.at(n.status)]]
    #html.p(show-text(n.summary))
    #for eq in n.at("equations", default: ()) { show-math(eq) }
    #html.dl[
      #field[State][#show-text(n.state)]
      #field[Structure][#show-text(n.structure)]
      #field[Solution concept][#show-text(n.solution)]
      #field[Courses][#coverage-list(n)]
      #field[Evidence][#evidence-list(n)]
      #kin6d-field(n)
      #field[Reduced from][#edge-links(ins, "from")]
      #field[Reduces to][#edge-links(outs, "to")]
    ]
  ]
}

#let edge-entry(e) = {
  let a = node-of.at(e.from)
  let b = node-of.at(e.to)
  html.article(id: "edge-" + edge-id(e), class: "map-entry map-edge-entry")[
    #html.h3[#a.name → #b.name]
    #html.p(class: "map-meta")[Reduction · #e.method · status: #html.span(class: "map-status")[#status-name.at(e.status)]]
    #if "small" in e [#html.p[Small parameters and ordering:] #show-math(e.small)]
    #html.dl[
      #field[Assumptions][#html.ul(e.assumptions.map(x => html.li(show-text(x))).join())]
      #field[Lost][#show-text(e.lost)]
      #field[Courses][#coverage-list(e)]
      #field[Evidence][#evidence-list(e)]
      #kin6d-field(e)
      #field[Models][#anchor("node-" + a.id, a.name) → #anchor("node-" + b.id, b.name)]
    ]
  ]
}

// Data for map.js: geometry, branches, statuses and course coverage only;
// the readable content stays in the typeset entries below.
#let map-json = json.encode(pretty: false, (
  branches: map-data.branches.map(b => (id: b.id, name: b.name, tag: b.tag)),
  statuses: status-ids,
  courses: course-ids.map(c => (id: c, name: map-data.courses.at(c).name)),
  nodes: map-data.nodes.map(n => (id: n.id, name: n.name, label: n.label,
    branch: n.branch, pos: n.pos, status: n.status,
    courses: course-ids.filter(c => covers(n, c)))),
  edges: map-data.edges.map(e => (id: edge-id(e), from: e.from, to: e.to,
    via: e.at("via", default: ()),
    status: e.status, courses: course-ids.filter(c => covers(e, c)))),
))

#let branch-css = {
  let light = map-data.branches.map(b => ".map-branch-" + b.id + " { --branch: " + b.color + "; }").join("\n")
  let dark = map-data.branches.map(b => ".map-branch-" + b.id + " { --branch: " + b.dark + "; }").join("\n")
  light + "\n@media (prefers-color-scheme: dark) {\n" + dark + "\n}"
}

#let status-sample(id) = html.elem("svg", attrs: (class: "map-status-sample status-" + id,
  viewBox: "0 0 36 8", width: "36", height: "8", "aria-hidden": "true"),
  html.elem("line", attrs: (x1: "1", y1: "4", x2: "35", y2: "4")))

#let model-map-page() = {
  // Script section labels are checked against the outline that the
  // derivations build writes (scripts/script-outline.sh) before the site is
  // compiled; the print and outline compilations never reach this page.
  let sections = json("/slides/build/script-outline.json").sections.map(s => s.label)
  for item in map-data.nodes + map-data.edges {
    for name in item.at("coverage", default: (:)).at("plasma", default: ()) {
      assert(name in sections, message: "map: unknown script section " + name)
    }
  }
  html.h1[Map of plasma models]
  html.p(class: "map-intro")[
    Each box is a model and each arrow a reduction from a more fundamental
    model, with first principles at the top. Select a model or an arrow to
    see its equations, assumptions, the courses that teach it and the
    evidence behind it. A course filter highlights the route that course
    takes through the map. The same data drive the overview figure in
    #link(label("intro-model-hierarchy"))[chapter 1] and are shared with
    the Fusion Physics and Kinetic Theory courses and the research theory map.
  ]
  html.style(branch-css)
  html.div(class: "model-map", id: "model-map")[
    #html.div(class: "map-toolbar", role: "toolbar", aria-label: "Map controls")[
      #html.div(class: "map-courses", role: "group", aria-label: "Highlight a course route")[
        #html.elem("button", attrs: (type: "button", "data-course": "", "aria-pressed": "true"))[All]
        #for c in course-ids {
          html.elem("button", attrs: (type: "button", "data-course": c, "aria-pressed": "false"))[#map-data.courses.at(c).name]
        }
      ]
      #html.div(class: "map-zoom", role: "group", aria-label: "Zoom")[
        #html.elem("button", attrs: (type: "button", "data-zoom": "in", aria-label: "Zoom in"))[+]
        #html.elem("button", attrs: (type: "button", "data-zoom": "out", aria-label: "Zoom out"))[−]
        #html.elem("button", attrs: (type: "button", "data-zoom": "reset"))[Fit]
      ]
    ]
    #html.div(class: "map-stage", id: "map-stage")[
      #html.div(class: "map-static model-map-card", role: "img", aria-label: map-alt)[
        #html.frame(block(fill: rgb("#fdfdfb"), inset: 4mm, model-map-diagram(course: "plasma")))
      ]
    ]
    #html.aside(class: "map-panel", id: "map-panel", aria-live: "polite")[
      #html.p(class: "map-panel-hint")[Select a model or a reduction.]
    ]
    #html.div(class: "map-legend")[
      #html.div(class: "map-legend-group")[
        #html.h2[Branches]
        #html.ul(map-data.branches.map(b => html.li(class: "map-branch-" + b.id)[#html.span(class: "map-swatch")[]#b.name]).join())
      ]
      #html.div(class: "map-legend-group")[
        #html.h2[Status of a model or reduction]
        #html.ol(class: "map-ladder", map-data.statuses.map(s => html.li[#status-sample(s.id)#html.strong(s.name): #s.text]).join())
      ]
      #html.div(class: "map-legend-group")[
        #html.h2[State in the research code kin6d]
        #html.ul(map-data.at("kin6d-states").map(s => html.li[#kin6d-mark.at(s.id) #html.strong(s.name): #s.text]).join())
      ]
    ]
  ]
  html.section(class: "map-entries", id: "map-entries")[
    #html.h2[Models]
    #for n in map-data.nodes { node-entry(n) }
    #html.h2[Reductions]
    #for e in map-data.edges { edge-entry(e) }
  ]
  html.elem("script", attrs: (type: "application/json", id: "map-data"), map-json)
  html.elem("script", attrs: (src: "map.js", defer: "true"))
}
