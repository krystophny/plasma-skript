"""Gyration in a uniform magnetic field: top view, velocity and position
components, and the helix.

Model (B = B e_z, E = 0, charge sign s = sign(q)): the board solution

    v_x = v_perp cos(omega_c t + phi),   v_y = -s v_perp sin(omega_c t + phi),
    x = x_0 + rho_L sin(omega_c t + phi),  y = y_0 + s rho_L cos(omega_c t + phi),
    z = z_0 + v_par t,

with omega_c = |q_alpha| B/m_alpha (the magnitude of the signed gyrofrequency
q_alpha B/m_alpha) and the Larmor radius rho_L = v_perp/omega_c. Viewed with B out of the
page, ions (s = +1) turn clockwise and electrons (s = -1) counterclockwise.
scripts/check-physics.py integrates the Lorentz force against gyro_orbit.

Top view: an ion and an electron at equal temperature, T_i = T_e, so
rho_Li/rho_Le = sqrt(m_i/m_e) and omega_ce/omega_ci = m_i/m_e. The scene uses the
stated reduced ratio m_i/m_e = 16 (hydrogen: 1836), which keeps the electron
orbit visible (rho_Le = rho_Li/4) and its rotation countable (16 turns per ion
turn). Lengths are in scene units; time is shown as omega_ci t [1].
"""

from manim import *
import numpy as np

from style import (
    B_FIELD, BG, CURVE_WIDTH, DOT_RADIUS, EASE, ELECTRON, FAINT, GRID, INK, ION,
    LABEL_SIZE, LINEAR, MATH_SIZE, MATH_SMALL, MUTED, THIN_WIDTH, AXIS_WIDTH,
    StyledScene, axes, axis_labels, dashed, label, math,
)

# Top view: reduced mass ratio, equal temperatures.
MASS_RATIO = 16.0
TRUE_MASS_RATIO = 1836.15
R_ION = 2.2                                  # scene units
R_ELECTRON = R_ION / np.sqrt(MASS_RATIO)
ION_TURNS = 1                                # loop: integer turns of both
TOP_PLAY_TIME = 14.0                         # seconds of video for one ion turn

# Helix: B along z, pitch 2 pi v_par/omega_c in units of rho_L.
HELIX_PITCH = 1.1
HELIX_TURNS = 3.0
HELIX_PLAY_TIME = 12.0

# Components: two turns of an ion, phase phi = 0.
COMPONENT_TURNS = 2.0
COMPONENT_PLAY_TIME = 12.0


def gyro_orbit(theta, sign, r_l=1.0, phase=0.0, center=(0.0, 0.0)):
    """Perpendicular position at gyrophase theta = omega_c t (array-safe)."""
    a = np.asarray(theta) + phase
    return np.array([center[0] + r_l * np.sin(a), center[1] + sign * r_l * np.cos(a)])


def gyro_velocity(theta, sign, v_perp=1.0, phase=0.0):
    """Perpendicular velocity (v_x, v_y) at gyrophase theta = omega_c t."""
    a = np.asarray(theta) + phase
    return np.array([v_perp * np.cos(a), -sign * v_perp * np.sin(a)])


def helix_point(theta, sign, pitch=HELIX_PITCH, r_l=1.0):
    """Helix position (x, y, z) at gyrophase theta: z advances pitch per turn."""
    x, y = gyro_orbit(theta, sign, r_l)
    return np.array([x, y, pitch * np.asarray(theta) / (2 * np.pi)])


def frequency_ratio(mass_ratio=MASS_RATIO):
    """omega_ce/omega_ci for equal |q| and B."""
    return mass_ratio


def radius_ratio(mass_ratio=MASS_RATIO):
    """rho_Li/rho_Le at equal temperature: v_perp ~ m^(-1/2), rho_L ~ m v_perp."""
    return np.sqrt(mass_ratio)


def b_lattice(xs, ys, size=0.08):
    """Uniform B out of the page: quiet dot-in-circle symbols."""
    marks = VGroup()
    for x in xs:
        for y in ys:
            marks.add(VGroup(Circle(radius=size, color=B_FIELD, stroke_width=1.4),
                             Dot(radius=0.022, color=B_FIELD)).move_to([x, y, 0]))
    return marks.set_opacity(0.55)


