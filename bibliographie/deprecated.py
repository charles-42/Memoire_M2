def calcul_chelma(choice_pred_init,choice_union_pred):
    """ calcul the ratio between the simple prediction 
    (conclusion is the next sentence of the conclusion) and the union """
    
    choice_pred_init = ast.literal_eval(choice_pred_init)
    choice_union_pred = ast.literal_eval(choice_union_pred)
    choice_pred = []
    for i in range(len(choice_pred_init)):
        choice_pred.append(choice_pred_init[i]/choice_union_pred[i])
    return choice_pred

df_union['choice_chelma_pred'] = df_union[["choice_pred","choice_union_pred"]].apply(lambda x: calcul_chelma(x[0],x[1]), axis=1)
df_chelma = df_union[["id_seq","choice_chelma_pred"]]