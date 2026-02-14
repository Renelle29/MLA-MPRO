import numpy as np
import random
import json

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

    return coordinates_n, coordinates_m, f, L, seed

import json

def save_instance_json(coordinates_n, coordinates_m, f, L=None, seed=None):
    
    n = int(len(coordinates_n))
    m = int(len(coordinates_m))
    filename = f"data/LS_{n}_{m}_{L}_{seed}.json"

    data = {
        "n": n,
        "m": m,
        "coordinates_n": coordinates_n.tolist(),
        "coordinates_m": coordinates_m.tolist(),
        "f": list(map(int, f)),
        "meta": {
            "L": L,
            "seed": seed,
            "metric": "manhattan"
        }
    }

    with open(filename, "w") as file:
        json.dump(data, file)

def gen_and_save_manhattan(n, m, L=100, cost_range=range(10, 51), seed=1):

    coordinates_n, coordinates_m, f, L, seed = generate_manhattan(n, m, L, cost_range, seed)

    save_instance_json(coordinates_n, coordinates_m, f, L, seed)