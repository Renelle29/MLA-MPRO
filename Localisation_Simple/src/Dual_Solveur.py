import json
import time
import numpy as np
from pathlib import Path
import pulp as pl
from utils import *

def dual_solveur(path,distance):
    n, m, C, F = load_instance_numpy(path,distance)

    I = [i for i in range(n)]
    J = [j for j in range(m)]

    # Model
    prob = pl.LpProblem("D", pl.LpMaximize)

    # Variables
    w = pl.LpVariable.dicts("w", (I, J), lowBound=0)
    v = pl.LpVariable.dicts("v", I, lowBound=0)

    # Objective Function
    prob += pl.lpSum(v[i] for i in I)

    for i in I :
        for j in J:
            prob += v[i] - w[i][j] <= C[i,j]

    for j in J:
        prob += pl.lpSum(w[i][j] for i in I) <= F[j]

    print("n =", n, "m =", m)
    print("Shape C =", C.shape)
    print("F =", F)
    print("C[0,0] =", C[0,0])
    # print(C)

    print("\nSOLVEUR\n")
    path_to_cplex = "C:\Program Files\IBM\ILOG\CPLEX_Studio2211\cplex\\bin\\x64_win64\cplex.exe"
    solver = pl.CPLEX_CMD(path=path_to_cplex, msg=True)
    
    start = time.perf_counter()
    status = prob.solve(solver)
    end = time.perf_counter()

    exec_time = end - start

    print("Status : ", pl.LpStatus[status])

    val_obj = pl.value(prob.objective)

    for var in prob.variables():
        if var.varValue > 0:
            print(var.name, "=", var.varValue)

    print("Statut :", pl.LpStatus[prob.status])
    print("v =", v.values())
    print("w =", w.values())
    print("Opt =", pl.value(prob.objective))

    W = np.zeros((n, m))
    V = np.zeros(n)
    for i in I:
        V[i] = v[i].varValue
        for j in J:
            W[i][j] = w[i][j].varValue

    cost = pl.value(prob.objective)

    return W, V, int(cost), exec_time


path = "../data/LS_10_10_1000_1.json"

distance = 1
W, V, cost, exec_time = dual_solveur(path,distance)
print(W, V, cost)