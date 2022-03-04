import pandas as pd
# package contenant la classe Syllogisme définie dans le cadre du projet 
# qui permet de manipuler les syllogismes et les formats des bdd.
import syllogism as sy 

###----------- Import des bases

df1 = pd.read_csv("./data/ressources/Ragni2016.csv")
df2 = pd.read_csv("./data/ressources/Veser2018.csv")

###----------- Preparation des données en vue de l'analyse

#########----- Création de l'id unique regroupant id et sequence
df1 = df1.assign(id_seq=lambda df: df1.id.apply(str).str.cat(df1.sequence.apply(str),sep="_") + "_R")
df2 = df2.assign(id_seq=lambda df: df2.id.apply(str).str.cat(df2.sequence.apply(str),sep="_") + "_V")


#########----- Concaténation des deux tables

df_concat = pd.concat([df1,df2])


#########----- Pour ne pas entrainer deux fois un même syllogisme, on supprimer les doublons
df_drop = df_concat.drop_duplicates(subset=['task','choices'])


#########----- Transformation des données en phrases valides:
df_drop['sentenced'] = df_drop.task.apply(lambda x : sy.Syllogism(x).sentenced)
df_drop['choice_str'] = df_drop[["task","choices"]].apply(lambda x: sy.Syllogism(x[0]).choice_to_str(x[1]), axis=1)

#########----- Selection des colonnes
df_to_train = df_drop[["id_seq","sentenced","choice_str"]]

print(df_to_train.shape)
#########----- enregristement de la base préparée
df_to_train.to_csv("./data/intermediate/df_to_train.csv" ,index=False)


# ###----------- Création de la base de données pour l'analyse des résultats


df_drop['task_form'] = df_drop.task.apply(lambda x : sy.Syllogism(x).full_form)
df_drop['human_response'] = df_drop[["task","response"]].apply(lambda x: sy.Syllogism(x[0]).evaluate_conclusion(x[1]), axis=1)

df_choice_forme = df_drop[["id_seq","task","task_form","choices","human_response"]]

df_choice_forme.to_csv("./data/intermediate/df_choice_forme.csv" ,index=False)

