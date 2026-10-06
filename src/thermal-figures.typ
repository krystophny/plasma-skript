#import "@preview/cetz:0.5.2": canvas, draw
#import "figures.typ": derived-plot
#import "theme.typ": qty

#let slot-standing-wave() = derived-plot("slot_standing_wave", width: 100%)
#let slot-momentum-cutoff() = derived-plot("slot_momentum_cutoff", width: 100%)

#let thermal-table() = context {
  if sys.inputs.at("outline-only", default: "false") != "true" {
    let data = json("/derivations/build/thermal-ionization.json")
    table(columns: 4, align: right, inset: 6pt,
      table.header([$n$ (#qty("1","m^-3"))], [$T_(1/2)$ (K)], [$k_B T_(1/2)$ (eV)], [$chi/(k_B T_(1/2))$ [1]]),
      ..data.rows.map(r => (
        qty("1e" + str(r.exponent), "m^-3"), qty(str(calc.round(r.T)), "K"),
        qty(str(calc.round(r.kT, digits: 3)), "eV"), [#calc.round(r.log, digits: 2)],
      )).flatten(),
    )
  }
}

// Each row is a distinct microstate; filled/open cells encode its binary choices.
#let microstates() = canvas(length: 12mm, {
  import draw: *
  for cells in range(1, 4) {
    let x = (cells - 1) * 4.5
    content((x + 0.55, 1.7), [#cells #if cells == 1 { [cell] } else { [cells] }])
    content((x + 0.55, 0.8), [$W = 2^#cells$ [1]])
    for state in range(calc.pow(2, cells)) {
      for bit in range(cells) {
        let filled = calc.rem(calc.floor(state / calc.pow(2, bit)), 2) == 1
        circle((x + bit * 0.65, -state * 0.65), radius: 0.14,
          fill: if filled { rgb("#0072B2") } else { white }, stroke: 0.6pt)
      }
    }
  }
})
