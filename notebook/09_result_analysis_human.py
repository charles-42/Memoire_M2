from utils import table_de_verite
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