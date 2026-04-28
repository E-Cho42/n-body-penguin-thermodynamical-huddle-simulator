import numpy as np

# These are now default values, but the logic will use the dict passed in
def heat_transfer(penguins, config):
    for i, pg in enumerate(penguins):
        neighbours = 0
        for j, other in enumerate(penguins):
            if i == j: continue
            dx = pg.location[0] - other.location[0]
            dy = pg.location[1] - other.location[1]
            if np.sqrt(dx**2 + dy**2) < 1.2: # CLOSE_DIST
                neighbours += 1

        dist_to_centre = np.sqrt(pg.location[0]**2 + pg.location[1]**2)
        boundary_penalty = 0.002 * dist_to_centre

        # Using config dictionary
        pg.heat += config['HEAT_GAIN'] * neighbours - config['HEAT_LOSS'] - boundary_penalty
        pg.heat = max(0.0, min(1.0, pg.heat))

def applyforce(penguins, config):
    for pg in penguins:
        # --- 1. Movement Logic (Your Heat Code) ---
        if pg.heat < 0.5:
            # Move toward center (0,0)
            pg.velocity[0] -= pg.location[0] * 0.005
            pg.velocity[1] -= pg.location[1] * 0.005
        elif pg.heat > 0.7:
            # Move away from center (0,0)
            pg.velocity[0] += pg.location[0] * 0.005
            pg.velocity[1] += pg.location[1] * 0.005
            
        # --- 2. Separation Logic (Don't touch) ---
        for other in penguins:
            if pg == other: continue
            
            dx = pg.location[0] - other.location[0]
            dy = pg.location[1] - other.location[1]
            dist = np.sqrt(dx**2 + dy**2)
            
            # If within separation distance, push away
            if dist < config['SEPARATION_DIST'] and dist > 0.01:
                # Add force proportional to how close they are
                pg.velocity[0] += (dx / dist) * config['SEPARATION_FORCE']
                pg.velocity[1] += (dy / dist) * config['SEPARATION_FORCE']

        # --- 3. Damping and Speed Limits ---
        # Apply Damping
        pg.velocity[0] *= config['DAMPING']
        pg.velocity[1] *= config['DAMPING']

        # Speed limit to keep physics stable
        speed = np.sqrt(pg.velocity[0]**2 + pg.velocity[1]**2)
        if speed > config['MAX_SPEED']:
            pg.velocity[0] *= (config['MAX_SPEED'] / speed)
            pg.velocity[1] *= (config['MAX_SPEED'] / speed)