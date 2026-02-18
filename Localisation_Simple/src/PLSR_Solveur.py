import json
import numpy as np
from pathlib import Path
import pulp as pl
from utils import *

def plsr_solveur(path):
    n, m, C, F = load_instance_numpy(path)
    print(C)

    I = [i for i in range(n)]
    J = [j for j in range(m)]

    # Model
    prob = pl.LpProblem("PLSR", pl.LpMinimize)

    # Variables
    x = pl.LpVariable.dicts("x", (I, J), lowBound=0)
    y = pl.LpVariable.dicts("y", J, lowBound=0)

    # Objective Function
    prob += pl.lpSum(C[i, j] * x[i][j] for i in I for j in J) + pl.lpSum(F[j] * y[j] for j in J)

    for i in I:
        prob += pl.lpSum(x[i][j] for j in J) == 1, f"A[{i}]"

    for i in I :
        for j in J:
            prob += x[i][j] <= y[j], f"B[{i},{j}]"

    print("n =", n, "m =", m)
    print("Shape C =", C.shape)
    print("F =", F)
    print("C[0,0] =", C[0,0])
    # print(C)

    print("\nSOLVEUR\n")
    path_to_cplex = "C:\Program Files\IBM\ILOG\CPLEX_Studio2211\cplex\\bin\\x64_win64\cplex.exe"
    solver = pl.CPLEX_CMD(path=path_to_cplex, msg=True)
    status = prob.solve(solver)

    print("Status : ", pl.LpStatus[status])

    val_obj = pl.value(prob.objective)

    for v in prob.variables():
        if v.varValue > 0:
            print(v.name, "=", v.varValue)

    print("Statut :", pl.LpStatus[prob.status])
    print("x =", x.values())
    print("y =", y.values())
    print("Opt =", pl.value(prob.objective))

    X = np.zeros((n,m))
    Y = np.zeros(m)
    for i in I:
        for j in J:
            X[i][j] = x[i][j].varValue
            Y[j] = y[j].varValue

    cost = pl.value(prob.objective)

    return X, Y, int(cost)

