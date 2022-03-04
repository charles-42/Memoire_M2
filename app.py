import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


st.title('Syllogism resolution')


# Load 10,000 rows of data into the dataframe.
df_valid= pd.read_csv("./data/results/result_valid_30_01_22.csv")
df_valid = df_valid.set_index('task_form')

stat_valid= pd.read_csv("./data/results/valid_mean_04_03_22.csv")
stat_valid = stat_valid.set_index('type')

df_unvalid= pd.read_csv("./data/results/result_unvalid_30_01_22.csv")
df_unvalid = df_unvalid.set_index('task_form')

stat_unvalid= pd.read_csv("./data/results/unvalid_mean_04_03_22.csv")
stat_unvalid = stat_unvalid.set_index('type')


# define the threshold

seuil_simple = st.sidebar.select_slider('seuil bert-base-uncased', options=["0.9999965","0.9999968","0.9999972","0.9999974","0.999996","0.999997"], value= "0.9999965")
seuil_mnli = st.sidebar.select_slider('seuil bart-mnli',  options=["00","03","05","10","20","30","40","50","60","70","80","90"], value = "03")
display_graph = st.sidebar.checkbox('Display graph', value=True)
display_mean = st.sidebar.checkbox('Display means',  value=True)
display_raw = st.sidebar.checkbox('Display raw data',  value=False)



# Result for valid syllogism

valid_filtered_data = df_valid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
stat_valid_filtered = stat_valid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]

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


if display_mean:
    st.caption('Mean')
    st.write(stat_valid_filtered)

if display_raw:
    st.caption('Raw data')
    st.write(valid_filtered_data)


# Result for unvalid syllogism
unvalid_filtered_data = df_unvalid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]
stat_unvalid_filtered = stat_unvalid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]


st.subheader('Unvalid syllogisms')

if display_graph:


    st.caption('Graph')
    fig= plt.figure(figsize=(10, 4))

    if sort_way == 'Human success':
        sns.lineplot(data=unvalid_filtered_data)
    else:
        sns.lineplot(data=unvalid_filtered_data.sort_index())
    st.pyplot(fig)


if display_mean:
    st.caption('Mean')
    st.write(stat_unvalid_filtered)

if display_raw:
    st.caption('Raw data')
    st.write(unvalid_filtered_data)