def ion_marker(point):
    """Point particle: a small dot; titles name the species."""
    return Dot(point, radius=DOT_RADIUS * 1.3, color=ION)


def sense_arrow(center, radius, start_angle, sign, color):
    """Short arc arrow outside an orbit: clockwise for sign > 0."""
    return Arc(radius=radius, start_angle=start_angle, angle=-sign * 0.9,
               arc_center=center, color=color, stroke_width=THIN_WIDTH
               ).add_tip(tip_length=0.16, tip_width=0.16)


def radius_marker(center, radius, angle, tex, color):
    """Static radius line with its symbol, at a fixed angle."""
    end = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
    line = Line(center, end, color=MUTED, stroke_width=AXIS_WIDTH)
    sym = math(tex, color=color, size=MATH_SMALL)
    normal = np.array([-np.sin(angle), np.cos(angle), 0])
    sym.move_to((center + end) / 2 + 0.32 * normal)
    return VGroup(line, sym)


class GyrationTopView(StyledScene):
    """Ion and electron gyrating in a uniform B out of the page (top view)."""

    def build(self):
        y0 = 0.15
        c_ion = np.array([-3.2, y0, 0])
        c_el = np.array([3.6, y0, 0])

        title_ion = label("ion", color=ION, size=LABEL_SIZE).move_to(c_ion + UP * (R_ION + 0.6))
        title_el = label("electron", color=ELECTRON, size=LABEL_SIZE).move_to(c_el + UP * 1.6)
        field = b_lattice(np.arange(-6.3, 6.4, 1.05), np.arange(-2.7, 3.2, 1.05))
        # Keep the lattice off the orbits and the labels.
        keep = VGroup()
        for mark in field:
            p = mark.get_center()
            clear_titles = all(np.linalg.norm(p - t.get_center()) > 0.4 + t.width / 2
                               for t in (title_ion, title_el))
            if (np.linalg.norm(p - c_ion) > R_ION + 0.35 and np.linalg.norm(p - c_el) > 1.0
                    and abs(p[1] - 3.1) > 0.35 and clear_titles):
                keep.add(mark)
        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}", color=B_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)


        orbit_ion = dashed(Circle(radius=R_ION, color=FAINT, stroke_width=THIN_WIDTH)
                           .move_to(c_ion), num_dashes=60)
        orbit_el = dashed(Circle(radius=R_ELECTRON, color=FAINT, stroke_width=THIN_WIDTH)
                          .move_to(c_el), num_dashes=24)
        gc_ion = Dot(c_ion, radius=0.05, color=INK)
        gc_el = Dot(c_el, radius=0.05, color=INK)
        r_ion = radius_marker(c_ion, R_ION, -2.4, r"\rho_{Li}", ION)
        r_el = radius_marker(c_el, R_ELECTRON, -2.4, r"\rho_{Le}", ELECTRON)
        r_el[1].move_to(c_el + np.array([-0.95, -0.55, 0]))
        sense_ion = sense_arrow(c_ion, R_ION + 0.28, 1.35, +1, ION)
        sense_el = sense_arrow(c_el, R_ELECTRON + 0.28, 1.0, -1, ELECTRON)

        key = VGroup(
            b_key,
            math(rf"m_i/m_e={MASS_RATIO:g}\quad(\mathrm{{H}}{{:}}\ {TRUE_MASS_RATIO:.0f})",
                 color=MUTED, size=MATH_SMALL),
            math(r"T_i=T_e", color=MUTED, size=MATH_SMALL),
        ).arrange(RIGHT, buff=0.7)
        key.move_to([0, -3.35, 0])
        clock_label = math(r"\omega_{ci}t=", color=MUTED, size=MATH_SMALL)
        clock_label.move_to([4.9, 3.35, 0])
        clock = DecimalNumber(0.0, num_decimal_places=2, color=INK, font_size=MATH_SMALL)

        tracker = ValueTracker(0.0)          # ion gyrophase omega_ci t

        def place_clock(m):
            m.set_value(tracker.get_value())
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)

        def point(theta, sign, radius, center):
            x, y = gyro_orbit(theta, sign, radius, center=center[:2])
            return np.array([x, y, 0])

        def trail(sign, radius, center, ratio, color):
            def make():
                th = tracker.get_value() * ratio
                span = min(th, 1.6)
                if span < 1e-3:
                    return VMobject()
                return ParametricFunction(lambda s: point(s, sign, radius, center),
                                          t_range=[th - span, th, span / 40],
                                          color=color, stroke_width=CURVE_WIDTH - 1
                                          ).set_stroke(opacity=[0.0, 1.0])
            return always_redraw(make)

        ion = always_redraw(lambda: ion_marker(point(tracker.get_value(), +1, R_ION, c_ion)))
        electron = always_redraw(lambda: Dot(
            point(tracker.get_value() * frequency_ratio(), -1, R_ELECTRON, c_el),
            radius=DOT_RADIUS * 1.3, color=ELECTRON))
        trail_ion = trail(+1, R_ION, c_ion, 1.0, ION)
        trail_el = trail(-1, R_ELECTRON, c_el, frequency_ratio(), ELECTRON)

        self.add(keep, orbit_ion, orbit_el, gc_ion, gc_el, r_ion, r_el, sense_ion,
                 sense_el, title_ion, title_el, key, clock_label, clock,
                 trail_ion, trail_el, ion, electron)
        self.wait(0.5)
        self.play(tracker.animate.set_value(2 * np.pi * ION_TURNS),
                  run_time=TOP_PLAY_TIME, rate_func=LINEAR)
        self.wait(0.5)


