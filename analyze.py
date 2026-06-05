import sqlite3
import pandas as pd

conn = sqlite3.connect("cell_count.db")

query = """
    WITH totaled_cells AS (
        SELECT
            sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte,
            (b_cell + cd8_t_cell + cd4_t_cell +nk_cell + monocyte) AS total_count
        FROM cell_counts
    )

    SELECT sample AS sample, total_count, 'b_cell' AS population, b_cell AS count,
        (b_cell * 100.0 / total_count) AS percentage FROM totaled_cells
    UNION ALL
    SELECT sample AS sample, total_count, 'cd8_t_cell' AS population, cd8_t_cell AS count,
        (cd8_t_cell * 100.0 / total_count) AS percentage FROM totaled_cells
    UNION ALL
    SELECT sample AS sample, total_count, 'cd4_t_cell' AS population, cd4_t_cell AS count,
        (cd4_t_cell * 100.0 / total_count) AS percentage FROM totaled_cells
    UNION ALL
    SELECT sample AS sample, total_count, 'nk_cell' AS population, nk_cell AS count,
        (nk_cell * 100.0 / total_count) AS percentage FROM totaled_cells
    UNION ALL
    SELECT sample AS sample, total_count, 'monocyte' AS population, monocyte AS count,
        (monocyte * 100.0 / total_count) AS percentage FROM totaled_cells
    ORDER BY sample, population;
"""

df = pd.read_sql_query(query, conn)
conn.close()
print(df.head())
