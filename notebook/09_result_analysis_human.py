
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


df_final["succes_human"]= df_final.human_response.apply(lambda x : 1 if ast.literal_eval(x)[1]==True else 0 )

# On calcul le taux de succès de chaque modèle pour chaque
df_result_human = df_final[['task_form', 'succes_human']].groupby(['task_form']).mean().merge(df_final[['task_form', 'succes_human']].groupby(['task_form']).count(), on="task_form")
df_result_human = df_result_human.drop(["succes_human_y"], axis=1)

df_result_human = df_result_human.rename(columns={"succes_human_x": "succes_human"})
df_result_human.to_csv("./data/results/result_human.csv")