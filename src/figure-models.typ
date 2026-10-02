// Pure normalized models shared by figures and independent physics checks.
// All arguments and return values use unit [1]. See each figure's caption
// for the dimensional reference scales and approximation regime.
#let maxwellian(x, drift: 0) = calc.exp(-calc.pow(x - drift, 2))
#let bump(v) = 0.9*maxwellian(v)+0.2*calc.exp(-4*calc.pow(v - 2, 2))
