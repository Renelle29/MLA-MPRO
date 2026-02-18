import numpy as np
import time
from PLSR_Solveur import *
from Dual_Solveur import *
from utils import *

def heuristic1(C,F,X,Y,V,W,n,m):
    affected_points = [0 for i in range(len(V))]
    V_bis = np.copy(V)

    clusters = []
    c_sites = []

    start = time.perf_counter()

    while sum(affected_points)!=len(affected_points):
        i_min = np.argmin(V_bis)
        cluster = []

        mask = X[i_min, :] > 0

        sites = np.where(mask)[0]
        site = sites[np.argmin(F[sites])]
        c_sites.append(site)

        C_sub = X[:, sites].sum(axis=1)
        neighbors = np.where(C_sub > 0)[0]

        for neighbor in neighbors:
            if V_bis[neighbor] < np.inf :
                V_bis[neighbor] = np.inf
                affected_points[neighbor] = 1
                cluster += [neighbor]

        clusters.append(cluster)

    X_h = np.zeros((n,m))
    Y_h = np.zeros(m)

    for p in range(len(clusters)):
        cluster = clusters[p]
        site = c_sites[p]
        for client in cluster:
            X_h[client][site] = 1

    for k in c_sites:
        Y_h[k] = 1

    end = time.perf_counter()

    exec_time = end - start

    cost = np.sum(C * X_h) + np.sum(F * Y_h)

    return X_h, Y_h, cost, exec_time

path = "../data/LS_10_10_1000_1.json"

distance = 1
X, Y, cost, exec_time = plsr_solveur(path,distance)
W, V, cost, exec_time = dual_solveur(path,distance)
n, m, C, F = load_instance_numpy(path,distance)

X, Y, cost, exec_time = heuristic1(C,F,X,Y,V,W,n,m)
print(X, Y, cost)




