"""Debye shielding as a self-consistent movement of mobile charges.

The scene integrates a reduced, one-dimensional slab model in normalized
variables.  A localized positive test charge is balanced by a broad fixed
background; the electron density evolves according to overdamped
drift-diffusion coupled to Poisson's equation::

    ∂nₑ/∂τ = −∂ₓ Γₑ,   Γₑ = −∂ₓ nₑ + nₑ ∂ₓ φ,
    ∂ₓ² φ = nₑ − 1 − ρ_ext.

Here x/λ_D [1] and t/τ_D [1] are the displayed reference-scaled
coordinates.  The dots are deterministic macroparticle markers reconstructed
from the evolving density, so the visible screening is caused by their
movement.  This is a pedagogical relaxation model, not a full 3D PIC result.
"""

import os

from manim import *
from manim.mobject.text.text_mobject import register_font
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
ION_COLOR = "#F2A65A"
ELECTRON_COLOR = "#4EA8DE"
FIELD_COLOR = "#72D6C9"
TEST_COLOR = "#F7C948"
# Fontconfig exposes the New Computer Modern family under this exact name.
TEXT_FONT = "NewComputerModern"
TEXT_FONT_FILE = os.environ.get("PLASMA_NEW_COMPUTER_MODERN_FONT")


def _derivative(values, wave_numbers):
    """Return a periodic spectral derivative of a grid quantity."""

    return np.real(np.fft.ifft(1j * wave_numbers * np.fft.fft(values)))


def _potential(charge_density, wave_numbers):
    """Solve the periodic, zero-mean Poisson equation in Fourier space."""

    charge_hat = np.fft.fft(charge_density)
    potential_hat = np.zeros_like(charge_hat, dtype=complex)
    nonzero = np.abs(wave_numbers) > 1e-12
    potential_hat[nonzero] = charge_hat[nonzero] / wave_numbers[nonzero] ** 2
    return np.real(np.fft.ifft(potential_hat))


def _marker_positions(density, grid, half_width, count):
    """Map equally weighted markers to the cumulative density."""

    dx = grid[1] - grid[0]
    edges = np.linspace(-half_width, half_width, len(grid) + 1)
    cumulative = np.concatenate(([0.0], np.cumsum(np.maximum(density, 1e-6) * dx)))
    cumulative /= cumulative[-1]
    quantiles = (np.arange(count) + 0.5) / count
    return np.interp(quantiles, cumulative, edges)


def _relaxation_history():
    """Integrate the reduced electron response and return render snapshots."""

    half_width = 8.0
    grid_size = 160
    grid = np.linspace(-half_width, half_width, grid_size, endpoint=False)
    dx = grid[1] - grid[0]
    wave_numbers = 2 * np.pi * np.fft.fftfreq(grid_size, d=dx)

    # A narrow positive source represents the test charge.  The broad
    # compensating term keeps the periodic teaching box charge balanced.
    source_width = 0.32
    source_strength = 0.72
    localized_source = source_strength / (np.sqrt(2 * np.pi) * source_width) * np.exp(
        -(grid**2) / (2 * source_width**2)
    )
    external_charge = localized_source - localized_source.mean()

    density = np.ones(grid_size)
    time_step = 0.0005
    total_steps = 7200
    sample_stride = 60
    density_history = []
    potential_history = []
    time_history = []

    for step in range(total_steps + 1):
        charge_density = 1.0 - density + external_charge
        potential = _potential(charge_density, wave_numbers)

        if step % sample_stride == 0:
            density_history.append(density.copy())
            potential_history.append(potential.copy())
            time_history.append(step * time_step)

        potential_gradient = _derivative(potential, wave_numbers)
        density_gradient = _derivative(density, wave_numbers)
        electron_flux = -density_gradient + density * potential_gradient
        density -= time_step * _derivative(electron_flux, wave_numbers)
        density = np.maximum(density, 0.2)
        density /= density.mean()

    density_history = np.asarray(density_history)
    potential_history = np.asarray(potential_history)
    potential_scale = max(np.max(np.abs(potential_history[0])), 1e-8)
    potential_history /= potential_scale

    markers = np.asarray(
        [
            _marker_positions(snapshot, grid, half_width, count=32)
            for snapshot in density_history
        ]
    )
    return grid, np.asarray(time_history), density_history, potential_history, markers


