import os
import random
import numpy as np
from utils import *
from PLSR_Solveur import *
from PLS_Solveur import *

def test_instance(path):
    X_plsr, Y_plsr, cost_plsr = plsr_solveur(path)
    X_pls, Y_pls, cost_pls = pls_solveur(path)
    
    print(f"PLSR value: {cost_plsr}")
    print(f"PLS value: {cost_pls}")

def find_fractional_instances():
    
    # Paramètres
    n, m, L = 1000, 100, 1000
    num_instances = 1000
    cost_range = range(300, 700)

    output_dir = "../data/fractional"

    for _ in range(num_instances):
        seed = random.randint(0, 100000)

        coordinates_n, coordinates_m, f, L, seed_used, fractional = generate_points(
            n, m, L=L, cost_range=cost_range, seed=seed, fractional=False
        )

        filename = f"LS_{n}_{m}_{L}_{seed_used}.json"
        path = os.path.join(output_dir, filename)
        save_instance_json(coordinates_n, coordinates_m, f, L, seed_used, fractional=True)

        X, Y, cost = plsr_solveur(path)
        print(X,Y)

        fractional_found = np.any((X > 0) & (X < 1))

        if fractional_found:
            print(f"Seed {seed_used}: fractional solution found, keeping file.")
        else:
            print(f"Seed {seed_used}: all x are binary, deleting file.")
            os.remove(path)

#find_fractional_instances()
path = "../data/integer_l1_frac_solution/LS_100_10_1000_25388.json"
test_instance(path)
