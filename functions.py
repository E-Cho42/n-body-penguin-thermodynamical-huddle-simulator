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
    
    # Extract target from config
    #target = np.array([config.get('TARGET_X', 0.0), config.get('TARGET_Y', 0.0)])
    
    target = [0,0]
    
    for pg in penguins:
        # --- 1. Movement Logic (Steering Toward Target) ---
        pos = np.array(pg.location)
        diff = target - pos
        dist_to_target = np.linalg.norm(diff)
        
        if dist_to_target > 0.1:
            direction = diff / dist_to_target
            pull_strength = 0.08 if pg.heat < 0.3 else 0.04
            pg.velocity += direction * pull_strength
            if pg.heat >= .8:
                if pg.dircetion == -1:
                    pg.velocity += [-.01,.04]
                else:
                    pg.velocity += [.01,.04]
            elif pg.heat < .4:
                if pg.dircetion == -1:
                    pg.velocity += [-.03,.0]
                else:
                    pg.velocity += [.03,.0]
                

        # --- 2. Separation Logic (Fluid Inverse-Square) ---
        for other in penguins:
            if pg == other: continue
            
            dx = pg.location[0] - other.location[0]
            dy = pg.location[1] - other.location[1]
            dist_sq = dx**2 + dy**2
            
            if dist_sq < config['SEPARATION_DIST']**2 and dist_sq > 0.01:
                dist = np.sqrt(dist_sq)
                push = config['SEPARATION_FORCE'] / dist
                pg.velocity[0] += (dx / dist) * push
                pg.velocity[1] += (dy / dist) * push

        # --- 3. Jitter (Brownian Motion) ---
        jitter = 0.001
        pg.velocity[0] += np.random.uniform(-jitter, jitter)
        pg.velocity[1] += np.random.uniform(-jitter, jitter)

        # --- 4. Damping and Speed Limits ---
        pg.velocity[0] *= config['DAMPING']
        pg.velocity[1] *= config['DAMPING']

        speed = np.linalg.norm(pg.velocity)
        if speed > config['MAX_SPEED']:
            pg.velocity = (pg.velocity / speed) * config['MAX_SPEED']
                        
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

