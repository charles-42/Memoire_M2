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

#df_valid = pd.read_csv("./data/results/result_valid_30_01_22.csv")
#df_valid = df_valid.set_index('task_form')
#df_unvalid = pd.read_csv("./data/results/result_unvalid_30_01_22.csv")
#df_unvalid = df_unvalid.set_index('task_form')

df = pd.read_csv("./data/app/df_results.csv")

valid_mean = pd.read_csv("./data/results/valid_mean_04_03_22.csv")
valid_mean = valid_mean.set_index('type')

valid_cor = pd.read_csv("./data/results/valid_cor_04_03_22.csv")


unvalid_mean = pd.read_csv("./data/results/unvalid_mean_04_03_22.csv")
unvalid_mean = unvalid_mean.set_index('type')

unvalid_cor = pd.read_csv("./data/results/unvalid_cor_04_03_22.csv")

similarity_valid = pd.read_csv("./data/results/result_similarity_valid.csv")
similarity_valid = similarity_valid.set_index('task_form').sort_values(by="succes_human" ,ascending=False)

similarity_unvalid = pd.read_csv("./data/results/result_similarity_unvalid.csv")
similarity_unvalid = similarity_unvalid.set_index('task_form').sort_values(by="succes_human" ,ascending=False)

# define the threshold

seuil_simple = st.sidebar.select_slider('seuil bert-base-uncased', options=["0.9999965","0.9999968","0.9999972","0.9999974","0.999996","0.999997"], value= "0.9999965")
seuil_mnli = st.sidebar.select_slider('seuil bart-mnli',  options=["max","00","03","05","10","20","30","40","50","60","70","80","90"], value = "03")
# display_graph = st.sidebar.checkbox('Display error graph', value=True)
# display_mean = st.sidebar.checkbox('Display means',  value=True)
# display_cor = st.sidebar.checkbox('Display correlations',  value=True)
display_similarity_graph = st.sidebar.checkbox('Display similarity graph', value=True)
display_raw = st.sidebar.checkbox('Display raw data',  value=False)


# Chart Options

st.subheader('Chart options')

sort_way = st.radio(
"Sort by",
('Human success', 'Syllogism Form'))

implicatur = st.radio(
"Criteria of validity:",
('Aristotle', 'Frege', 'Only show implicatur'))

# implicatur

if implicatur == 'Aristotle':
    df_valid = df[df["has_conclusion"]==True]
    
    df_unvalid = df[df["has_conclusion"]==False]

if implicatur == 'Frege':
    df_valid = df[df["has_conclusion"]==True and df["implicatur"]!=True ]
    df_unvalid = df[df["has_conclusion"]==False or df["implicatur"]==True ]
     
if implicatur == 'Only show implicatur':
    df_valid = df[df["implicatur"]==True]
    df_unvalid = df
     

df_valid= df_valid.drop(columns=["has_conclusion","implicatur"]).set_index('task_form')
df_unvalid= df_unvalid.drop(columns=["has_conclusion","implicatur"]).set_index('task_form')


#######--------Valid syllogism----------#########

# filters