class DebyeShielding(Scene):
    """Show a localized charge becoming screened as electron markers move."""

    def construct(self):
        if not TEXT_FONT_FILE:
            raise RuntimeError(
                "PLASMA_NEW_COMPUTER_MODERN_FONT must be set by the Nix environment"
            )
        with register_font(TEXT_FONT_FILE):
            self._construct_scene()

    def _construct_scene(self):
        self.camera.background_color = BG

        (
            grid,
            times,
            density_history,
            potential_history,
            electron_positions,
        ) = _relaxation_history()
        half_width = 8.0
        history_count = len(times)
        marker_count = electron_positions.shape[1]

        title = Text(
            "Debye shielding by particle motion",
            color=INK,
            font_size=32,
            font=TEXT_FONT,
            disable_ligatures=True,
        )
        subtitle = Text(
            "self-consistent electron relaxation in a 1D slab model",
            color=MUTED,
            font_size=20,
            font=TEXT_FONT,
            disable_ligatures=True,
        )
        title_group = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        title_group.to_edge(UP, buff=0.28).to_edge(LEFT, buff=0.42)

        time_label = MathTex(r"t/\tau_D\ [1] =", color=FIELD_COLOR, font_size=25)
        time_value = DecimalNumber(
            0.0,
            num_decimal_places=1,
            color=FIELD_COLOR,
            font_size=25,
        )
        time_group = VGroup(time_label, time_value).arrange(RIGHT, buff=0.08)
        time_group.to_corner(UR, buff=0.38)

        left_center = np.array([-3.75, 0.15, 0.0])
        left_box = RoundedRectangle(
            width=5.85,
            height=3.55,
            corner_radius=0.16,
            color=GRID,
            stroke_width=2,
        ).move_to(left_center)
        model_label = Text(
            "mobile electrons move; ions stay fixed",
            color=MUTED,
            font_size=18,
            font=TEXT_FONT,
            disable_ligatures=True,
        ).move_to(left_center + UP * 1.33)

        domain_y = left_center[1] - 0.12
        domain_left = left_center[0] - 2.48
        domain_right = left_center[0] + 2.48

        def particle_point(position, vertical_offset=0.0):
            horizontal = domain_left + (position + half_width) / (2 * half_width) * (
                domain_right - domain_left
            )
            return np.array([horizontal, domain_y + vertical_offset, 0.0])

        domain = Line(
            particle_point(-half_width),
            particle_point(half_width),
            color=GRID,
            stroke_width=3,
        )
        domain_label = MathTex(r"x/\lambda_D\ [1]", color=MUTED, font_size=18).move_to(
            left_center + DOWN * 0.78
        )

        ion_positions = np.linspace(-7.3, 7.3, marker_count)
        ion_offsets = 0.13 * np.cos(np.arange(marker_count) * 1.7)
        electron_offsets = 0.13 * np.sin(np.arange(marker_count) * 1.9)
        ions = VGroup(
            *[
                Triangle(
                    color=ION_COLOR,
                    fill_color=ION_COLOR,
                    fill_opacity=1,
                    stroke_width=1,
                )
                .scale(0.095)
                .move_to(particle_point(position, offset))
                for position, offset in zip(ion_positions, ion_offsets)
            ]
        )
        electrons = VGroup(
            *[
                Dot(
                    particle_point(position, offset),
                    radius=0.055,
                    color=ELECTRON_COLOR,
                )
                for position, offset in zip(electron_positions[0], electron_offsets)
            ]
        )

        tracker = ValueTracker(0.0)

        def frame_index():
            return min(
                history_count - 1,
                max(0, int(round(tracker.get_value() * (history_count - 1)))),
            )

        def update_particles(group):
            positions = electron_positions[frame_index()]
            for dot, position, offset in zip(group, positions, electron_offsets):
                dot.move_to(particle_point(position, offset))

        electrons.add_updater(update_particles)

        test_charge = Star(
            n=5,
            outer_radius=0.22,
            inner_radius=0.095,
            color=TEST_COLOR,
            fill_color=TEST_COLOR,
            fill_opacity=1,
        ).move_to(particle_point(0.0, 0.0))
        test_charge_label = VGroup(
            MathTex(r"+Q", color=TEST_COLOR, font_size=23),
            Text(
                "test charge",
                color=TEST_COLOR,
                font_size=16,
                font=TEXT_FONT,
                disable_ligatures=True,
            ),
        ).arrange(DOWN, buff=0.02).next_to(test_charge, UP, buff=0.08)

        left_arrows = VGroup(
            Arrow(
                particle_point(-5.8, -0.46),
                particle_point(-4.45, -0.46),
                color=ELECTRON_COLOR,
                stroke_width=3,
                buff=0,
                max_tip_length_to_length_ratio=0.18,
            ),
            Arrow(
                particle_point(5.8, -0.46),
                particle_point(4.45, -0.46),
                color=ELECTRON_COLOR,
                stroke_width=3,
                buff=0,
                max_tip_length_to_length_ratio=0.18,
            ),
        )
        motion_label = Text(
            "electron motion toward +Q",
            color=ELECTRON_COLOR,
            font_size=16,
            font=TEXT_FONT,
            disable_ligatures=True,
        )
        motion_label.move_to(left_center + DOWN * 1.18)

        legend = VGroup(
            VGroup(
                Triangle(
                    color=ION_COLOR,
                    fill_color=ION_COLOR,
                    fill_opacity=1,
                    stroke_width=1,
                ).scale(0.075),
                Text(
                    "fixed ion background",
                    color=MUTED,
                    font_size=15,
                    font=TEXT_FONT,
                    disable_ligatures=True,
                ),
            ).arrange(RIGHT, buff=0.08),
            VGroup(
                Dot(radius=0.045, color=ELECTRON_COLOR),
                Text(
                    "mobile electron markers",
                    color=MUTED,
                    font_size=15,
                    font=TEXT_FONT,
                    disable_ligatures=True,
                ),
            ).arrange(RIGHT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        legend.move_to(left_center + DOWN * 1.53)

        density_axes = Axes(
            x_range=[-8.0, 8.0, 4.0],
            y_range=[0.7, 1.7, 0.25],
            x_length=5.1,
            y_length=1.42,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).move_to(np.array([3.25, 1.05, 0.0]))
        potential_axes = Axes(
            x_range=[-8.0, 8.0, 4.0],
            y_range=[-0.55, 1.05, 0.4],
            x_length=5.1,
            y_length=1.42,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).move_to(np.array([3.25, -1.33, 0.0]))

        density_ylabel = MathTex(r"n_e/n_0\ [1]", color=MUTED, font_size=17).rotate(PI / 2)
        density_ylabel.next_to(density_axes.y_axis, LEFT, buff=0.13)
        density_xlabel = MathTex(r"x/\lambda_D\ [1]", color=MUTED, font_size=17)
        density_xlabel.next_to(density_axes.x_axis, DOWN, buff=0.16)
        potential_ylabel = MathTex(r"\phi/\phi_0\ [1]", color=MUTED, font_size=17).rotate(PI / 2)
        potential_ylabel.next_to(potential_axes.y_axis, LEFT, buff=0.13)
        potential_xlabel = MathTex(r"x/\lambda_D\ [1]", color=MUTED, font_size=17)
        potential_xlabel.next_to(potential_axes.x_axis, DOWN, buff=0.16)

        density_baseline = DashedLine(
            density_axes.c2p(-8.0, 1.0),
            density_axes.c2p(8.0, 1.0),
            color=MUTED,
            stroke_width=2,
            dash_length=0.08,
        )
        initial_potential = VMobject(color=MUTED, stroke_width=2)
        initial_potential.set_points_as_corners(
            [
                potential_axes.c2p(position, value)
                for position, value in zip(grid[::2], potential_history[0, ::2])
            ]
        )
        initial_potential = DashedVMobject(initial_potential, num_dashes=32)

        density_curve = VMobject(color=ELECTRON_COLOR, stroke_width=4)
        potential_curve = VMobject(color=FIELD_COLOR, stroke_width=4)

        def update_curve(mob, axes, snapshots, scale=1.0):
            values = snapshots[frame_index()] / scale
            mob.set_points_as_corners(
                [
                    axes.c2p(position, value)
                    for position, value in zip(grid[::2], values[::2])
                ]
            )

        density_curve.set_points_as_corners(
            [
                density_axes.c2p(position, value)
                for position, value in zip(grid[::2], density_history[0, ::2])
            ]
        )
        potential_curve.set_points_as_corners(
            [
                potential_axes.c2p(position, value)
                for position, value in zip(grid[::2], potential_history[0, ::2])
            ]
        )
        density_curve.add_updater(
            lambda mob: update_curve(mob, density_axes, density_history)
        )
        potential_curve.add_updater(
            lambda mob: update_curve(mob, potential_axes, potential_history)
        )

        density_title = Text(
            "electron density",
            color=ELECTRON_COLOR,
            font_size=18,
            font=TEXT_FONT,
            disable_ligatures=True,
        )
        density_title.next_to(density_axes, UP, buff=0.11)
        potential_title = Text(
            "electrostatic potential",
            color=FIELD_COLOR,
            font_size=18,
            font=TEXT_FONT,
            disable_ligatures=True,
        )
        potential_title.next_to(potential_axes, UP, buff=0.11)
        initial_key = VGroup(
            DashedLine(ORIGIN, RIGHT * 0.33, color=MUTED, stroke_width=2),
            Text(
                "initial",
                color=MUTED,
                font_size=14,
                font=TEXT_FONT,
                disable_ligatures=True,
            ),
        ).arrange(RIGHT, buff=0.07)
        initial_key.next_to(potential_axes, RIGHT, buff=0.1).shift(UP * 0.15)

        def status_text():
            current_time = times[frame_index()]
            if current_time < 0.8:
                message = "response begins: electrons move inward"
            elif current_time < 2.2:
                message = "negative charge gathers around +Q"
            else:
                message = "localized potential: screened response"
            return Text(
                message,
                color=INK,
                font_size=17,
                font=TEXT_FONT,
                disable_ligatures=True,
            ).move_to(np.array([3.25, -2.76, 0.0]))

        status = always_redraw(status_text)
        time_value.add_updater(lambda mob: mob.set_value(times[frame_index()]))

        self.play(
            FadeIn(title_group),
            FadeIn(time_group),
            FadeIn(left_box),
            FadeIn(model_label),
            Create(domain),
            FadeIn(domain_label),
            Create(density_axes),
            Create(potential_axes),
            FadeIn(density_ylabel),
            FadeIn(density_xlabel),
            FadeIn(potential_ylabel),
            FadeIn(potential_xlabel),
            run_time=1.4,
        )
        self.play(
            FadeIn(ions),
            FadeIn(electrons),
            FadeIn(test_charge),
            FadeIn(test_charge_label),
            GrowArrow(left_arrows[0]),
            GrowArrow(left_arrows[1]),
            FadeIn(motion_label),
            FadeIn(legend),
            Create(density_baseline),
            Create(initial_potential),
            Create(density_curve),
            Create(potential_curve),
            FadeIn(density_title),
            FadeIn(potential_title),
            FadeIn(initial_key),
            FadeIn(status),
            run_time=1.6,
        )
        self.add(electrons, density_curve, potential_curve, status, time_value)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=8.0, rate_func=linear)
        self.wait(1.0)
