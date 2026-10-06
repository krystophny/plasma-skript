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

// The wave dispersion, sheath and probe curves of chapters 11-15 are plotted
// from the SymPy derivations (derivations/chapters/ch11-ch15), whose tests
// check them.
#let h = 1e-5
// The marked phase velocity 1.7 lies on the clearly rising side of the
// bump: its slope exceeds 0.1 there, while 1.5 is almost the local minimum.
#assert((m.bump(1.7+h)-m.bump(1.7-h))/(2*h) > 0.1)
#assert(calc.abs((m.bump(1.5+h)-m.bump(1.5-h))/(2*h)) < 0.02)
#assert((m.maxwellian(1.7+h)-m.maxwellian(1.7-h))/(2*h) < 0)
#near(integrate(m.bump, -8, 8), calc.sqrt(calc.pi))

// The Debye-sphere potentials are plotted from the SymPy derivation
// (derivations/chapters/ch03_debye_shielding.py), whose tests check them.
#metadata("passed") <physics-check>
