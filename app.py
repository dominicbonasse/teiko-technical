import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.title("Melanoma Miraclib Trial Dashboard")

if not os.path.exists('frequencies.csv') or not os.path.exists('baseline.csv'):
    st.error("Dashboard data files missing! Please run 'make pipeline' first to generate them.")
else:
    st.header("Baseline Cohort Metrics at t=0")
    df_baseline = pd.read_csv('baseline.csv')

    st.metric("Total Baseline Samples", len(df_baseline))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("Breakdown per Project:")
        st.write(df_baseline['project'].value_counts())
    with col2:
        st.caption("Patient Responses:")
        st.write(df_baseline['response'].value_counts())
    with col3:
        st.caption("Patient Sex Profiles:")
        st.write(df_baseline['sex'].value_counts())

    st.header("Cell Population Relative Frequencies")
    df_freq = pd.read_csv('frequencies.csv')

    cell_options = df_freq['population'].unique().tolist()
    selected_cells = st.multiselect("Toggle Immune Populations:", options=cell_options, default=cell_options)

    df_filtered = df_freq[df_freq['population'].isin(selected_cells)]

    if not df_filtered.empty:
        fig, ax = plt.subplots(figsize=(10, 4.5))
        sns.boxplot(data=df_filtered, x="population", y="percentage", hue="response", palette="Set2", ax=ax)
        ax.set_ylabel("Relative Frequency (%)")
        ax.set_xlabel("Immune Cell Population")
        st.pyplot(fig)
    else:
        st.warning("Please select at least one cell type variable above to render the plot.")