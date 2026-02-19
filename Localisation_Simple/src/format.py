from utils import *
from PLS_Solveur import *
from PLSR_Solveur import *
import pandas as pd

def format_results(input_path, output_path):
    
    data = load_instance_json(input_path)
    
    PLSR = data["PLSR"]["integer_l1_frac_solution"]
    PLS = data["PLS"]["integer_l1_frac_solution"]
    heuristic1 = data["Heuristic1"]["integer_l1_frac_solution"]
    heuristic2 = data["Heuristic2"]["integer_l1_frac_solution"]
    
    instances = PLSR.keys()
    
    PLS_rows = []
    heuristic1_rows = []
    heuristic2_rows = []
    
    for instance in instances:
        
        PLS_rows.append({
            "Instance": instance,
            "PLSR value": PLSR[instance]["cost"],
            "PLSR time (s)": PLSR[instance]["time"],
            "PLS value": PLS[instance]["cost"],
            "PLS time (s)": PLS[instance]["time"],
            "Saut intégral": f"{round(100 * (PLS[instance]["cost"] - PLSR[instance]["cost"])/PLSR[instance]["cost"],3)}%"
        })
        
        heuristic1_rows.append({
            "Instance": instance,
            "PLS value": PLS[instance]["cost"],
            "PLS time (s)": PLS[instance]["time"],
            "Heur1 value": int(heuristic1[instance]["cost"]),
            "Heur1 time (s)": heuristic1[instance]["time"] + PLSR[instance]["time"],
            "Gap": f"{round(100 * (heuristic1[instance]["cost"] - PLS[instance]["cost"])/PLS[instance]["cost"],2)}%"
        })
        
        heuristic2_rows.append({
            "Instance": instance,
            "PLS value": PLS[instance]["cost"],
            "PLS time (s)": PLS[instance]["time"],
            "Heur2 value": heuristic2[instance]["cost"],
            "Heur2 time (s)": heuristic2[instance]["time"],
            "Gap": f"{round(100 * (heuristic2[instance]["cost"] - PLS[instance]["cost"])/PLS[instance]["cost"],2)}%"
        })
        
    PLS_df = pd.DataFrame(PLS_rows)
    heuristic1_df = pd.DataFrame(heuristic1_rows)
    heuristic2_df = pd.DataFrame(heuristic2_rows)
    
    PLS_latex_table = PLS_df.to_latex(
        index=False,
        float_format="%.3f",
        caption="Comparaison PLS vs PLSR",
        label="tab:comparison",
        column_format="lrrrrr"
    )
    
    heuristic1_latex_table = heuristic1_df.to_latex(
        index=False,
        float_format="%.3f",
        caption="Comparaison Heuristic1 vs PLS",
        label="tab:comparison",
        column_format="lrrrrr"
    )
    
    heuristic2_latex_table = heuristic2_df.to_latex(
        index=False,
        float_format="%.3f",
        caption="Comparaison Heuristic2 vs PLS",
        label="tab:comparison",
        column_format="lrrrrr"
    )

    print(PLS_latex_table.replace("_","\_").replace("%","\%"))
    print(heuristic1_latex_table.replace("_","\_").replace("%","\%"))
    print(heuristic2_latex_table.replace("_","\_").replace("%","\%"))
    
    #path = "../data/integer_l1_frac_solution/LS_100_100_100_54463.json"
    #X, Y, cost, exec_time = pls_solveur(path,1)
    
input_path = "../res/res.json"
output_path = "../res/formatted_res.txt"
format_results(input_path, output_path)