valid_filtered_data = df_valid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
valid_mean_filtered = valid_mean[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
valid_cor_filtered = valid_cor[[f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]

# display

with st.container():
    st.subheader('Valid syllogisms')
    st.write("We first study the syllogisms that have a valid conclusion")
    
    # Display Graph Valid syllogisme
    st.caption('Error graph')
    fig= plt.figure(figsize=(10, 4))

    if sort_way == 'Human success':
        sns.lineplot(data=valid_filtered_data, markers=True)
    else:
        sns.lineplot(data=valid_filtered_data.sort_index(), markers=True)
        plt.xticks(rotation=90)
    st.pyplot(fig)

    # Display Correlation Valid syllogisme
    st.caption('Correlation with human answers')
    st.write(valid_cor_filtered)

    # Display Mean Valid syllogisme
    st.caption('Average succes rate by syllogism form')
    st.write(valid_mean_filtered)

    # Display Raw Data syllogisme
    if display_raw:
        st.caption('Raw data')
        st.write(valid_filtered_data)


#######--------Unvalid syllogism----------#########


# filters
if implicatur != 'Only show implicatur':
    unvalid_filtered_data = df_unvalid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
    unvalid_mean_filtered = unvalid_mean[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
    unvalid_cor_filtered = unvalid_cor[[f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]

# Display
if implicatur != 'Only show implicatur':
    with st.container():
        st.subheader('Unvalid syllogisms')


        st.caption('Graph')
        fig= plt.figure(figsize=(10, 4))

        if sort_way == 'Human success':
            sns.lineplot(data=unvalid_filtered_data, markers=True)
        else:
            sns.lineplot(data=unvalid_filtered_data.sort_index(), markers=True)
        plt.xticks(rotation=90)
        st.pyplot(fig)
    
        st.caption('Correlation with human answers')
        st.write(unvalid_cor_filtered)

      
        st.caption('Average succes rate by syllogism form')
        st.write(unvalid_mean_filtered)


        if display_raw:
            st.caption('Raw data')
            st.write(unvalid_filtered_data)


#######--------Similarity----------#########

st.subheader('Study for similarity')

if display_similarity_graph:
    
    st.write("We look when human and algorithm give the same answer. Human and algorith have to choose between 8 possible answer so if the algorithm is random the average similarity rate should be 0.125 ")
    st.write("We start looking for valid syllogism")
    st.caption('Similarity between human response and mnli when human are right and wrong')
    fig= plt.figure(figsize=(10, 4))
    if sort_way == 'Human success':
        
 
        # # creating subplots
        # fig,ax = plt.subplots()
 
        # # plotting columns
        # ax = sns.barplot(x=similarity_valid.index, y=similarity_valid["mean_mnli_human_right"], color='g')
        # ax = sns.barplot(x=similarity_valid.index, y=similarity_valid["mean_mnli_human_false"], color='r')
 
        # # renaming the axes
        # ax.set(xlabel="form", ylabel="percent of similarity")
 
        # # visualizing illustration
        # st.pyplot(fig, clear_figure=True)
        
        #sns.lineplot(data=similarity_valid[["mean_mnli_human_right","mean_mnli_human_false","succes_human"]], palette=["g","r","b"])
        #st.bar_chart(data=similarity_valid[["mean_mnli_human_right","mean_mnli_human_false"]])    
    
        fig = px.line(similarity_valid, x=similarity_valid.index, y="succes_human",
             labels={'pop':'population of Canada'})
        fig.add_bar(x=similarity_valid.index, y=similarity_valid.mean_mnli_human_right, name="Last year")
        fig.add_bar(x=similarity_valid.index, y=similarity_valid.mean_mnli_human_false, name="Last year")
        fig.update_layout(barmode='stack')
        #fig.show()
        st.plotly_chart(fig)
    
    else:
        sns.lineplot(data=similarity_valid[["mean_mnli_human_right","mean_mnli_human_false","succes_human"]].sort_index(), palette=["g","r","b"])  


    st.caption('Similarity between human response and the simple moddle when human are right and wrong')
    fig= plt.figure(figsize=(10, 4))
    if sort_way == 'Human success':
        sns.lineplot(data=similarity_valid[["mean_simple_human_right","mean_simple_human_false","succes_human"]], palette=["g","r","b"])
    else:
        sns.lineplot(data=similarity_valid[["mean_simple_human_right","mean_simple_human_false","succes_human"]].sort_index(), palette=["g","r","b"])  
    st.pyplot(fig)

    st.write("We look now for unvalid syllogism. We haven't use the threshold so the algorithme is never right (answer: No Valid Conclusion")
    st.caption('Similarity between human response and mnli when human are right and wrong')
    fig= plt.figure(figsize=(10, 4))
    if sort_way == 'Human success':
        sns.lineplot(data=similarity_unvalid[["mean_mnli_human_right","mean_mnli_human_false","succes_human"]], palette=["g","r","b"])
    else:
        sns.lineplot(data=similarity_unvalid[["mean_mnli_human_right","mean_mnli_human_false","succes_human"]].sort_index(), palette=["g","r","b"])  
    st.pyplot(fig)

    st.caption('Similarity between human response and the simple moddle when human are right and wrong')
    fig= plt.figure(figsize=(10, 4))
    if sort_way == 'Human success':
        sns.lineplot(data=similarity_unvalid[["mean_simple_human_right","mean_simple_human_false","succes_human"]], palette=["g","r","b"])
    else:
        sns.lineplot(data=similarity_unvalid[["mean_simple_human_right","mean_simple_human_false","succes_human"]].sort_index(), palette=["g","r","b"])  
    st.pyplot(fig)