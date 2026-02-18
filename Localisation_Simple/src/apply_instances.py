from PLS_Solveur import *
from PLSR_Solveur import *
from Dual_Solveur import *
from Heuristic1 import *
from solve import *
from utils import *
import concurrent.futures
import os
import re

path_to_json = "../res/res.json"

dos = "../data/"

with open(path_to_json, "w", encoding="utf-8") as f:
    json.dump({}, f, indent=4)

folders = [name for name in os.listdir(dos)
           if os.path.isdir(os.path.join(dos, name))]

print(folders)

folders.reverse()
print(folders)

for folder in folders:
    match = re.search(r'l(\d+)_', folder)
    distance = int(match.group(1))

    path = Path(dos) / folder

    def natural_key(p):
        # extrait tous les nombres dans le nom
        numbers = re.findall(r'\d+', p.name)
        return tuple(int(n) for n in numbers)


    for file in sorted(path.glob("*.json"), key=natural_key):
        #print(file)

        # PLS
        X, Y, cost, exec_time = pls_solveur(file,distance)

        with open(path_to_json, "r", encoding="utf-8") as f:
            dico = json.load(f)
            #print("\n\n\n\n\n\n\n")
            #print(dico)
            #print("\n\n\n\n\n\n\n")
            dico.setdefault("PLS", {}) \
                .setdefault(file.parent.name, {}) \
                .setdefault(file.name, {}) \
                .setdefault("cost", cost)
            dico["PLS"][file.parent.name][file.name].setdefault("time", exec_time)

        with open(path_to_json, "w", encoding="utf-8") as f:
            json.dump(dico, f, indent=4)

        # PLSR
        X, Y, cost, exec_time = plsr_solveur(file,distance)

        with open(path_to_json, "r", encoding="utf-8") as f:
            dico = json.load(f)
            dico.setdefault("PLSR", {}) \
                .setdefault(file.parent.name, {}) \
                .setdefault(file.name, {}) \
                .setdefault("cost", cost)
            dico["PLSR"][file.parent.name][file.name].setdefault("time", exec_time)

        with open(path_to_json, "w", encoding="utf-8") as f:
            json.dump(dico, f, indent=4)

        # Heuristic1

        W, V, cost, exec_time = dual_solveur(file, distance)
        n, m, C, F = load_instance_numpy(file, distance)
        X, Y, cost, exec_time = heuristic1(C, F, X, Y, V, W, n, m)

        with open(path_to_json, "r", encoding="utf-8") as f:
            dico = json.load(f)
            dico.setdefault("Heuristic1", {}) \
                .setdefault(file.parent.name, {}) \
                .setdefault(file.name, {}) \
                .setdefault("cost", cost)
            dico["Heuristic1"][file.parent.name][file.name].setdefault("time", exec_time)

        with open(path_to_json, "w", encoding="utf-8") as f:
            json.dump(dico, f, indent=4)

        # Heuristic2
        """
        instance = load_instance_json(file)
        affectation, opened_warehouses, cost, exec_time = heuristic2(instance)

        with open(path_to_json, "r", encoding="utf-8") as f:
            dico = json.load(f)
            dico.setdefault("Heuristic2", {}) \
                .setdefault(file.parent.name, {}) \
                .setdefault(file.name, {}) \
                .setdefault("cost", cost)
            dico["Heuristic2"][file.parent.name][file.name].setdefault("time", exec_time)

        with open(path_to_json, "w", encoding="utf-8") as f:
            json.dump(dico, f, indent=4)
        """

