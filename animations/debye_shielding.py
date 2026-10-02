"""Debye shielding as movement of mobile charges.

The scene integrates a reduced, one-dimensional slab model in normalized
variables.  A localized positive test charge is balanced by a broad fixed
background; the electron density evolves according to overdamped
drift-diffusion coupled to Poisson's equation::

    ∂nₑ/∂τ = −∂ₓ Γₑ,   Γₑ = −∂ₓ nₑ + nₑ ∂ₓ φ,
    ∂ₓ² φ = nₑ − 1 − ρ_ext.

Here x/λ_D [1] and t/τ_D [1] are the displayed reference-scaled
coordinates.  The density and potential profiles on the right are the
one-dimensional model output.  The left panel uses a separate deterministic
two-dimensional particle relaxation so the screening cloud is formed by
markers moving in both x/λ_D [1] and y/λ_D [1].  It is a pedagogical particle
illustration, not a full 2D or 3D particle-in-cell result.
"""

from manim import *
import numpy as np

from style import (
    AXIS_WIDTH, BG, CURVE_WIDTH, EASE, ELECTRON, FAINT, GRID, INK, ION, LINEAR,
    MUTED, POTENTIAL, THIN_WIDTH, StyledScene, axes, math,
)


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


def _scattered_particle_positions(
    count,
    seed,
    half_range=2.2,
    minimum_separation=0.30,
    exclusion_radius=0.42,
):
    """Return reproducible, randomly scattered 2D positions.

    The hard-core spacing prevents markers from being rendered on top of one
    another, while the seeded rejection sampler keeps the animation stable
    across builds.  The central exclusion leaves the positive test charge
    visible at the start of the response.
    """

    rng = np.random.default_rng(seed)
    positions = []
    max_attempts = max(10_000, 4_000 * count)

    for _ in range(max_attempts):
        if len(positions) == count:
            break
        candidate = rng.uniform(-half_range, half_range, size=2)
        if np.linalg.norm(candidate) < exclusion_radius:
            continue
        if positions:
            existing = np.asarray(positions)
            distances = np.linalg.norm(existing - candidate, axis=1)
            if np.min(distances) < minimum_separation:
                continue
        positions.append(candidate)

    if len(positions) != count:
        raise RuntimeError("could not place the requested scattered 2D markers")
    return np.asarray(positions)


def _two_dimensional_marker_history(snapshot_count, initial_positions):
    """Return deterministic 2D radial trajectories for the particle panel.

    Each marker keeps its direction and moves inward by a fraction that
    decays with distance from +Q, so the electron density rises near the
    test charge while the far field stays at the background density.  The
    map r -> r (1 - 0.45 exp(-r^2/1.44)) is monotonic, so markers never cross.
    """

    initial = np.asarray(initial_positions, dtype=float)
    if initial.ndim != 2 or initial.shape[1] != 2:
        raise ValueError("2D particle positions must have shape (count, 2)")

    radius = np.linalg.norm(initial, axis=1)
    final_scale = 1.0 - 0.45 * np.exp(-(radius**2) / 1.44)
    final = initial * final_scale[:, np.newaxis]

    # Relaxation-like approach to the screened state.
    fractions = 1.0 - np.exp(-4.0 * np.linspace(0.0, 1.0, snapshot_count))
    fractions /= fractions[-1]
    return np.asarray(
        [(1.0 - fraction) * initial + fraction * final for fraction in fractions]
    )


