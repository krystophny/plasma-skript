"""Finite spherical source and the reduction of its Coulomb potential.

The scene uses normalized coordinates r/lambda_D [1] and potential
phi/(Q/lambda_D) [1].  A uniformly charged three-dimensional sphere is shown
as a two-dimensional cross-section populated by scattered source markers.
The bare Gaussian-CGS potential is quadratic inside the sphere and has a 1/r
tail outside it.  The screened curve solves the linearized spherical
Debye--Hückel equation for the same finite source and therefore has an
exponentially reduced exterior tail.

The fixed source is permeable: mobile electrons occupy its interior and
exterior. Source plus signs and electron dots are a visual aid. The endpoint
curves are analytic continuum equilibria; their linear interpolation is not
a time-dependent field solution. Choose Q small enough that 3 e Q/(2 R kT)
is much less than one; the displayed shape normalization does not fix Q.
"""

from manim import *
import numpy as np

from style import (
    CURVE_WIDTH, EASE, ELECTRON, FAINT, INK, ION, MUTED, POTENTIAL, THIN_WIDTH,
    LABEL_SIZE, StyledScene, axes, label, math, title,
)


SPHERE_RADIUS = 0.5


def _uniform_sphere_potential(radii, radius=SPHERE_RADIUS):
    """Return phi/(Q/lambda_D) for a bare uniform sphere with lambda_D=1."""

    radii = np.asarray(radii, dtype=float)
    potential = np.empty_like(radii)
    inside = radii <= radius
    potential[inside] = (3 * radius**2 - radii[inside] ** 2) / (2 * radius**3)
    potential[~inside] = 1.0 / radii[~inside]
    return potential


def _screened_sphere_potential(radii, radius=SPHERE_RADIUS):
    """Return the exact linearized Debye--Hückel potential for a sphere.

    The input is normalized by lambda_D and the output by Q/lambda_D.  The
    expression matches the regular interior solution and the decaying
    exterior solution at the source boundary.
    """

    radii = np.asarray(radii, dtype=float)
    sphere_parameter = radius
    particular = 3.0 / sphere_parameter**3
    interior_coefficient = (
        -sphere_parameter
        * particular
        * (sphere_parameter + 1.0)
        * np.exp(-sphere_parameter)
        / sphere_parameter
    )
    exterior_coefficient = (
        sphere_parameter
        * particular
        * (
            np.exp(sphere_parameter) * (sphere_parameter - 1.0)
            + (sphere_parameter + 1.0) * np.exp(-sphere_parameter)
        )
        / (2.0 * sphere_parameter)
    )

    potential = np.empty_like(radii)
    inside = radii <= sphere_parameter
    at_origin = inside & (radii == 0.0)
    away_from_origin = inside & ~at_origin
    potential[at_origin] = particular + interior_coefficient
    potential[away_from_origin] = particular + interior_coefficient * (
        np.sinh(radii[away_from_origin]) / radii[away_from_origin]
    )
    potential[~inside] = (
        exterior_coefficient * np.exp(-radii[~inside]) / radii[~inside]
    )
    return potential


def _scattered_annulus_positions(
    count,
    seed,
    inner_radius,
    outer_radius,
    minimum_separation,
):
    """Return reproducible area-uniform 2D points with hard-core spacing."""

    rng = np.random.default_rng(seed)
    positions = []
    max_attempts = max(10_000, 4_000 * count)

    for _ in range(max_attempts):
        if len(positions) == count:
            break
        radius = np.sqrt(
            rng.uniform(inner_radius**2, outer_radius**2)
        )
        angle = rng.uniform(0.0, 2.0 * np.pi)
        candidate = radius * np.array([np.cos(angle), np.sin(angle)])
        if positions:
            existing = np.asarray(positions)
            distances = np.linalg.norm(existing - candidate, axis=1)
            if np.min(distances) < minimum_separation:
                continue
        positions.append(candidate)

    if len(positions) != count:
        raise RuntimeError("could not place the scattered source markers")
    return np.asarray(positions)


def _screening_targets(initial_positions):
    """Move each mobile marker inward without changing its polar direction.

    The inward shift r -> r (1 - 0.4 exp(-r^2)) (r in lambda_D) is largest
    near the source and decays outside about one Debye length, so the far
    electron density is left unchanged.  The map is monotonic in r.
    """

    radii = np.linalg.norm(initial_positions, axis=1)
    # Plasma can enter the fixed volume source. No surface exclusion or
    # collecting wall is imposed; this is a prescribed illustrative map.
    target_radii = radii * (1.0 - 0.4 * np.exp(-(radii**2)))
    directions = initial_positions / radii[:, np.newaxis]
    return directions * target_radii[:, np.newaxis]


