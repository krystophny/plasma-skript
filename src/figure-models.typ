// Pure normalized models shared by figures and independent physics checks.
// All arguments and return values use unit [1]. See each figure's caption
// for the dimensional reference scales and approximation regime.
#let maxwellian(x, drift: 0) = calc.exp(-calc.pow(x - drift, 2))
#let diffusion(x, tau) = calc.exp(-x*x/(4*tau))/calc.sqrt(tau)
#let cross-field(x) = 1/(1+x*x)
#let classical(b) = 1/(b*b)
#let bohm(b) = 1/b
#let cold-em(k) = calc.sqrt(1+k*k)
#let circular-index(w, y: 0.3, sense: 1) = calc.sqrt(calc.max(0, 1 - 1/(w*(w + sense*y))))
#let circular-cutoff(y: 0.3, sense: 1) = (calc.sqrt(y*y+4) - sense*y)/2
#let ion-rh(k) = (k*k+calc.sqrt(k*k*k*k+4*k*k))/2
#let ion-lh(k) = (calc.sqrt(k*k*k*k+4*k*k)-k*k)/2
#let warm-electron(k) = calc.sqrt(1+k*k)
#let ion-acoustic(k) = k/calc.sqrt(1836*(1+k*k))
#let bohm-gross(k) = calc.sqrt(1+3*k*k)
#let bump(v) = 0.9*maxwellian(v)+0.2*calc.exp(-4*calc.pow(v - 2, 2))
#let two-stream(k) = calc.sqrt(calc.max(0, (calc.sqrt(1+8*k*k)-1-2*k*k)/2))
#let sheath-barrier(x) = 2.8*calc.pow(1-x/6, 2)
#let sheath-electron(x) = calc.exp(-sheath-barrier(x))
#let sheath-ion(x) = 1/calc.sqrt(1+2*sheath-barrier(x))
#let probe(u) = 0.058-calc.exp(calc.min(u, 0))
#let sphere-bare(r, a: 0.5) = if r <= a { (3-r*r/(a*a))/(2*a) } else { 1/r }
#let sphere-screened(r, a: 0.5) = {
  let sinhc = if r == 0 { 1 } else { calc.sinh(r)/r }
  if r <= a { 3/(a*a*a)*(1-(a+1)*calc.exp(-a)*sinhc) }
  else { 3/(a*a*a)*(a*calc.cosh(a)-calc.sinh(a))*calc.exp(-r)/r }
}
