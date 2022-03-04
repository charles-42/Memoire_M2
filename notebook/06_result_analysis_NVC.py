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


def select_best_few_shot(pred_list):
    """ determine the answer of the model as the conclusion with the 
    highest probability
    """
    
    choice_form = ['Aac', 'Aca', 'Iac', 'Ica', 'Oac', 'Oca', 'Eac', 'Eca', 'NVC']
    
    if isinstance(pred_list,str):
        pred_list = ast.literal_eval(pred_list)
    
    conclusion_list = []
    
    # we want to know if entail is the higher probability for one of the choices
    for i in pred_list[:-1]:
        if i[2] > i[1] and i[2] > i[1]:
            conclusion_list.append("entail")
        else :
            conclusion_list.append("no_entail")
    
    if "entail" not in conclusion_list:
        # if for any choice entail is the higher probability
        return "NVC"        
    else:
        # we select only entail probability
        pred_list = [c for a,b,c in pred_list[:-1]]

    
    max_value = max(pred_list)
    max_index = pred_list.index(max_value)
    # if max_value <= 1:
    #     max_value *= 100
    return choice_form[max_index]



# We get the answer of each mode

df_final['best_few_shot'] = df_final.choice_mnli_pred.apply(lambda x: select_best_few_shot(x))
# On détermine si les réponses sont valides ou non



df_final['few_shot_result'] = df_final[["task_form","best_few_shot"]].apply(lambda x:  x[1] in table_de_verite[x[0]], axis=1)

#df_final['few_shot_result'] = df_final[["task","best_few_shot"]].apply(lambda x:  x[1] in sy.Syllogism(x[0]).conclusion, axis=1)

df_final["succes"]= df_final.few_shot_result.apply(lambda x : 1 if x==True else 0 )


df_result_few_shot = df_final[['task_form', 'succes']].groupby(['task_form']).mean().merge(df_final[['task_form', 'succes']].groupby(['task_form']).count(), on="task_form")
df_result_few_shot = df_result_few_shot.drop(["succes_y"], axis=1)

df_result_few_shot = df_result_few_shot.rename(columns={"succes_x": "succes_mnli"})

df_result_few_shot.to_csv("./data/results/result_mnli.csv")