class DebyePotentialReduction(StyledScene):
    """Compare the bare and Debye-screened potential of a finite sphere."""

    def build(self):
        heading = title("Screened potential of a finite sphere")

        # --- left: cross-section with source and electron markers ---------
        scale = 1.6                      # Manim units per lambda_D
        center = np.array([-3.75, -0.35, 0.0])

        def pp(position):
            return center + scale * np.array([position[0], position[1], 0.0])

        sphere = Circle(radius=scale * SPHERE_RADIUS, color=ION, stroke_width=THIN_WIDTH,
                        fill_color=ION, fill_opacity=0.12).move_to(center)
        source_positions = _scattered_annulus_positions(
            48, seed=20260916, inner_radius=0.0, outer_radius=0.43,
            minimum_separation=0.085)
        plus = VGroup(*[
            VGroup(Line(LEFT * 0.045, RIGHT * 0.045, color=ION, stroke_width=2.4),
                   Line(DOWN * 0.045, UP * 0.045, color=ION, stroke_width=2.4)).move_to(pp(p))
            for p in source_positions
        ])
        initial = _scattered_annulus_positions(
            64, seed=20260917, inner_radius=0.0, outer_radius=1.48, minimum_separation=0.13)
        target = _screening_targets(initial)
        progress = ValueTracker(0.0)
        electrons = VGroup(*[Dot(pp(p), radius=0.055, color=ELECTRON) for p in initial])

        def move_electrons(group):
            s = progress.get_value()
            for dot, a, b in zip(group, initial, target):
                dot.move_to(pp((1 - s) * a + s * b))

        electrons.add_updater(move_electrons)
        radius_line = Line(center, pp([SPHERE_RADIUS * np.cos(-0.6), SPHERE_RADIUS * np.sin(-0.6)]),
                           color=INK, stroke_width=1.8)
        radius_label = math(r"R/\lambda_D=0.5\ [1]", color=MUTED, size=30)
        radius_label.next_to(pp([0, -1.5]), DOWN, buff=0.25)

        # --- right: radial potential ----------------------------------------
        ax = axes([0, 4, 1], [0, 3.2, 1], 6.2, 4.6).move_to([3.45, -0.55, 0])
        ax_labels = VGroup(
            math(r"r/\lambda_D\ [1]", color=MUTED, size=30).next_to(ax.x_axis, DOWN, buff=0.2)
            .align_to(ax.x_axis, RIGHT),
            math(r"\phi\,\lambda_D/Q\ [1]", color=MUTED, size=30).next_to(ax.y_axis, UP, buff=0.18),
        )
        ax_numbers = VGroup(*[
            math(str(k), color=FAINT, size=26).next_to(ax.c2p(k, 0), DOWN, buff=0.14)
            for k in (1, 2, 3)
        ])
        r_mark = DashedLine(ax.c2p(SPHERE_RADIUS, 0), ax.c2p(SPHERE_RADIUS, 3.2), color=FAINT,
                            stroke_width=1.6, dash_length=0.08)
        r_mark_label = math(r"R", color=MUTED, size=30).next_to(ax.c2p(SPHERE_RADIUS, 0), DOWN, buff=0.14)

        radii = np.linspace(0.0, 4.0, 241)
        bare_values = _uniform_sphere_potential(radii)
        screened_values = _screened_sphere_potential(radii)

        def curve(values, **style):
            return VMobject(**style).set_points_smoothly(
                [ax.c2p(r, v) for r, v in zip(radii, values)])

        bare = DashedVMobject(curve(bare_values, color=INK, stroke_width=THIN_WIDTH), num_dashes=70)
        screened = always_redraw(lambda: curve(
            (1 - progress.get_value()) * bare_values + progress.get_value() * screened_values,
            color=POTENTIAL, stroke_width=CURVE_WIDTH))
        bare_label = label("bare", color=INK, size=LABEL_SIZE).move_to(ax.c2p(2.95, 0.62))
        screened_label = label("screened", color=POTENTIAL, size=LABEL_SIZE).move_to(ax.c2p(1.8, 0.31))

        self.play(FadeIn(heading), Create(ax), FadeIn(ax_labels), FadeIn(ax_numbers),
                  FadeIn(r_mark), FadeIn(r_mark_label), run_time=0.9, rate_func=EASE)
        self.play(FadeIn(sphere), FadeIn(plus), FadeIn(radius_line), FadeIn(radius_label),
                  FadeIn(electrons), Create(bare), FadeIn(bare_label), run_time=1.1, rate_func=EASE)
        self.add(screened)
        self.wait(0.6)
        self.play(progress.animate.set_value(1.0), run_time=5.0, rate_func=EASE)
        self.play(FadeIn(screened_label), run_time=0.6, rate_func=EASE)
        self.wait(3.4)
