import numpy as np
import random

def generate_seeds(num_seeds, coord_limit): 
    points = []
    for _ in range(num_seeds): 
        x = random.randint(0, coord_limit)
        y = random.randint(0, coord_limit)
        points.append([x, y])
    return np.array(points)

seeds = generate_seeds(100, 100)