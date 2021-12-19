import pandas as pd
# package contenant la classe Syllogisme définie dans le cadre du projet 
# qui permet de manipuler les syllogismes et les formats des bdd.
import syllogism as sy 

###----------- Import des bases

df1 = pd.read_csv("../data/ressources/Ragni2016.csv")
df2 = pd.read_csv("../data/ressources/Veser2018.csv")

###----------- Preparation des données en vue de l'analyse

#########----- Concaténation des deux tables

df_concat = pd.concat([df1,df2])

#########----- Pour ne pas entrainer deux fois un même syllogisme, on supprimer les doublons
df_concat = df_concat.drop_duplicates(subset=['task','choices'])

#########----- Création de l'id unique regroupant id et sequence
df_concat = df_concat.assign(id_seq=lambda df: df_concat.id.apply(str).str.cat(df_concat.sequence.apply(str),sep="_"))

#########----- Transformation des données en phrases valides:
df_concat['sentenced'] = df_concat.task.apply(lambda x : sy.Syllogism(x).sentenced)
df_concat['choice_str'] = df_concat[["task","choices"]].apply(lambda x: sy.Syllogism(x[0]).choice_to_str(x[1]), axis=1)

#########----- Selection des colonnes
df_to_train = df_concat[["id_seq","sentenced","choice_str"]]

#########----- enregristement de la base préparée
df_to_train.to_csv("../data/intermediate/df_to_train.csv" ,index=False)


###----------- Création de la base de données pour l'analyse des résultats


df_concat['task_form'] = df_concat.task.apply(lambda x : sy.Syllogism(x).full_form)
df_concat['human_response'] = df_concat[["task","response"]].apply(lambda x: sy.Syllogism(x[0]).evaluate_conclusion(x[1]), axis=1)
df_concat['choice_forme'] = df_concat[["task","choices"]].apply(lambda x: sy.Syllogism(x[0]).choice_to_form(x[1]), axis=1)

df_choice_forme = df_concat[["id_seq","task","task_form","human_response","choice_forme","choices"]]

df_choice_forme.to_csv("../data/intermediate/df_choice_forme.csv" ,index=False)