class GyrationComponents(StyledScene):
    """Ion orbit next to v_x(t) and x(t): cosine and sine of amplitude v_perp, rho_L."""

    def build(self):
        r = 1.9
        c = np.array([-4.3, 0.2, 0])
        theta_max = 2 * np.pi * COMPONENT_TURNS

        field = b_lattice(np.arange(-6.6, -1.9, 0.95), np.arange(-2.3, 2.8, 0.95))
        keep = VGroup(*[m for m in field if np.linalg.norm(m.get_center() - c) > r + 0.3])
        orbit = dashed(Circle(radius=r, color=FAINT, stroke_width=THIN_WIDTH).move_to(c),
                       num_dashes=56)
        gc = Dot(c, radius=0.05, color=INK)
        x_axis = Arrow(c + LEFT * (r + 0.5), c + RIGHT * (r + 0.6), buff=0, color=MUTED,
                       stroke_width=AXIS_WIDTH, max_tip_length_to_length_ratio=0.05)
        x_lab = math("x", color=MUTED, size=MATH_SMALL).next_to(x_axis, RIGHT, buff=0.1)
        y_axis = Arrow(c + DOWN * (r + 0.5), c + UP * (r + 0.6), buff=0, color=MUTED,
                       stroke_width=AXIS_WIDTH, max_tip_length_to_length_ratio=0.05)
        y_lab = math("y", color=MUTED, size=MATH_SMALL).next_to(y_axis, UP, buff=0.1)
        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}", color=B_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
        b_key.move_to(c + np.array([-1.3, -r - 1.05, 0]))
        sense = sense_arrow(c, r + 0.3, 2.0, +1, ION)
        r_mark = radius_marker(c, r, -2.3, r"\rho_L", INK)

        w, h = 6.4, 2.3
        top = axes([0, theta_max, np.pi], [-1.3, 1.3, 1], w, h).move_to([2.95, 1.75, 0])
        bot = axes([0, theta_max, np.pi], [-1.3, 1.3, 1], w, h).move_to([2.95, -1.75, 0])
        top_y = math(r"v_x/v_\perp\ [1]", color=MUTED, size=MATH_SMALL).next_to(top.y_axis, UP, buff=0.12)
        bot_y = math(r"(x-x_0)/\rho_L\ [1]", color=MUTED, size=MATH_SMALL).next_to(bot.y_axis, UP, buff=0.12)
        bot_x = math(r"\omega_c t\ [1]", color=MUTED, size=MATH_SMALL)
        bot_x.next_to(bot.x_axis.get_right(), DOWN, buff=0.22).align_to(bot.x_axis.get_right(), RIGHT)
        ticks = VGroup()
        for ax in (top, bot):
            for v in (1, -1):
                ticks.add(math(f"{v:+d}".replace("+", ""), color=MUTED, size=MATH_SMALL)
                          .next_to(ax.c2p(0, v), LEFT, buff=0.15))
                ticks.add(DashedLine(ax.c2p(0, v), ax.c2p(theta_max, v), color=GRID,
                                     stroke_width=1.2, dash_length=0.08))
        for k, tex in ((2, r"2\pi"), (4, r"4\pi")):
            ticks.add(math(tex, color=MUTED, size=MATH_SMALL).next_to(bot.c2p(k * np.pi, -1.3), DOWN, buff=0.12))

        tracker = ValueTracker(0.0)

        def p_xy(theta):
            x, y = gyro_orbit(theta, +1, r)
            return c + np.array([x, y, 0])

        def make_curve(ax, f, color):
            def make():
                th = tracker.get_value()
                if th < 1e-3:
                    return VMobject()
                return ax.plot(f, x_range=[0, th, th / 120], color=color,
                               stroke_width=CURVE_WIDTH - 1)
            return always_redraw(make)

        vx_curve = make_curve(top, lambda s: gyro_velocity(s, +1)[0], ION)
        x_curve = make_curve(bot, lambda s: gyro_orbit(s, +1)[0], ION)
        vx_dot = always_redraw(lambda: Dot(top.c2p(tracker.get_value(),
                                                   gyro_velocity(tracker.get_value(), +1)[0]),
                                           radius=DOT_RADIUS, color=INK))
        x_dot = always_redraw(lambda: Dot(bot.c2p(tracker.get_value(),
                                                  gyro_orbit(tracker.get_value(), +1)[0]),
                                          radius=DOT_RADIUS, color=INK))
        particle = always_redraw(lambda: ion_marker(p_xy(tracker.get_value())))
        velocity = always_redraw(lambda: Arrow(
            p_xy(tracker.get_value()),
            p_xy(tracker.get_value()) + 0.9 * np.append(gyro_velocity(tracker.get_value(), +1), 0),
            buff=0, color=INK, stroke_width=3, max_tip_length_to_length_ratio=0.25))
        drop = always_redraw(lambda: DashedLine(
            p_xy(tracker.get_value()), [p_xy(tracker.get_value())[0], c[1], 0],
            color=MUTED, stroke_width=1.4, dash_length=0.07))
        v_lab = always_redraw(lambda: math(r"\mathbf{v}_\perp", color=INK, size=MATH_SMALL).move_to(
            p_xy(tracker.get_value()) + 0.9 * np.append(gyro_velocity(tracker.get_value(), +1), 0)
            + 0.38 * np.append(gyro_orbit(tracker.get_value(), +1), 0)))

        clock_label = math(r"\omega_c t=", color=MUTED, size=MATH_SMALL).move_to([-3.3, -2.75, 0])
        clock = DecimalNumber(0.0, num_decimal_places=2, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            m.set_value(tracker.get_value())
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)

        self.add(keep, orbit, gc, x_axis, x_lab, y_axis, y_lab, b_key, sense, r_mark,
                 top, bot, top_y, bot_y, bot_x, ticks, clock_label, clock,
                 vx_curve, x_curve, drop, velocity, v_lab, particle, vx_dot, x_dot)
        self.wait(0.5)
        self.play(tracker.animate.set_value(theta_max), run_time=COMPONENT_PLAY_TIME,
                  rate_func=LINEAR)
        self.wait(1.0)


