# Penguin Huddle Simulator

A physics-based multi-agent simulation of emperor penguin thermoregulation. Emperor penguins survive Antarctic winters by forming dense huddles — individuals on the cold exterior gradually rotate inward as they lose heat, while warm interior penguins push outward. This simulator models that emergent collective behavior from the bottom up, using thermal state updates, n-body separation forces, and velocity-based steering across 150 autonomous agents.

---

## How It Works

Each penguin agent carries a heat value in [0, 1] and a position and velocity in 2D space. Every timestep, three physical processes update the system:

**1. Thermal Exchange**

Each penguin loses heat passively and gains heat proportional to the number of neighbors within a fixed interaction radius (1.0 units). Penguins farther from the huddle centre incur an additional boundary heat penalty proportional to their distance from the origin:

```
heat += HEAT_GAIN * neighbours - HEAT_LOSS - 0.002 * dist_to_centre
heat = clamp(heat, 0, 1)
```

This means isolated or exposed penguins cool down, while densely packed penguins warm up — recreating the real thermodynamic gradient observed in emperor penguin huddles.

**2. Steering and Separation Forces**

Each penguin steers toward the huddle centre with a pull strength that depends on its thermal state — cold penguins (heat < 0.3) pull harder toward the centre than warm ones. Hot penguins (heat ≥ 0.8) drift outward laterally, and cold penguins (heat < 0.4) push sideways, producing rotational circulation within the huddle.

Penguins that come too close to each other experience an inverse-distance repulsion force that prevents unphysical overlap:

```
push = SEPARATION_FORCE / dist    (for dist < SEPARATION_DIST)
```

**3. Velocity Dynamics**

Each timestep, a small uniform random perturbation is added to each penguin's velocity (jitter amplitude: ±0.001), simulating low-level stochastic motion. Velocities are then damped by a fixed coefficient and capped at MAX_SPEED to ensure numerical stability.

---

## Architecture

```
.
├── main.py        # Simulation loop, Matplotlib animation, sliders, metrics dashboard
├── functions.py   # Heat transfer, separation forces, steering, hex grid initialization
└── penguin.py     # Agent class: heat, position, velocity, internal clock, drift direction
```

**`penguin.py`** defines the agent. Each penguin stores its thermal state, position vector, velocity vector, internal time counter, and a randomly assigned lateral drift direction (±1) used to produce rotational huddle circulation.

**`functions.py`** contains the physics: heat transfer rules, inverse-distance separation forces, velocity-based steering, uniform jitter, damping, and the hexagonal lattice initialization that places agents in a close-packed starting configuration.

**`main.py`** runs the animation loop using Matplotlib's `FuncAnimation`, renders the scatter plot coloured by heat (plasma colormap), and displays a live metrics dashboard with three real-time graphs.

---

## Live Metrics Dashboard

The right panel tracks three system-level quantities updated every frame:

| Metric | Description |
|--------|-------------|
| Avg Temp | Standard deviation of heat values across all agents |
| Huddle Compactness | Mean distance of all agents from the huddle centroid |
| Colony Agitation Index | Mean speed (kinetic energy per agent) across the colony |

---

## Parameters

All parameters are adjustable via sliders during runtime:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `HEAT_LOSS` | Passive heat loss per timestep | 0.175 |
| `HEAT_GAIN` | Heat gained per neighbor per timestep | 0.02 |
| `SENSITIVITY` | (Reserved for future use) | 0.05 |
| `SEPARATION_FORCE` | Strength of inter-agent repulsion | 0.08 |
| `SEPARATION_DIST` | Radius within which repulsion activates | 0.5 |
| `MAX_SPEED` | Maximum agent velocity | 0.15 |
| `DAMPING` | Velocity damping coefficient per timestep | 0.363 |
| `TARGET_X/Y` | Huddle centre target coordinates | 0.0, 0.0 |

---

## Installation

Requires Python 3.x

```bash
pip install numpy matplotlib
python main.py
```

---

## Biological Basis

Emperor penguin huddling is a well-studied phenomenon in biophysics. Real huddles exhibit slow wave-like motion as penguins on the periphery push inward when cold, displacing interior penguins outward — producing a steady rotational circulation that gives all individuals periodic access to the warm centre. This simulator reproduces that qualitative behavior through purely local agent rules, with no global coordination.