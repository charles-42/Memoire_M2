import pandas as pd
import notebook.syllogism as sy 

df1 = pd.read_csv("./data/ressources/Ragni2016.csv")
df2 = pd.read_csv("./data/ressources/Veser2018.csv")

###----------- Preparation des données en vue de l'analyse

#########----- Création de l'id unique regroupant id et sequence
df1 = df1.assign(id_seqTrue=lambda df: df1.id.apply(str).str.cat(df1.sequence.apply(str),sep="_") + "_R")
df2 = df2.assign(id_seqTrue=lambda df: df2.id.apply(str).str.cat(df2.sequence.apply(str),sep="_") + "_V")


#########----- Concaténation des deux tables

df_concat = pd.concat([df1,df2])


#########----- Pour ne pas entrainer deux fois un même syllogisme, on supprimer les doublons
df_drop = df_concat.drop_duplicates(subset=['task','choices'])
df_drop['sentenced'] = df_drop.task.apply(lambda x : sy.Syllogism(x).sentenced)
df_drop = df_drop[["sentenced","id_seqTrue"]]
# print(df_drop.shape)
# print(df_drop.head())
print(df_drop.columns)

df_simple = pd.read_csv("./data/intermediate/df_trained_union_old.csv")


df_new =  pd.merge(df_simple, df_drop, on="sentenced",how="inner")
df_new = df_new[['id_seqTrue', 'sentenced', 'choice_str', 'choice_pred', 'choice_union_pred']]
df_new = df_new.rename(columns={"id_seqTrue": "id_seq"})


print(df_new.shape)
print(df_new.columns)
print(df_new.head(10))
print(df_new.id_seq.nunique())
df_new.to_csv("./data/intermediate/df_trained_union.csv" ,index=False)