def oblique(point, phi=np.radians(68), theta=np.radians(-55)):
    """Project a 3D point (z up) onto the screen as seen from polar angle phi
    and azimuth theta (Manim's ThreeDCamera convention)."""
    x, y, z = point
    # Rotate about z so that the viewer sits at azimuth theta, then tilt.
    a = -theta - np.pi / 2
    xr = x * np.cos(a) - y * np.sin(a)
    yr = x * np.sin(a) + y * np.cos(a)
    return np.array([xr, yr * np.cos(phi) + z * np.sin(phi), 0.0])


class GyrationHelix(StyledScene):
    """Ion helix with v_par != 0 along B = B e_z, its guiding centre and projection."""

    def build(self):
        scale = 1.5                          # scene units per rho_L
        theta_max = 2 * np.pi * HELIX_TURNS
        z_top = HELIX_PITCH * HELIX_TURNS
        origin = np.array([-0.6, -2.55, 0])

        def to_screen(p):
            return origin + scale * oblique(p)

        base = dashed(ParametricFunction(lambda s: to_screen([np.cos(s), np.sin(s), 0]),
                                         t_range=[0, TAU, TAU / 120], color=FAINT,
                                         stroke_width=THIN_WIDTH), num_dashes=48)
        axis = DashedLine(to_screen([0, 0, 0]), to_screen([0, 0, z_top + 0.45]), color=MUTED,
                          stroke_width=THIN_WIDTH, dash_length=0.1)
        b_start = to_screen([0, 0, 0]) + np.array([-3.6, 0.4, 0])
        b_arrow = Arrow(b_start, b_start + UP * 2.6, buff=0, color=B_FIELD, stroke_width=4,
                        max_tip_length_to_length_ratio=0.12)
        b_lab = math(r"\mathbf{B}", color=B_FIELD, size=MATH_SIZE).next_to(b_arrow, UP, buff=0.15)
        # Radius toward the lower right of the base ellipse on screen.
        angles = np.linspace(0, TAU, 360, endpoint=False)
        a_front = angles[np.argmin([np.dot(oblique([np.cos(a), np.sin(a), 0])[:2], [-1, 1])
                                    for a in angles])]
        r_line = Line(to_screen([0, 0, 0]), to_screen([np.cos(a_front), np.sin(a_front), 0]),
                      color=MUTED, stroke_width=AXIS_WIDTH)
        r_lab = math(r"\rho_L", color=INK, size=MATH_SMALL).next_to(r_line.get_end(), DR, buff=0.08)
        v_par = Arrow(to_screen([0, 0, z_top + 0.45]), to_screen([0, 0, z_top + 1.25]), buff=0,
                      color=INK, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        v_par_lab = math(r"v_\parallel", color=INK, size=MATH_SMALL).next_to(v_par, RIGHT, buff=0.12)

        tracker = ValueTracker(0.0)

        def trace():
            th = tracker.get_value()
            if th < 1e-3:
                return VMobject()
            return ParametricFunction(lambda s: to_screen(helix_point(s, +1)),
                                      t_range=[0, th, 0.03], color=ION,
                                      stroke_width=CURVE_WIDTH - 1)

        helix = always_redraw(trace)
        particle = always_redraw(lambda: Dot(to_screen(helix_point(tracker.get_value(), +1)),
                                             radius=DOT_RADIUS * 1.3, color=ION))
        centre = always_redraw(lambda: Dot(
            to_screen([0, 0, helix_point(tracker.get_value(), +1)[2]]),
            radius=0.05, color=INK))
        shadow = always_redraw(lambda: Dot(
            to_screen([*gyro_orbit(tracker.get_value(), +1), 0]),
            radius=DOT_RADIUS * 0.8, color=FAINT))

        clock_label = math(r"\omega_c t=", color=MUTED, size=MATH_SMALL).move_to([4.2, 3.3, 0])
        clock = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            m.set_value(tracker.get_value())
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)
        key = math(rf"2\pi v_\parallel/\omega_c={HELIX_PITCH:g}\,\rho_L", color=MUTED,
                   size=MATH_SMALL).move_to([4.4, -3.3, 0])

        self.add(base, axis, b_arrow, b_lab, r_line, r_lab, v_par, v_par_lab, key,
                 clock_label, clock, shadow, helix, centre, particle)
        self.wait(0.5)
        self.play(tracker.animate.set_value(theta_max), run_time=HELIX_PLAY_TIME,
                  rate_func=LINEAR)
        self.wait(1.0)
