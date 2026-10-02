"""An electron characteristic in a prescribed traveling electrostatic wave.

X=x/L0, V=v/v0, tau=t v0/L0; dX/dtau=V,
dV/dtau=-A sin(K(X-Vphi tau)). A=0.18, K=1, Vphi=0.92.
E/(me v0²/(e L0))=A sin(K(X-Vphi tau)); no wave feedback or damping
is simulated. The left panel is the wave frame (X-Vphi tau,V-Vphi).
Its invariant is (V-Vphi)^2/2-(A/K) cos(K(X-Vphi tau)); the faint curves
are exact level sets of it, the dashed curve is the separatrix
u=±sqrt(2A(1+cos xi)), and the electron completes one closed (trapped)
bounce orbit, tau = 0 ... 17.25.  Upper half (u>0) moves to +xi, so trapped
orbits circulate clockwise.
The right Maxwellian f0 v0/n0=exp(-V²)/sqrt(pi) explains the ensemble
slope criterion for a weak positive-phase-velocity Langmuir wave.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, BG, CURVE_WIDTH, EASE, ELECTRON, FAINT, INK, LINEAR, MUTED, SMALL_SIZE,
    THIN_WIDTH, StyledScene, axes, axis_labels, label, math,
)


def landau_rhs(tau, state, amplitude=0.18, wave_number=1.0, phase_speed=0.92):
    x, v = state
    return np.array([v, -amplitude * np.sin(wave_number * (x - phase_speed * tau))])


def integrate_landau(duration=12.0, dt=0.01, x0=-1.4, v0=1.12,
                     amplitude=0.18, wave_number=1.0, phase_speed=0.92):
    """Return times and (X,V) samples of the actual lab-frame characteristic (RK4)."""
    if duration <= 0 or dt <= 0:
        raise ValueError("duration and dt must be positive")
    times = np.linspace(0, duration, int(np.ceil(duration / dt)) + 1)
    states = np.empty((len(times), 2))
    states[0] = [x0, v0]
    h = times[1] - times[0]
    for i, t in enumerate(times[:-1]):
        state = states[i]
        k1 = landau_rhs(t, state, amplitude, wave_number, phase_speed)
        k2 = landau_rhs(t + h/2, state + h*k1/2, amplitude, wave_number, phase_speed)
        k3 = landau_rhs(t + h/2, state + h*k2/2, amplitude, wave_number, phase_speed)
        k4 = landau_rhs(t + h, state + h*k3, amplitude, wave_number, phase_speed)
        states[i+1] = state + h*(k1 + 2*k2 + 2*k3 + k4)/6
    return times, states


def wave_frame_invariant(xi, u, amplitude=0.18, wave_number=1.0):
    """Invariant u^2/2 - (A/K) cos(K xi) in the wave frame xi = X - Vphi tau."""
    return u * u / 2 - amplitude / wave_number * np.cos(wave_number * xi)


BOUNCE_TIME = 17.25  # one closed trapped orbit for the default initial state


class LandauResonance(StyledScene):
    """Show a resonant particle and the slope of an equilibrium distribution."""

    def build(self):

        # Left: wave-frame phase plane.
        ph = axes([-3.6, 3.6, 1], [-1.0, 1.0, 0.5], 6.9, 4.4).move_to([-2.95, 0.0, 0])
        ph_labels = axis_labels(ph, r"\xi=(x-v_\varphi t)/L_0\ [1]",
                                r"u=(v-v_\varphi)/v_0\ [1]")
        ph_labels[0].next_to(ph, DOWN, buff=0.15).align_to(ph, RIGHT)

        def contour(energy, sign, color, width, opacity):
            # u(xi) on the invariant level set, where real.
            def u_of(x):
                return sign * np.sqrt(max(2 * (energy + 0.18 * np.cos(x)), 0.0))
            if energy < 0.18:
                xmax = np.arccos(-energy / 0.18)
                rng = [-xmax, xmax]
            else:
                rng = [-3.6, 3.6]
            return ph.plot(u_of, x_range=rng + [0.01], color=color,
                           stroke_width=width, stroke_opacity=opacity)

        family = VGroup()
        for energy in (-0.12, -0.05, 0.3, 0.42):
            for sign in (1, -1):
                family.add(contour(energy, sign, FAINT, 1.4, 0.7))
        separatrix = VGroup(*[
            DashedVMobject(ph.plot(lambda x, s=s: s * np.sqrt(0.36 * (1 + np.cos(x))),
                                   x_range=[-PI, PI], color=MUTED, stroke_width=THIN_WIDTH),
                           num_dashes=36)
            for s in (1, -1)
        ])

        times, states = integrate_landau(duration=BOUNCE_TIME, dt=0.01)
        xi = states[:, 0] - 0.92 * times
        u = states[:, 1] - 0.92
        tracker = ValueTracker(0.0)

        def point_at(t):
            return ph.c2p(np.interp(t, times, xi), np.interp(t, times, u))

        def orbit():
            n = max(2, int(np.searchsorted(times, tracker.get_value())))
            pts = [ph.c2p(a, b) for a, b in zip(xi[:n:4], u[:n:4])]
            pts.append(point_at(tracker.get_value()))
            return VMobject(stroke_color=ELECTRON, stroke_width=CURVE_WIDTH - 0.5).set_points_smoothly(pts)

        trail = always_redraw(orbit)
        electron = always_redraw(lambda: Dot(point_at(tracker.get_value()), radius=0.11, color=ELECTRON))
        trapped = label("trapped", color=MUTED, size=SMALL_SIZE).move_to(ph.c2p(0, -0.11))
        trapped = VGroup(BackgroundRectangle(trapped, color=BG, fill_opacity=1, buff=0.04), trapped)
        passing = label("passing", color=MUTED, size=SMALL_SIZE).next_to(ph.c2p(2.3, 0.88), UP, buff=0.05)

        # Right: Maxwellian marginal and its slope at the phase velocity.
        fx = axes([-2.4, 2.4, 1], [0, 0.65, 0.2], 4.4, 4.4).move_to([4.05, 0.0, 0])
        fx_labels = axis_labels(fx, r"v/v_0\ [1]", r"f_0 v_0/n_0\ [1]")
        v_phi = 0.92
        f0 = lambda v: np.exp(-v * v) / np.sqrt(np.pi)
        maxwellian = fx.plot(f0, x_range=[-2.4, 2.4], color=INK, stroke_width=CURVE_WIDTH - 1)
        res_line = DashedLine(fx.c2p(v_phi, 0), fx.c2p(v_phi, 0.6), color=ACCENT,
                              stroke_width=THIN_WIDTH, dash_length=0.1)
        res_label = math(r"v_\varphi", color=ACCENT, size=32).next_to(res_line, UP, buff=0.1)
        slope = -2 * v_phi * f0(v_phi)
        tangent = Line(fx.c2p(v_phi - 0.55, f0(v_phi) - 0.55 * slope),
                       fx.c2p(v_phi + 0.55, f0(v_phi) + 0.55 * slope),
                       color=ACCENT, stroke_width=THIN_WIDTH)
        touch = Dot(fx.c2p(v_phi, f0(v_phi)), radius=0.07, color=ACCENT)
        slope_label = math(r"\partial f_0/\partial v<0", color=ACCENT, size=30)
        slope_label.next_to(fx.c2p(1.25, 0.42), RIGHT, buff=0.0)

        self.play(Create(ph), Create(fx),
                  FadeIn(ph_labels), FadeIn(fx_labels), run_time=1.0, rate_func=EASE)
        self.play(FadeIn(family), Create(separatrix), Create(maxwellian),
                  FadeIn(trapped), FadeIn(passing), run_time=0.8, rate_func=EASE)
        self.play(Create(res_line), FadeIn(res_label), Create(tangent), FadeIn(touch),
                  FadeIn(slope_label), FadeIn(electron), run_time=0.6, rate_func=EASE)
        self.add(trail, electron)
        self.play(tracker.animate.set_value(BOUNCE_TIME), run_time=9.0, rate_func=LINEAR)
        self.wait(1.4)
