import sqlite3
import csv

conn = sqlite3.connect("cell_count.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# subjects stores unique patient demographic and clinical data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        subject TEXT PRIMARY KEY,
        project TEXT,
        condition TEXT,
        age INTEGER,
        sex TEXT,
        treatment TEXT,
        response TEXT
    );
    """)

# samples stores data for each unique blood sample, linked to subjects
cursor.execute("""
    CREATE TABLE IF NOT EXISTS samples (
        sample TEXT PRIMARY KEY,
        subject TEXT,
        sample_type TEXT,
        time_from_treatment_start INTEGER,
        FOREIGN KEY (subject) REFERENCES subjects(subject)
    );
    """)

# cell_counts stores cell counts, linked to samples
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cell_counts (
        sample TEXT PRIMARY KEY,
        b_cell INTEGER,
        cd8_t_cell INTEGER,
        cd4_t_cell INTEGER,
        nk_cell INTEGER,
        monocyte INTEGER,
        FOREIGN KEY (sample) REFERENCES samples(sample)
    );
    """)

with open('cell-count.csv', mode='r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        age = int(row['age']) if row['age'] else None
        time_start = int(row['time_from_treatment_start']) if row['time_from_treatment_start'] else 0

        # insert subject
        cursor.execute("""
            INSERT OR REPLACE INTO subjects (subject, project, condition, age, sex, treatment, response)
            VALUES (?,?,?,?,?,?,?)
        """,(
            row['subject'], row['project'], row['condition'],
            row['age'], row['sex'], row['treatment'], row['response']
        ))

        # insert sample
        cursor.execute("""
            INSERT OR REPLACE INTO samples (sample, subject, sample_type, time_from_treatment_start)
            VALUES (?,?,?,?)
        """,
            (row['sample'], row['subject'], row['sample_type'], time_start
        ))

        # insert cell counts
        cursor.execute("""
            INSERT OR REPLACE INTO cell_counts (sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte)
            VALUES (?,?,?,?,?,?)
        """, (
            row['sample'],
            int(row['b_cell']) if row['b_cell'] else 0,
            int(row['cd8_t_cell']) if row['cd8_t_cell'] else 0,
            int(row['cd4_t_cell']) if row['cd4_t_cell'] else 0,
            int(row['nk_cell']) if row['nk_cell'] else 0,
            int(row['monocyte']) if row['monocyte'] else 0,
        ))

conn.commit()
conn.close()
print("load_data.py finished")
