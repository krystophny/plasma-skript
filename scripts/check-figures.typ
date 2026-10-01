#import "../src/figure-models.typ" as m
#let near(a, b, tol: 1e-8) = assert(calc.abs(a - b) < tol)
#let integrate(f, lo, hi, n: 4000) = {
  let dx = (hi - lo)/n
  range(n).map(i => f(lo+(i+0.5)*dx)*dx).sum()
}

// Independent moment and conservation checks, not copied sample arrays.
#near(m.maxwellian(1), 0.3678794411714423)
#near(m.maxwellian(2), 0.01831563888873418)
#near(integrate(x => m.maxwellian(x), -8, 8), calc.sqrt(calc.pi))
#near(integrate(x => x*x*m.maxwellian(x), -8, 8)/calc.sqrt(calc.pi), 0.5)
#for t in (1, 4) {
  let mass = integrate(x => m.diffusion(x, t), -24, 24)
  near(mass, 2*calc.sqrt(calc.pi))
  near(integrate(x => x*m.diffusion(x, t), -24, 24), 0)
  near(integrate(x => x*x*m.diffusion(x, t), -24, 24)/mass, 2*t)
}
#near(m.diffusion(0, 4)/m.diffusion(0, 1), 0.5)
#near(m.cross-field(1), 0.5)
#near(m.classical(2), 0.25)
#near(m.bohm(2), 0.5)

// Substitute the plotted roots into independently written dispersion laws.
#for k in (0.1, 0.2, 0.4, 0.8, 1) {
  let rh = m.ion-rh(k)
  let lh = m.ion-lh(k)
  near(rh*rh/(1+rh), k*k)
  near(lh*lh/(1 - lh), k*k)
  assert(rh > k and lh < k)
  let w2 = -calc.pow(m.two-stream(k), 2)
  near(w2*w2 - (1+2*k*k)*w2+k*k*(k*k - 1), 0)
  near(calc.pow(m.cold-em(k), 2)-k*k, 1)
}
#near(m.ion-rh(1), (1+calc.sqrt(5))/2)
#near(m.two-stream(0), 0)
#near(m.two-stream(1), 0)
#near(m.two-stream(calc.sqrt(3/8)), 1/(2*calc.sqrt(2)))
#for k in range(101).map(i => i/100) {
  assert(m.two-stream(k) <= 1/(2*calc.sqrt(2))+1e-12)
}
#for sense in (-1, 1) {
  let w = m.circular-cutoff(sense: sense)
  near(w*(w+sense*0.3), 1)
  let n = m.circular-index(2, sense: sense)
  near(1-n*n, 1/(2*(2+sense*0.3)))
}
#let h = 1e-5
// The marked phase velocity 1.7 lies on the clearly rising side of the
// bump: its slope exceeds 0.1 there, while 1.5 is almost the local minimum.
#assert((m.bump(1.7+h)-m.bump(1.7-h))/(2*h) > 0.1)
#assert(calc.abs((m.bump(1.5+h)-m.bump(1.5-h))/(2*h)) < 0.02)
#assert((m.maxwellian(1.7+h)-m.maxwellian(1.7-h))/(2*h) < 0)
#near(integrate(m.bump, -8, 8), calc.sqrt(calc.pi))

// Screened-sphere matching, Poisson operator, and large-radius limit.
#let a = 0.5
#near(m.sphere-screened(a - h), m.sphere-screened(a+h), tol: 1e-4)
#near((m.sphere-screened(a)-m.sphere-screened(a - h))/h,
  (m.sphere-screened(a+h)-m.sphere-screened(a))/h, tol: 1e-3)
#for r in (0.2, 0.8) {
  let f = m.sphere-screened(r)
  let radial = ((m.sphere-screened(r+h)-2*f+m.sphere-screened(r - h))/(h*h)
    + (m.sphere-screened(r+h)-m.sphere-screened(r - h))/(h*r)-f)
  near(radial, if r < a { -3/(a*a*a) } else { 0 }, tol: 1e-3)
}
#near(m.sphere-bare(0), 3)
#near(m.sphere-bare(2), 0.5)
#near(m.probe(-h), m.probe(h), tol: 2e-5)
#near(m.probe(0), -0.942)
// Ion-to-electron edge flux ratio sqrt(2 pi m_e/m_i) for hydrogen and the
// labelled floating value u_f = ln 0.058.
#near(0.058, calc.sqrt(2*calc.pi/1836), tol: 5e-4)
#near(m.probe(calc.ln(0.058)), 0, tol: 1e-12)
#near(calc.ln(0.058), -2.847, tol: 1e-3)
#near(m.sheath-electron(6), 1)
#near(m.sheath-ion(6), 1)
#metadata("passed") <physics-check>
