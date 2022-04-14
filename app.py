import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
#import plotly.figure_factory as ff

"# Syllogism resolution "

with st.expander("See explanation", expanded=True):

    """
    
    Natural Language Processing algorithms that aim to perform tasks related to human language are now achieving impressive results in sentiment analysis, translation or text classification. We seek to understand whether they rely on a logic model to perform these tasks. This model could be formal logic, human "logic" (reconstructed from the training corpus) or a specific logic resulting from the algorithms used.

    To address this problem, we have tested two pre-trained NLP models against a set of 6500 syllogisms belonging to the 64 classical forms. 
    - The first model is a **`bert-base-uncased`** (named simple in the next dataframes and charts). This model is pretrained on a large unlabelled corpus of English data. We used its next sententence prediction function.  So we gave it as input on one side the two premises of the syllogism and on the other side 8 possible conclusions.For each conclusion the model estimates the probability that it is the next sentence. The conclusion with the highest probability is considered as the answer of the algorithm.
    - The second one is a **`facebook/bart-large-mnli`** (also called mnli). This model is pre-trained on the mnli corpus and aims at predicting whether for a given sentence a second sentence is its entailment, its contradiction or is neutral to it. We gave it as input the two premisses and the 8 possible conclusion. The conclusion with the highest "entailment" probability is considered as the answer.

    We also had to study the syllogisms without valid conclusion. It is particularly difficult to make an NLP algorithm predict the absence of valid conclusion. We have explored two ways to tackle this problem. 
    - define a rule such that if the conclusion with the highest probability is below a threshold then the answer is replaced by "Non valid answer".
    - for the mnli algorithm only, if for all conclusion the probability of contradiction or neutral is higher than the probability of entailment then the answer is replaced by "Non valid answer"

    You can explore these different scenarios using the slider. For  mnli, the threshold called "max" corresponds to the second path where we compare the probabilities of entailment, contradiction and neutral
    """



# Load Data


df_valid_aris = pd.read_csv("./data/results/result_similarity_valid.csv")
df_valid_aris = df_valid_aris.set_index('task_form').sort_values(by="succes_human" ,ascending=False)
df_valid_aris = df_valid_aris.rename(columns={"succes_simple_0.9999965": "succes_simple"})

df_unvalid = pd.read_csv("./data/results/result_similarity_unvalid.csv")
df_unvalid = df_unvalid.set_index('task_form').sort_values(by="succes_human" ,ascending=False)
df_unvalid = df_unvalid.rename(columns={"succes_simple_0.9999965": "succes_simple"})

# Chart Options

st.subheader('Chart options')

sort_way = st.radio(
"Sort by",
('Human success', 'Syllogism Form'))

implicatur = st.radio(
"Criteria of validity:",
('Aristotle', 'Frege', 'Only show implicatur'))

# implicatur




if implicatur == 'Frege':
    df_valid = df_valid_aris[df_valid_aris["implicatur"]==False ]
     
elif implicatur == 'Only show implicatur':
    df_valid = df_valid_aris[df_valid_aris["implicatur"]==True]

else:
    df_valid = df_valid_aris




#######--------Valid syllogism----------#########



with st.container():
    st.subheader('Valid syllogisms')
    st.write("We first study the syllogisms that have a valid conclusion")
    
    # bart-large-MNLI

    if sort_way == 'Human success':
        fig = px.line(df_valid, x=df_valid.index, y="succes_human", title="bart-large-mnli algortihm for valid syllogism")

    else:
        fig = px.line(df_valid.sort_index(), x=df_valid.index, y="succes_human", title="bart-large-mnli algortihm for valid syllogisme")
    
    fig.add_scatter(x=df_valid.index, y=df_valid.succes_mnli_00,marker=dict(color="darkorchid" ),name="% Success for bart-large-mnli") # Not what is desired - need a line 
    #fig.add_trace(px.line(df_valid, x=df_valid.index, y="succes_mnli_00",labels={'pop':'population of Canada'}))
    fig.add_bar(x=df_valid.index, y=df_valid.mean_mnli_human_right,marker=dict(color="yellowgreen"), name="% Similarity when human is right")
    fig.add_bar(x=df_valid.index, y=df_valid.mean_mnli_human_false,marker=dict(color="indianred"), name="% Similarity when human is wrong")
    fig.update_layout(barmode='stack')
    #fig.show()
    st.plotly_chart(fig)

    # bert-large-MNLI

    if sort_way == 'Human success':
        fig = px.line(df_valid, x=df_valid.index, y="succes_human", title="BERT algortihm for valid syllogism")

    else:
        fig = px.line(df_valid.sort_index(), x=df_valid.index, y="succes_human", title="BERT algortihm for valid syllogisme")
    
    fig.add_scatter(x=df_valid.index, y=df_valid.succes_simple,marker=dict(color="darkorchid" ),name="% of BERT Success")
    fig.add_bar(x=df_valid.index, y=df_valid.mean_simple_human_right,marker=dict(color="yellowgreen"), name="% Similarity when human is right")
    fig.add_bar(x=df_valid.index, y=df_valid.mean_simple_human_false,marker=dict(color="indianred"), name="% Similarity when human is wrong")
    fig.update_layout(barmode='stack')
    #fig.show()
    st.plotly_chart(fig)


#######--------UnValid syllogism----------#########


with st.container():
    st.subheader('Unvalid syllogisms')
    st.write("We were unable to get the algorithms to predict that the syllogisms did not have a valid answer. We therefore observe in the cases where humans and the algorithm were wrong whether they gave the same answer. ")
    # bart-large-MNLI

    if sort_way == 'Human success':
        fig = px.line(df_unvalid, x=df_unvalid.index, y="succes_human", title="bart-large-mnli algortihm for unvalid syllogism")

    else:
        fig = px.line(df_unvalid.sort_index(), x=df_unvalid.index, y="succes_human", title="bart-large-mnli algortihm for unvalid syllogisme")
    
    fig.add_bar(x=df_unvalid.index, y=df_unvalid.mean_mnli_human_false,marker=dict(color="indianred"), name="% Similarity when human is wrong")
    fig.update_layout(barmode='stack')

    st.plotly_chart(fig)

    # bert-large-MNLI

    if sort_way == 'Human success':
        fig = px.line(df_unvalid, x=df_unvalid.index, y="succes_human", title="BERT algortihm for unvalid syllogism")

    else:
        fig = px.line(df_unvalid.sort_index(), x=df_unvalid.index, y="succes_human", title="BERT algortihm for unvalid syllogisme")
    
    fig.add_bar(x=df_unvalid.index, y=df_unvalid.mean_simple_human_false,marker=dict(color="indianred"), name="% Similarity when human is wrong")
    fig.update_layout(barmode='stack')
    #fig.show()
    st.plotly_chart(fig)