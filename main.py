import penguin as p
from functions import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import matplotlib.gridspec as gridspec

def hex_grid(n, spacing=2.0):
    candidates = []
    grid_side = int(np.ceil(np.sqrt(n))) + 4
    for row in range(-grid_side, grid_side + 1):
        for col in range(-grid_side, grid_side + 1):
            x = col * spacing + (row % 2) * spacing * 0.5
            y = row * spacing * (np.sqrt(3) / 2)
            candidates.append([x, y])
    candidates.sort(key=lambda pos: pos[0]**2 + pos[1]**2)
    return candidates[:n]

def main():
    N_PENGUINS = 75
    config = {
    "HEAT_LOSS": 0.01, 
    "HEAT_GAIN": 0.02, 
    "SENSITIVITY": 0.05, 
    "SEPARATION_FORCE": 0.08, # Add this
    "SEPARATION_DIST": 1.2,    # Add this
    "MAX_SPEED": 0.15,        # Add this
    "DAMPING": 0.8
}

    positions = hex_grid(N_PENGUINS)
    penguins = [p.Penguin(heat=np.random.uniform(0.3, 1.0), location=positions[i], velocity=[0, 0]) for i in range(N_PENGUINS)]

    fig = plt.figure(figsize=(15, 7), facecolor="#2b4b77")

    # Top-level: 1 row, 2 columns — sim on left, panel on right
    gs_main = gridspec.GridSpec(1, 2, width_ratios=[2, 1], wspace=0.35, figure=fig)

    # --- LEFT: Simulation ---
    ax_sim = fig.add_subplot(gs_main[0, 0])
    ax_sim.set_facecolor("#1b375c")
    ax_sim.set_title("Penguin Simulator", color="white", fontsize=14)
    ax_sim.set_xlabel("X Position (meters)", color="white")
    ax_sim.set_ylabel("Y Position (meters)", color="white")
    ax_sim.set_xlim(-10, 10); ax_sim.set_ylim(-10, 10); ax_sim.set_aspect("equal")
    ax_sim.tick_params(colors="white")
    scat = ax_sim.scatter(
        [pg.location[0] for pg in penguins],
        [pg.location[1] for pg in penguins],
        c=[pg.heat for pg in penguins], cmap="plasma", vmin=0, vmax=1, s=80
    )

    # --- RIGHT: nested 2-row sub-grid (graph top, sliders bottom) ---
    gs_right = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs_main[0, 1],
                                                height_ratios=[1, 1], hspace=0.55)

    # Temp graph (top-right)
    ax_graph = fig.add_subplot(gs_right[0])
    ax_graph.set_facecolor("#1b375c")
    ax_graph.set_title("Avg Huddle Temperature", color="white", fontsize=10)
    ax_graph.tick_params(colors="white")
    ax_graph.spines[:].set_color("#28558c")
    line, = ax_graph.plot([], [], color="#ffcc00", linewidth=1.5)
    temp_history = []



    # Get the bounding box of the bottom-right cell to position sliders inside it
    # We'll use figure-fraction coordinates manually aligned to gs_right[1]
    # Left edge of the right column starts around x=0.68 in a 15"-wide figure with width_ratios [2,1]
    slider_left   = 0.685
    slider_width  = 0.27
    slider_height = 0.025
    slider_keys   = list(config.keys())
    n_sliders     = len(slider_keys)

    # Distribute sliders evenly inside the bottom half of the figure
    bottom_top    = 0.44   # top of the bottom-right panel (approx)
    bottom_bottom = 0.05
    panel_height  = bottom_top - bottom_bottom
    gap = panel_height / (n_sliders + 1)

    sliders = {}
    for i, key in enumerate(slider_keys):
        y_pos = bottom_top - gap * (i + 1)
        ax_s = fig.add_axes([slider_left, y_pos, slider_width, slider_height],
                            facecolor="#1b375c")
        sl = Slider(ax_s, key, 0.0, 1.0, valinit=config[key], color="#ffcc00")
        sl.label.set_color("white")
        sl.label.set_fontsize(7)
        sl.valtext.set_color("white")
        sl.valtext.set_fontsize(7)

        def make_updater(k):
            def update_val(val):
                config[k] = val
            return update_val

        sl.on_changed(make_updater(key))
        sliders[key] = sl

    def update(frame):
        heat_transfer(penguins, config)
        applyforce(penguins, config)
        for pg in penguins:
            pg.location[0] += pg.velocity[0]
            pg.location[1] += pg.velocity[1]

        scat.set_offsets([[pg.location[0], pg.location[1]] for pg in penguins])
        scat.set_array(np.array([pg.heat for pg in penguins]))

        avg_heat = np.mean([pg.heat for pg in penguins])
        temp_history.append(avg_heat)
        if len(temp_history) > 200:
            temp_history.pop(0)

        line.set_data(range(len(temp_history)), temp_history)
        ax_graph.set_xlim(0, 200)
        ax_graph.set_ylim(0, 1)
        return scat, line

    ani = FuncAnimation(fig, update, interval=40, blit=False, cache_frame_data=False)
    plt.show()
    return 0

main()