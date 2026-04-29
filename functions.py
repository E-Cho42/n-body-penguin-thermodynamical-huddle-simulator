import numpy as np
import random as rd

# These are now default values, but the logic will use the dict passed in
def heat_transfer(penguins, config):
    for i, pg in enumerate(penguins):
        neighbours = 0
        for j, other in enumerate(penguins):
            if i == j: continue
            dx = pg.location[0] - other.location[0]
            dy = pg.location[1] - other.location[1]
            if np.sqrt(dx**2 + dy**2) < 1.0: # CLOSE_DIST
                neighbours += 1
        

        dist_to_centre = np.sqrt(pg.location[0]**2 + pg.location[1]**2)
        boundary_penalty = 0.002 * dist_to_centre

        # Using config dictionary
        if neighbours == 0:
            pg.heat += config['HEAT_GAIN'] * neighbours - config['HEAT_LOSS'] - boundary_penalty
        else: 
            pg.heat += config['HEAT_GAIN'] * neighbours - config['HEAT_LOSS'] - boundary_penalty
        pg.heat = max(0.0, min(1.0, pg.heat))

def applyforce(penguins, config):
    for pg in penguins:
        # --- 1. Movement Logic (Target-based) ---
        # We calculate the direction to the center (0,0)
        target = np.array([0.0, 0.0])
        pos = np.array(pg.location)
        diff = target - pos
        dist_to_center = np.linalg.norm(diff)
        
        if dist_to_center > 0.1:
            # Normalize the direction vector
            direction_unit = diff / dist_to_center
            
            if pg.heat < 0.3:
                # Cold penguins: head inward
                pg.velocity[0] += direction_unit[0] * 0.1 
                pg.velocity[1] += direction_unit[1] * 0.1 
            elif pg.heat > 0.99:
                # Hot penguins: head outward 
                pg.velocity[0] -= direction_unit[0] * 0.08 + pg.dircetion * .05
                pg.velocity[1] -= direction_unit[1] * 0.08 -.05

        # --- 2. Separation Logic (Fluid Inverse-Square) 
        for other in penguins:
            if pg == other: continue
            
            dx = pg.location[0] - other.location[0]
            dy = pg.location[1] - other.location[1]
            dist_sq = dx**2 + dy**2
            
            # Using squared distance for the check is faster
            if dist_sq < config['SEPARATION_DIST']**2 and dist_sq > 0.01:
                dist = np.sqrt(dist_sq)
                # Force gets much stronger as they get closer
                push = config['SEPARATION_FORCE'] / dist
                pg.velocity[0] += (dx / dist) * push
                pg.velocity[1] += (dy / dist) * push

        # --- 3. Jitter (Brownian Motion) ---
        jitter = 0.05
        pg.velocity[0] += np.random.uniform(-jitter, jitter)
        pg.velocity[1] += np.random.uniform(-jitter, jitter)

        # --- 4. Damping and Speed Limits ---
        pg.velocity[0] *= config['DAMPING']
        pg.velocity[1] *= config['DAMPING']

        speed = np.sqrt(pg.velocity[0]**2 + pg.velocity[1]**2)
        if speed > config['MAX_SPEED']:
            pg.velocity[0] *= (config['MAX_SPEED'] / speed)
            pg.velocity[1] *= (config['MAX_SPEED'] / speed)
            
            
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