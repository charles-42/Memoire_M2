table_de_verite = { "AA1":["Aac", "Iac", "Ica"], "AA2":["Aca", "Iac", "Ica"], "AA3":["NVC"], "AA4":["Iac", "Ica"],
                    "AI1":["NVC"], "AI2":["Iac", "Ica"], "AI3":["NVC"], "AI4":["Iac", "Ica"],
                    "AE1":["Eac", "Eca", "Oac", "Oca"], "AE2":["Oac"], "AE3":["Eac", "Eca", "Oac", "Oca"], "AE4":["Oac"],
                    "AO1":["NVC"], "AO2":["NVC"], "AO3":["Oca"], "AO4":["Oac"],  
                    "IA1":["Iac", "Oca"], "IA2":["NVC"], "IA3":["NVC"], "IA4":["Iac", "Oca"],
                    "IE1":["Oac"], "IE2":["Oac"], "IE3":["Oac"], "IE4":["Oac"], 
                    "II1":["NVC"], "II2":["NVC"], "II3":["NVC"], "II4":["NVC"],
                    "IO1":["NVC"], "IO2":["NVC"], "IO3":["NVC"], "IO4":["NVC"],                     
                    "EA1":["Oca"], "EA2":["Eac", "Eca", "Oac", "Oca"], "EA3":["Eac", "Eca", "Oac", "Oca"], "EA4":["Oca"],
                    "EI1":["Oca"], "EI2":["Oca"], "EI3":["Oca"], "EI4":["Oca"], 
                    "EE1":["NVC"], "EE2":["NVC"], "EE3":["NVC"], "EE4":["NVC"],
                    "EO1":["NVC"], "EO2":["NVC"], "EO3":["NVC"], "EO4":["NVC"],
                    "OA1":["NVC"], "OA2":["NVC"], "OA3":["NVC"], "OA4":["NVC"],
                    "OE1":["NVC"], "OE2":["NVC"], "OE3":["NVC"], "OE4":["NVC"],
                    "OO1":["NVC"], "OO2":["NVC"], "OO3":["NVC"], "OO4":["NVC"],
                    "OI1":["NVC"], "OI2":["NVC"], "OI3":["NVC"], "OI4":["NVC"]
                    }

import ast
import pandas as pd
import syllogism as sy


df_final = pd.read_csv("./data/intermediate/df_merge_results.csv")


import ast

def select_best(pred_list,seuil, few_shot=False):
    """ determine the answer of the model as the conclusion with the 
    highest probability
    """
    choice_form = ['Aac', 'Aca', 'Iac', 'Ica', 'Oac', 'Oca', 'Eac', 'Eca', 'NVC']
    if isinstance(pred_list,str):
        pred_list = ast.literal_eval(pred_list)   
    
    if few_shot:
        # we select only entail probability
        pred_list = [c for a,b,c in pred_list[:-1]]
    
    max_value = max(pred_list)
    max_index = pred_list.index(max_value)

    if max_value >= seuil:
        return choice_form[max_index]
    else:
        return "NVC"



def calcul_result(df_final, model, seuil):

    # We get the answer of each mode
    if model == "mnli":
        df_final[f'best_{model}'] = df_final[f"choice_{model}_pred"].apply(lambda x: select_best(x,seuil,True))
    else:
        df_final[f'best_{model}'] = df_final[f"choice_{model}_pred"].apply(lambda x: select_best(x,seuil))

    # On détermine si les réponses sont valides ou non
    df_final[f'result_{model}'] = df_final[["task_form",f'best_{model}']].apply(lambda x:  x[1] in table_de_verite[x[0]], axis=1)

    #df_final['few_shot_result'] = df_final[["task","best_few_shot"]].apply(lambda x:  x[1] in sy.Syllogism(x[0]).conclusion, axis=1)
    df_final[f"succes_{model}"]= df_final[f'result_{model}'].apply(lambda x : 1 if x==True else 0 )


    df_final = df_final[['task_form', f"succes_{model}"]].groupby(['task_form']).mean().merge(df_final[['task_form',  f"succes_{model}"]].groupby(['task_form']).count(), on="task_form")
    
    return df_final.drop([f"succes_{model}_y"], axis=1)


#df = calcul_result(df_final,"mnli", 0)

df = calcul_result(df_final,"mnli", 0)
df = df.rename(columns={"succes_mnli_x": "succes_mnli_00"})
print(df)
df.to_csv("./data/results/result_mnli_00.csv")

