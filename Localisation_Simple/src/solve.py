import numpy as np

from src.utils import *

def heuristic2(instance):

    n = instance["n"]
    m = instance["m"]

    coordinates_n = instance["coordinates_n"]
    coordinates_m = instance["coordinates_m"]
    f = instance["f"]

    affectation = np.zeros(n) - 1
    opened_warehouses = np.zeros(m)

    v = np.zeros(n)
    w = np.zeros((n,m))

    ### PHASE 1

    while np.any(affectation == -1):
        
        v[affectation == -1] += 1

        for j in range(m):
            for i in range(n):

                if affectation[i] == -1:

                    c = distance(coordinates_n[i], coordinates_m[j])

                    # Event 1
                    if v[i] == c and opened_warehouses[j] == 1:
                        print(f"Affecting {i} to {j} - Event 1")
                        affectation[i] = j

                    # Event 2
                    if v[i] > c and opened_warehouses[j] == 0:
                        w[i,j] += 1

            # Event 3
            already_paid = sum(w[i,j] for i in range(n))
            
            if opened_warehouses[j] == 0 and already_paid == f[j]:
                opened_warehouses[j] = 1

                for i in range(n):
                    if affectation[i] == -1 and v[i] >= distance(coordinates_n[i], coordinates_m[j]):
                        print(f"Affecting {i} to {j} - Event 3")
                        affectation[i] = j

    ### PHASE 2

    # Build graph
    V = [j for j in range(m) if opened_warehouses[j] == 1]
    couples = []

    for j1 in V:
        for j2 in V:
            if j2 > j1:
                for i in range(n):
                    if w[i,j1] > 0 and w[i,j2] > 0:
                        couples.append((j1,j2))
                        break

    # Compute max indep set
    indep_set = []

    for j2 in V:
        indep = True
        for j1 in indep_set:
            if (j1, j2) in couples:
                print(f"{j1} - {j2} in couples")
                indep = False
                break
        if indep:
            indep_set.append(j2)

    # Close some warehouses
    for j in V:
        if j not in indep_set:
            opened_warehouses[j] = 0

    # Reassign clients
    for i in range(n):
        if affectation[i] not in indep_set:
            for j in indep_set:
                if (j, affectation[i]) in couples:
                    print(f"Reaffecting {i} from {affectation[i]} to {j}")
                    affectation[i] = j
                    break

    cost = sum(distance(coordinates_n[i], coordinates_m[int(affectation[i])]) for i in range(n)) + sum(f[j] * opened_warehouses[j] for j in range(m))

    return affectation, opened_warehouses, int(cost)