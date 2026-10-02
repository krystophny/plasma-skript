#import "../theme.typ": *
#import "@preview/physica:0.9.8": div, grad, curl, pdv, laplacian

// The only place in the script where Gaussian CGS units and CGS-form
// equations may appear (SPEC.md, unit-system contract).
#let appendix = [
  #page-title[Appendix: Gaussian CGS translation] <cgs-translation>

  #lead[
    The script uses SI throughout; much of the older plasma literature uses
    Gaussian CGS, and the table below translates the equations and scales
    used in this script from one system to the other.
  ]

  #table(
    columns: (auto, 1fr, 1fr),
    stroke: 0.5pt + muted,
    inset: 0.45em,
    align: left + horizon,
    table.header([Quantity], [SI], [Gaussian CGS]),
    [Coulomb force],
      [$F = q_1 q_2\/(4 pi epsilon_0 r^2)$],
      [$F = q_1 q_2\/r^2$],
    [Poisson equation],
      [$laplacian phi = -rho_q\/epsilon_0$],
      [$laplacian phi = -4 pi rho_q$],
    [Lorentz force],
      [$bold(F) = q (bold(E) + bold(v) times bold(B))$],
      [$bold(F) = q (bold(E) + bold(v) times bold(B)\/c)$],
    [Gauss's law],
      [$div bold(E) = rho_q\/epsilon_0$],
      [$div bold(E) = 4 pi rho_q$],
    [Ampère--Maxwell law],
      [$curl bold(B) = mu_0 bold(j) + mu_0 epsilon_0 pdv(bold(E), t, style: "horizontal")$],
      [$curl bold(B) = (4 pi)/c bold(j) + 1/c pdv(bold(E), t)$],
    [Faraday's law],
      [$curl bold(E) = -pdv(bold(B), t, style: "horizontal")$],
      [$curl bold(E) = -(1\/c) pdv(bold(B), t, style: "horizontal")$],
    [No magnetic monopoles],
      [$div bold(B) = 0$],
      [$div bold(B) = 0$],
    [Debye length],
      [$lambda_D = sqrt(epsilon_0 k_B T_e\/(n e^2))$],
      [$lambda_D = sqrt(k_B T_e\/(4 pi n e^2))$],
    [Electron plasma frequency],
      [$omega_(p e) = sqrt(n e^2\/(epsilon_0 m_e))$],
      [$omega_(p e) = sqrt(4 pi n e^2\/m_e)$],
    [Signed gyrofrequency],
      [$Omega = q B\/m$],
      [$Omega = q B\/(m c)$],
    [Magnetic pressure],
      [$B^2\/(2 mu_0)$],
      [$B^2\/(8 pi)$],
    [Plasma beta],
      [$beta = 2 mu_0 p\/B^2$],
      [$beta = 8 pi p\/B^2$],
    [$bold(E) times bold(B)$ drift],
      [$bold(v)_E = bold(E) times bold(B)\/B^2$],
      [$bold(v)_E = c bold(E) times bold(B)\/B^2$],
    [Magnetic moment of a current loop],
      [$mu = I S$],
      [$mu = I S\/c$],
    [MHD force density],
      [$bold(j) times bold(B)$],
      [$bold(j) times bold(B)\/c$],
    [Magnetic field],
      [$1 "T"$],
      [$10^4 "G"$],
    [Energy],
      [$1 "J"$],
      [$10^7 "erg"$],
    [Number density],
      [$1 thin "m"^(-3)$],
      [$10^(-6) thin "cm"^(-3)$],
    [Charge],
      [$1 "C"$],
      [$approx 2.998 dot 10^9 "statC"$],
    [Electric potential],
      [$1 "V"$],
      [$approx (1\/299.8) "statV"$],
  )

  Purely geometric factors, such as the Debye number
  $N_D = (4 pi\/3) n lambda_D^3$, are identical in both systems. Temperatures
  quoted as $k_B T$ in electronvolts carry the same number in both systems;
  only the conversion to energy differs,

  $ 1 "eV" = 1.602176634 dot 10^(-19) "J" = 1.602176634 dot 10^(-12) "erg" . $
]
