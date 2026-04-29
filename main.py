import penguin as p
from functions import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
import matplotlib.gridspec as gridspec

def main():
    N_PENGUINS = 150
    config = {
        "HEAT_LOSS": 0.175, 
        "HEAT_GAIN": 0.02, 
        "SENSITIVITY": 0.05, 
        "SEPARATION_FORCE": 0.08, 
        "SEPARATION_DIST": .5,    
        "MAX_SPEED": 0.15,        
        "DAMPING": 0.363,
        "TARGET_X": 0.0,
        "TARGET_Y": 0.0
    }
    
    positions = hex_grid(N_PENGUINS)
    penguins = [p.Penguin(t=0, heat=np.random.uniform(0.3, 1.0), location=positions[i], velocity=[0, 0]) for i in range(N_PENGUINS)]

    fig = plt.figure("Penguin Thermodynamics Analysis", figsize=(16, 8), facecolor="#2b4b77")
    gs_main = gridspec.GridSpec(1, 2, width_ratios=[2, 1], wspace=0.3, figure=fig)

    # --- LEFT: Simulation ---
    ax_sim = fig.add_subplot(gs_main[0, 0])
    ax_sim.set_facecolor("#1b375c")
    ax_sim.set_title("Penguin Simulator (Click to move huddle)", color="white", fontsize=14)
    ax_sim.set_xlim(-10, 10); ax_sim.set_ylim(-10, 10); ax_sim.set_aspect("equal")
    ax_sim.tick_params(colors="white")
    scat = ax_sim.scatter([pg.location[0] for pg in penguins], [pg.location[1] for pg in penguins], 
                          c=[pg.heat for pg in penguins], cmap="plasma", vmin=0, vmax=1, s=80)

    # --- RIGHT: Nested metrics ---
    # Increased to 5 rows to fit the button under the top graph
    gs_right = gridspec.GridSpecFromSubplotSpec(5, 1, subplot_spec=gs_main[0, 1], hspace=0.6)
    
    # Graphs
    axes = [fig.add_subplot(gs_right[1]), fig.add_subplot(gs_right[2]), fig.add_subplot(gs_right[3])]
    titles = ["Avg Temp", "Huddle Compactness", "Colony Agitation Index"]
    lines = []
    histories = [[], [], []]
    
    for i, ax in enumerate(axes):
        ax.set_facecolor("#1b375c")
        ax.set_title(titles[i], color="white", fontsize=9)
        ax.tick_params(colors="white", labelsize=8)
        line, = ax.plot([], [], color="#ffcc00", linewidth=1.5)
        lines.append(line)

    # --- Button Implementation ---
    ax_btn = fig.add_subplot(gs_right[0])
    btn = Button(ax_btn, 'Reset Simulation', color="#2b4b77", hovercolor="#3d6aa6")
    btn.label.set_color("white")
    
    def reset_simulation(event):
        new_pos = hex_grid(N_PENGUINS)
        for i, pg in enumerate(penguins):
            pg.location = new_pos[i]
            pg.heat = np.random.uniform(0.3, 1.0)
            pg.velocity = [0, 0]
        for h in histories:
            h.clear()
            
    btn.on_clicked(reset_simulation)

    # --- Click Interaction ---
    def on_click(event):
        if event.inaxes == ax_sim:
            config['TARGET_X'] = event.xdata
            config['TARGET_Y'] = event.ydata

    fig.canvas.mpl_connect('button_press_event', on_click)

    # Sliders
    slider_keys = list(config.keys())
    sliders = {}
    for i, key in enumerate(slider_keys):
        # Adjusted y-positioning slightly to fit under the new layout
        ax_s = fig.add_axes([0.72, 0.22 - (i * 0.035), 0.18, 0.02], facecolor="#1b375c")
        sl = Slider(ax_s, key, 0.0, 1.0, valinit=config[key], color="#ffcc00")
        sl.label.set_color("white"); sl.label.set_fontsize(7)
        sl.valtext.set_color("white"); sl.valtext.set_fontsize(7)
        sl.on_changed(lambda val, k=key: config.update({k: val}))
        sliders[key] = sl
    
    def update(frame):
        heat_transfer(penguins, config)
        applyforce(penguins, config)
        
        locs = np.array([pg.location for pg in penguins])
        vels = np.array([pg.velocity for pg in penguins])
        locs += vels
        
        for i, pg in enumerate(penguins):
            pg.location = locs[i]
            pg.t += 1/60
            
        scat.set_offsets(locs)
        scat.set_array(np.array([pg.heat for pg in penguins]))

        # Metrics
        heat_vals = np.array([pg.heat for pg in penguins])
        histories[0].append(np.std(heat_vals))
        
        centroid = np.mean(locs, axis=0)
        dists = np.linalg.norm(locs - centroid, axis=1)
        histories[1].append(np.mean(dists))
        
        ke = np.sum(np.linalg.norm(vels, axis=1))/len(penguins)
        histories[2].append(ke)

        for i in range(3):
            if len(histories[i]) > 200: histories[i].pop(0)
            lines[i].set_data(range(len(histories[i])), histories[i])
            axes[i].set_xlim(0, 200)
            # Use auto-scaling for y-axis
            if len(histories[i]) > 0:
                axes[i].set_ylim(min(histories[i]) - 0.1, max(histories[i]) + 0.1)

        return [scat] + lines

    ani = FuncAnimation(fig, update, interval=60, blit=False, cache_frame_data=False)
    plt.show()

if __name__ == "__main__":
    main()