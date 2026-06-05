import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

conn = sqlite3.connect("cell_count.db")

# Part 2: Frequency of each cell type in each sample

query = """
    WITH totaled_cells AS (
        SELECT
            sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte,
            (b_cell + cd8_t_cell + cd4_t_cell +nk_cell + monocyte) AS total_count
        FROM cell_counts
    ),

    summary_table AS (
        SELECT sample AS sample, total_count, 'b_cell' AS population, b_cell AS count, (b_cell * 100.0 / total_count) AS percentage \
        FROM totaled_cells \
        UNION ALL \
        SELECT sample       AS sample, \
               total_count, \
               'cd8_t_cell' AS population, \
               cd8_t_cell AS count,
                (cd8_t_cell * 100.0 / total_count) AS percentage \
        FROM totaled_cells \
        UNION ALL \
        SELECT sample       AS sample, \
               total_count, \
               'cd4_t_cell' AS population, \
               cd4_t_cell AS count,
                (cd4_t_cell * 100.0 / total_count) AS percentage \
        FROM totaled_cells \
        UNION ALL \
        SELECT sample    AS sample, \
               total_count, \
               'nk_cell' AS population, \
               nk_cell AS count,
                (nk_cell * 100.0 / total_count) AS percentage \
        FROM totaled_cells \
        UNION ALL \
        SELECT sample     AS sample, \
               total_count, \
               'monocyte' AS population, \
               monocyte AS count,
                (monocyte * 100.0 / total_count) AS percentage \
        FROM totaled_cells
    )
        
    SELECT st.sample, st.total_count, st.population, st.count, st.percentage, sub.condition, sub.treatment, sub.response, sam.sample_type
    FROM summary_table AS st
    JOIN samples sam ON st.sample = sam.sample
    JOIN subjects sub ON sam.subject = sub.subject
"""

df = pd.read_sql_query(query, conn)
conn.close()

print(df.head())
print("Columns: " + ", ".join(df.columns))
print("Number of rows: " + str(df.shape[0]))

# Part 3: Difference in relative cell pop. freqs between melanoma patient responders to miraclib and non-responders,
# only using PBMC samples. Visualized using boxplot, reporting sig. diffs in relative freqs.

filtered_df = df[
    (df["condition"] == "melanoma")
    & (df["treatment"] == "miraclib")
    & (df["sample_type"] == "PBMC")
    & (df["response"].isin(["yes","no"]))
]

plt.figure(figsize=(10,6))
sns.boxplot(data=filtered_df, x="population", y="percentage", hue="response")
plt.title("Boxplot of relative immune cell population frequencies comparing responders to non-responders")
plt.xlabel("Population")
plt.ylabel("Relative immune cell population percentage")
plt.show()

for pop in filtered_df["population"].unique():
    pop_df = filtered_df[filtered_df["population"] == pop]
    responders = pop_df[pop_df["response"] == "yes"]["percentage"]
    non_responders = pop_df[pop_df["response"] == "no"]["percentage"]

    # Two ind. groups, not assuming equal variances
    t_stat, p_val = stats.ttest_ind(responders, non_responders, equal_var=False)

    print(f"\nPopulation: {pop}")
    print(f"Mean for responders: {responders.mean():.2f} %")
    print(f"Mean for non-responders: {non_responders.mean():.2f} %")
    print(f"t-statistic: {t_stat:.5f}")
    print(f"p-value: {p_val:.5f}")
    print(f"Significant (alpha=0.05): {str(p_val < 0.05)}")

# Part 4: Identify melanoma PBMC samples at baseline (time_from_treatment_start = 0).
# Extend query to determine how many samples from each project, how many subjects are responders/non-responders,
# how many subjects are male/female.