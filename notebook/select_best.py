from utils import choice_form
import ast

def bert(pred_list,seuil):
    """ determine the answer of the model as the conclusion with the 
    highest probability
    """
    if isinstance(pred_list,str):
        pred_list = ast.literal_eval(pred_list)
    
    
    max_value = max(pred_list)
    
    if max_value >= seuil:
        return pred_list.index(max_value)
    else:
        return 8



def mnli(pred_list,seuil):
    """ determine the answer of the model as the conclusion with the 
    highest probability
    """
    if isinstance(pred_list,str):
        pred_list = ast.literal_eval(pred_list)
    
    # if for every choice, prob contradiction or neutre > prob entail we return NVC
    for i in pred_list[:-1]:
        if i[2] > i[1] and i[2] > i[1]:
            break
    
    
    # we select only entail probability
    pred_list = [c for a,b,c in pred_list[:-1]]
    
    max_value = max(pred_list)
    
    if max_value >= seuil:
        return pred_list.index(max_value)
    else:
        return 8



def mnli_3_options(pred_list):
    """ determine the answer of the model as the conclusion with the 
    highest probability
    """
    
    if isinstance(pred_list,str):
        pred_list = ast.literal_eval(pred_list)
    
    conclusion_list = []
    
    # we want to know if entail is the higher probability for one of the choices
    for i in pred_list[:-1]:
        if i[2] > i[1] and i[2] > i[0]:
            conclusion_list.append("entail")
        else :
            conclusion_list.append("no_entail")
    
    if "entail" not in conclusion_list:
        # if for any choice entail is the higher probability
        return 8       
    else:
        # we select only entail probability
        pred_list = [c for a,b,c in pred_list[:-1]]

    
    max_value = max(pred_list)
    max_index = pred_list.index(max_value)

    return max_index

def few_shot(prediction,choices):
    """ determine the answer of the model as the conclusion with the 
    highest probability
    """
    if len(str(prediction))<4: #Hack pas très beau pour gérer les nan
        return -2
    # We clean the prediction
    prediction = prediction[1:]
    if isinstance(choices,str):
        choices = ast.literal_eval(choices)
    
    for conclusion in choices:
        if prediction == conclusion:
            return choices.index(prediction)
        
    return -1  