class DebyeShielding(StyledScene):
    """Show a localized charge becoming screened as electron markers move in 2D."""

    def build(self):
        grid, times, density_history, potential_history, _ = _relaxation_history()
        history_count = len(times)
        marker_count = 64
        scattered = _scattered_particle_positions(2 * marker_count, seed=20260915)
        ion_positions = scattered[:marker_count]
        electron_history = _two_dimensional_marker_history(
            history_count, scattered[marker_count:])

        tracker = ValueTracker(0.0)

        def frame_index():
            return min(history_count - 1,
                       max(0, int(round(tracker.get_value() * (history_count - 1)))))

        # --- left: 2D marker panel (prescribed motion) ----------------------
        half_range = 2.4
        side = 5.0
        panel_center = np.array([-3.55, 0.0, 0.0])

        def pp(x, y):
            return panel_center + np.array([x, y, 0.0]) * side / (2 * half_range)

        frame = Square(side_length=side, color=GRID, stroke_width=AXIS_WIDTH).move_to(panel_center)
        panel_labels = VGroup(
            math(r"x/\lambda_D\ [1]", color=MUTED, size=30).next_to(frame, DOWN, buff=0.18)
            .align_to(frame, RIGHT),
            math(r"y/\lambda_D\ [1]", color=MUTED, size=30).next_to(frame, UP, buff=0.18)
            .align_to(frame, LEFT),
        )
        debye_circle = DashedVMobject(
            Circle(radius=side / (2 * half_range), color=FAINT, stroke_width=THIN_WIDTH),
            num_dashes=36).move_to(panel_center)
        debye_label = VGroup(
            DashedLine(ORIGIN, RIGHT * 0.5, color=FAINT, stroke_width=THIN_WIDTH, dash_length=0.08),
            math(r"r=\lambda_D", color=MUTED, size=30),
        ).arrange(RIGHT, buff=0.15)
        debye_label.next_to(frame, UP, buff=0.18).align_to(frame, RIGHT)

        ions = VGroup(*[
            Triangle(color=ION, fill_color=ION, fill_opacity=1, stroke_width=0)
            .scale(0.085).move_to(pp(x, y)) for x, y in ion_positions
        ])
        electrons = VGroup(*[Dot(pp(x, y), radius=0.065, color=ELECTRON)
                             for x, y in electron_history[0]])

        def update_electrons(group):
            for dot, (x, y) in zip(group, electron_history[frame_index()]):
                dot.move_to(pp(x, y))

        electrons.add_updater(update_electrons)
        trails = always_redraw(lambda: VGroup(*[
            Line(pp(*a), pp(*b), color=ELECTRON, stroke_width=1.4, stroke_opacity=0.45)
            for a, b in zip(electron_history[0], electron_history[frame_index()])
            if np.linalg.norm(b - a) > 0.02
        ]))
        test_charge = VGroup(
            Circle(radius=0.17, color=INK, fill_color=INK, fill_opacity=1, stroke_width=0),
            math("+", color=BG, size=34),
        ).move_to(pp(0, 0))

        # --- right: 1D slab model profiles ---------------------------------
        dens_ax = axes([-8, 8, 2], [0.85, 1.3, 0.1], 6.0, 1.7).move_to([3.45, 1.5, 0])
        pot_ax = axes([-8, 8, 2], [-0.6, 1.05, 0.5], 6.0, 2.0).move_to([3.45, -1.45, 0])
        dens_labels = VGroup(
            math(r"n_e/n_0\ [1]", color=ELECTRON, size=30).next_to(dens_ax, UP, buff=0.15)
            .align_to(dens_ax, LEFT),
            math(r"x/\lambda_D\ [1]", color=MUTED, size=30).next_to(dens_ax, DOWN, buff=0.12)
            .align_to(dens_ax, RIGHT),
        )
        pot_labels = VGroup(
            math(r"\phi/\phi_0\ [1]", color=POTENTIAL, size=30).next_to(pot_ax, UP, buff=0.1)
            .align_to(pot_ax, LEFT),
            math(r"x/\lambda_D\ [1]", color=MUTED, size=30).next_to(pot_ax, DOWN, buff=0.12)
            .align_to(pot_ax, RIGHT),
        )
        background = DashedLine(dens_ax.c2p(-8, 1.0), dens_ax.c2p(8, 1.0), color=FAINT,
                                stroke_width=THIN_WIDTH, dash_length=0.08)

        def profile(ax, values, **style):
            return VMobject(**style).set_points_smoothly(
                [ax.c2p(x, v) for x, v in zip(grid[::2], values[::2])])

        bare = DashedVMobject(profile(pot_ax, potential_history[0], color=FAINT,
                                      stroke_width=THIN_WIDTH), num_dashes=60)
        bare_label = math(r"t=0", color=FAINT, size=28).next_to(pot_ax.c2p(1.6, 0.75), RIGHT, buff=0.1)
        density_curve = always_redraw(lambda: profile(
            dens_ax, density_history[frame_index()], color=ELECTRON, stroke_width=CURVE_WIDTH))
        potential_curve = always_redraw(lambda: profile(
            pot_ax, potential_history[frame_index()], color=POTENTIAL, stroke_width=CURVE_WIDTH))

        self.play(Create(frame), FadeIn(panel_labels),
                  Create(dens_ax), Create(pot_ax), FadeIn(dens_labels), FadeIn(pot_labels),
                  run_time=1.2, rate_func=EASE)
        self.play(FadeIn(ions), FadeIn(electrons), FadeIn(test_charge),
                  FadeIn(background), FadeIn(density_curve), Create(bare), FadeIn(bare_label),
                  FadeIn(debye_circle), FadeIn(debye_label), run_time=1.0, rate_func=EASE)
        self.add(trails, potential_curve)
        self.wait(0.3)
        self.play(tracker.animate.set_value(1.0), run_time=8.0, rate_func=LINEAR)
        self.wait(1.5)
