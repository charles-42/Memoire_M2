# load model pretrained on MNLI
import pandas as pd
from transformers import BartForSequenceClassification, BartTokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-mnli')
model = BartForSequenceClassification.from_pretrained('facebook/bart-large-mnli')

df_train = pd.read_csv("../data/intermediate/df_to_train.csv")

def prediction_MNLI(syllogism,hypothesis):
    """ Calcul probability than hypothesis is the entailment of syllogism

    Args:
        syllogism (str): 
        hypothesis (str): 
    
    Return:
        int:probability that hypothesis is the entailment of the premise
    """
    
    input_ids = tokenizer.encode(syllogism, hypothesis, return_tensors='pt')
    logits = model(input_ids)[0]

    # we throw away "neutral" (dim 1) and take the probability of
    # "entailment" (2) as the probability of the label being true 
    entail_contradiction_logits = logits[:,[0,2]]
    probs = entail_contradiction_logits.softmax(dim=1)
    true_prob = probs[:,1].item() * 100
    return true_prob

import ast
global counter 
counter = 0
def prediction_choice_MNLI(syllogisme,choices):
    """ Calcul the probability for each choice of being the entailment of the syllogism

    Args:
        syllogisme (str)
        choices (list(str))

    Returns:
        list(int): list of probability of true
    """
    global counter 
    counter +=1
    print(counter)
    pred_choice=list()
    choices = ast.literal_eval(choices)
    for c in choices:
        if c =="NVC":
            pred_choice.append(-1)
        else:
            pred_choice.append(prediction_MNLI(syllogisme,c))
    return pred_choice


# On applique les fonctions définies au dataframe
df_train['choice_union_pred'] = df_train[["sentenced","choice_str"]].apply(lambda x: prediction_choice_MNLI(x[0],x[1]), axis=1)
df_train.to_csv("../Data/df2016_test_MNLI.csv" ,index=False)