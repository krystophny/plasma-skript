# Map of plasma models

`plasma-models.yaml` is the registry of plasma models (nodes) and the
reductions between them (edges) for the Plasma Physics, Fusion Physics and
Kinetic Theory courses and for the research theory map. It is the only source
of the map. `src/map.typ` reads it and produces

- the interactive page `map/index.html` of the site (graph drawn by
  `src/map.js`, styles in `src/map.css`, entries typeset by Typst),
- the static overview figure in chapter 1 of the script
  (`model-map-figure`), and
- the same figure as a full slide in `slides/01-introduction.typ`
  (`model-map-diagram`), with the route of this course highlighted.

The site build (`scripts/build-site.sh`) checks the registry: an edge to an
unknown node, an unknown status, branch, course or script section, or a SymPy
check name that is not a `section("...")` of the cited derivation script
stops the build.

## Schema

Top level: `schema` (version), `site` and `repository` (base URLs for
absolute map links and for evidence links), `statuses`, `kin6d-states`,
`branches`, `courses`, `nodes`, `edges`.

Node:

| key | content |
|---|---|
| `id` | stable identifier, lowercase with hyphens; never renamed once used |
| `name`, `label` | full name; short graph label, `\n` breaks the line |
| `branch` | one of `branches` (colour and region of the graph) |
| `pos` | `[column, row]` in the shared layout (quarter steps); row 0 holds the first principles, rows grow toward reduced models; keep boxes apart and arrows clear of other boxes (use `via` where a straight arrow would cross one) |
| `summary` | one or two sentences |
| `equations` | list of Typst math strings |
| `state`, `structure`, `solution` | state variables; invariants and structure; notion of solution |
| `status` | one of `statuses` for the equations shown |
| `coverage` | optional, see below |
| `evidence` | optional, see below |
| `kin6d` | optional, see below |

Edge: `from`, `to` (node ids; the edge id is `<from>--<to>`), `method`,
`small` (Typst math: small parameters and ordering; omitted for exact steps),
`assumptions` (list), `lost` (what the reduction drops), `status`,
`coverage`, `evidence`, optional `kin6d`, and optional `via`: a list of
`[column, row]` waypoints that route the arrow around boxes in the figure
and on the interactive page.

Text fields are Typst markup, so `$...$` is inline math. Equations are Typst
math with the `physica` operators `pdv`, `dv`, `grad`, `div`, `curl`,
`laplacian`, `vb` and `hbar` in scope. Write a prime as `^prime` (a single
quote ends a YAML string), group subscripts as `f_(s)` and parenthesize
fractions as in the script (`SPEC.md`). Quote a list item that contains a
comma.

### Status ladder

The ladder of the research theory map, weakest first: `stated`,
`algebra-checked`, `limit-checked`, `defect-measured`, `literature-intake`,
`reproduced`, `formally-proved`, plus `open-problem` and `erratum`. A status
names what the public evidence of the entry supports. `algebra-checked` and
`limit-checked` require a SymPy script in `evidence`; `literature-intake`
requires the cited theorem; `open-problem` marks a step without a known
rigorous justification even when its formal derivation is standard.
Research results that are not public (for example a defect measured by a
private code) stay in `coverage.research` as text and do not raise the
public status.

### kin6d state

`kin6d: {state, note, ref}` records how far the research code kin6d
implements a model or reduction: `state` is one of `kin6d-states`
(`implemented`, `partial`, `planned`), `note` names the case and the
evidence label kin6d itself gives it (certified, reference comparison,
candidate, ...), and `ref` names the kin6d document as plain text. kin6d
is private: `ref` is never a link, and the state never raises the public
`status`. The static figure marks the state with a filled, half-filled or
open circle; the interactive page shows the note.

### Coverage

`coverage` maps a course to the parts that teach the node or take the edge:

- `plasma`: section labels of this script (`kinetic-boltzmann`), shown as
  "§N.M The Boltzmann and Vlasov equations" with a link;
- `fusion`: blocks of the Fusion Physics plan (`B2`), named in
  `courses.fusion.units`;
- `kinetic`: chapters (`N2.2`) and dated lectures (`L4`) of the Kinetic
  Theory course, named in `courses.kinetic.units`;
- `research`: free text such as `kin6d`, `NEO-2`, `SIMPLE`. Never a link into
  a private repository.

A course route is the set of edges with that course plus every node that the
course covers or that such an edge touches. The course filter of the page and
the highlighted route of the figures use this rule.

### Evidence

A list of

- `{sympy: derivations/chapters/chNN_*.py, checks: [section titles]}`: the
  SymPy checks of this repository, linked on GitHub;
- `{literature: "Author, Journal volume, page (year)"}`: a public source.

## Referencing ids from elsewhere

The ids are the interface. A course or code refers to a model as
`map/index.html#node-<id>` and to a reduction as
`map/index.html#edge-<from>--<to>`; `?course=plasma|fusion|kinetic|research`
opens the page with that route highlighted, for example
`https://krystophny.github.io/plasma-skript/map/index.html?course=kinetic#node-landau`.

- The Fusion Physics script and the Kinetic Theory course add their section
  or lecture references under `coverage.fusion` and `coverage.kinetic` here,
  using the block and lecture ids listed in `courses`. Adding a new course
  means a new entry under `courses` and its key in `coverage`.
- The research theory map (kin6d) does not copy this file. Its claims,
  FortSym derivations, proofs and defect experiments attach to the same node
  and edge ids; this file records only the public text in
  `coverage.research`.

## Adding an edge with evidence

1. Add the parent and child nodes if they are missing, with a `pos` that
   keeps first principles above reduced models; check the figure by building
   the slides (`scripts/build-slides.sh`) or the site.
2. Add the edge with `method`, `small`, `assumptions`, `lost` and
   `status: stated`.
3. Write the SymPy check in `derivations/chapters/chNN_*.py` as a
   `section("<title>", script="<label>")` that verifies the step
   (`make -C derivations test`).
4. Cite it under `evidence` with the exact section title and raise the
   status to `algebra-checked` (or `limit-checked` for a reproduced limit).
5. Tag the courses that take the step under `coverage` and build the site;
   the build rejects a wrong section title or label.
