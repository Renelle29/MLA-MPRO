import numpy as np
import random

def generate_manhattan(n, m, L=100, cost_range=range(10, 51), seed=1):
    random.seed(seed)
    np.random.seed(seed)

    total_points = (L + 1) ** 2
    assert n + m <= total_points, "Grid too small"

    # Generate full lattice
    grid = [(x, y) for x in range(L + 1) for y in range(L + 1)]

    # Sample without replacement
    selected = random.sample(grid, n + m)

    # Split
    coordinates_n = np.array(selected[:n], dtype=int)
    coordinates_m = np.array(selected[n:n + m], dtype=int)

    # Facility opening costs
    f = np.random.choice(list(cost_range), size=m)

    return coordinates_n, coordinates_m, f
