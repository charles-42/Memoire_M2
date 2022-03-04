import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


st.title('Syllogism resolution')


# Load 10,000 rows of data into the dataframe.
df_valid= pd.read_csv("./data/results/result_valid_30_01_22.csv")
df_valid = df_valid.set_index('task_form')

valid_mean= pd.read_csv("./data/results/valid_mean_04_03_22.csv")
valid_mean = valid_mean.set_index('type')

valid_cor= pd.read_csv("./data/results/valid_cor_04_03_22.csv")

df_unvalid= pd.read_csv("./data/results/result_unvalid_30_01_22.csv")
df_unvalid = df_unvalid.set_index('task_form')

unvalid_mean= pd.read_csv("./data/results/unvalid_mean_04_03_22.csv")
unvalid_mean = unvalid_mean.set_index('type')

unvalid_cor= pd.read_csv("./data/results/unvalid_cor_04_03_22.csv")


# define the threshold

seuil_simple = st.sidebar.select_slider('seuil bert-base-uncased', options=["0.9999965","0.9999968","0.9999972","0.9999974","0.999996","0.999997"], value= "0.9999965")
seuil_mnli = st.sidebar.select_slider('seuil bart-mnli',  options=["max","00","03","05","10","20","30","40","50","60","70","80","90"], value = "03")
display_graph = st.sidebar.checkbox('Display graph', value=True)
display_mean = st.sidebar.checkbox('Display means',  value=True)
display_cor = st.sidebar.checkbox('Display correlations',  value=True)
display_raw = st.sidebar.checkbox('Display raw data',  value=False)



# Result for valid syllogism

valid_filtered_data = df_valid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
valid_mean_filtered = valid_mean[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
valid_cor_filtered = valid_cor[[f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]

if display_graph:
    sort_way = st.radio(
     "Sort by",
     ('Human success', 'Syllogism Form'))

st.subheader('Valid syllogisms')

if display_graph:

    st.caption('Graph')
    fig= plt.figure(figsize=(10, 4))

    if sort_way == 'Human success':
        sns.lineplot(data=valid_filtered_data)
    else:
        sns.lineplot(data=valid_filtered_data.sort_index())
    st.pyplot(fig)

if display_cor:
    st.caption('Correlation with human answers')
    st.write(valid_cor_filtered)

if display_mean:
    st.caption('Mean')
    st.write(valid_mean_filtered)

if display_raw:
    st.caption('Raw data')
    st.write(valid_filtered_data)


# Result for unvalid syllogism
unvalid_filtered_data = df_unvalid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
unvalid_mean_filtered = unvalid_mean[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
unvalid_cor_filtered = unvalid_cor[[f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]

st.subheader('Unvalid syllogisms')

if display_graph:


    st.caption('Graph')
    fig= plt.figure(figsize=(10, 4))

    if sort_way == 'Human success':
        sns.lineplot(data=unvalid_filtered_data)
    else:
        sns.lineplot(data=unvalid_filtered_data.sort_index())
    st.pyplot(fig)

if display_cor:
    st.caption('Correlation with human answers')
    st.write(unvalid_cor_filtered)

if display_mean:
    st.caption('Mean')
    st.write(unvalid_mean_filtered)


if display_raw:
    st.caption('Raw data')
    st.write(unvalid_filtered_data)