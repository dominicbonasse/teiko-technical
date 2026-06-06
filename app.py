import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Dominic Bonasse's Teiko Technical")
st.title("Melanoma Miraclib Trial Dashboard by Dominic Bonasse")

# Dependency Verification Check
required_files = [
    'frequencies.csv', 'baseline.csv',
    'summary_table.csv', 'stats.csv'
]

if not all(os.path.exists(f) for f in required_files):
    st.error("Required data assets are missing! Please execute 'make pipeline' first to populate files.")

else:
    # summary table
    st.header("Data Overview")
    st.markdown("Average relative frequencies compared across treatment outcomes is shown in the 'percentage' column. "
                "Sort by a column by clicking its header.")
    df_sum_table = pd.read_csv('summary_table.csv')
    st.dataframe(df_sum_table, use_container_width=True, hide_index=True)
    st.markdown("Number of rows: " + str(df_sum_table.shape[0]))

    # boxplot
    st.header("Cellular Distribution Boxplots")
    st.markdown("Visualization of relative cellular population frequencies, comparing responders vs. non-responders "
                "for each immune cell population. Only using PBMC samples from melanoma patients receiving miraclib.")

    fig, ax = plt.subplots(figsize=(10, 4.5))
    sns.boxplot(data=pd.read_csv('frequencies.csv'), x="population", y="percentage", hue="response", palette="Set2", ax=ax)
    ax.set_ylabel("Relative Frequency (%)")
    ax.set_xlabel("Immune Cell Population")
    st.pyplot(fig)

    # stats
    st.header("Statistical Analysis")
    st.markdown("Independent two-sample t-test evaluations of relative cell population frequencies, comparing "
                "responders vs non-responders.")
    df_sig_report = pd.read_csv('stats.csv')
    st.dataframe(df_sig_report, use_container_width=True, hide_index=True)
    st.markdown("We can see that cd4 t-cell counts are significantly higher in miraclib responders compared to "
                "miraclib non-responders, indicating a correlation between successful miraclib treatment and cd4 "
                "t-cell counts. It also indicates no correlation between miraclib response and other immune cell "
                "counts.")

    # baseline
    st.header("Data Subset Analysts")
    st.markdown("Melanoma PBMC samples at t=0 from patients treated with miraclib")
    df_baseline = pd.read_csv('baseline.csv')
    st.metric("Total Baseline Samples:", len(df_baseline))
    st.dataframe(df_baseline, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("Samples per Project:")
        st.dataframe(df_baseline['project'].value_counts(), use_container_width=True)
    with col2:
        st.caption("Patient Responses:")
        st.dataframe(df_baseline['response'].value_counts(), use_container_width=True)
    with col3:
        st.caption("Patient Sex Profiles:")
        st.dataframe(df_baseline['sex'].value_counts(), use_container_width=True)