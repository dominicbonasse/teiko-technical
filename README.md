# teiko-technical README
Install the entire folder from GitHub.

Navigate to this directory in your shell and ensure the 'make' utility is installed.

Run the 'make setup' command to create a virtual environment, install pip, and install all requirements.

Next, run the 'make pipeline' command to initialize the cell_counts database and generate output tables.

Finally, run 'make dashboard' to start the local server for the interactive dashboard.

Once the dashboard is created, it can be accessed in your web browser at http://localhost:8501/

# Schema explanation

The database maps the clinical dataset into a schema across three specialized tables: subjects, samples, and cell_counts.

This design guarantees data integrity through relational foreign keys.

As the workflow scales to hundreds of projects and thousands of longitudinal samples, this structure maintains compact table footprints and quick index-driven queries. 

New analytics can be integrated  without changing the existing architecture by  attaching modular assay tables directly to the central sample IDs.

The project uses load_data.py for the pipeline ingestion, analyze.py for statistical analysis, and app.py for dashboard presentation. 

By separating the layers and caching intermediate statistical data to .csv files, the interactive dashboard reloads quickly without rerunning everything.