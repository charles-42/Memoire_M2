import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


st.title('Syllogism resolution')

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
df_valid= pd.read_csv("./data/results/result_valid_30_01_22.csv")
df_valid = df_valid.set_index('task_form')

df_unvalid= pd.read_csv("./data/results/result_unvalid_30_01_22.csv")
df_unvalid = df_unvalid.set_index('task_form')


# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

seuil_simple = st.sidebar.select_slider('seuil bert-base-uncased', options=["0.9999965","0.9999968","0.9999972","0.9999974","0.999996","0.999997"], value= "0.9999965")
seuil_mnli = st.sidebar.select_slider('seuil bart-mnli',  options=["00","03","05","10","20","30","40","50","60","70","80","90"], value = "03")


valid_filtered_data = df_valid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]



st.subheader('Valid syllogisms')

fig= plt.figure(figsize=(10, 4))
sns.lineplot(data=valid_filtered_data)
st.pyplot(fig)

unvalid_filtered_data = df_unvalid[["succes_human",f"succes_simple_{seuil_simple}", f"succes_mnli_{seuil_mnli}"]]

st.subheader('Raw data')
st.write(unvalid_filtered_data)

st.subheader('Unvalid syllogisms')

fig= plt.figure(figsize=(10, 4))
sns.lineplot(data=unvalid_filtered_data)
st.pyplot(fig)


st.subheader('Raw data')
st.write(valid_filtered_data)
st.write(unvalid_filtered_data)