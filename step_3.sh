#!/bin/bash

# Alexandr (Sasha) Trubetskoy
# April 2019
# trub@uchicago.edu

echo "Running all projects..." # 50 hours
python code/analysis/run_all_projects.py
echo "Done running all projects."

echo "Creating top project for cities table..."
python code/tables_and_figures/table_top_project_for_cities.py
echo "Top project for cities table created."

echo "Creating top projects table..."
python code/tables_and_figures/table_top_projects.py
echo "Top projects table created."