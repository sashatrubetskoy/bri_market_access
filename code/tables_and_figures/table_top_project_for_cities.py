# Alexandr (Sasha) Trubetskoy
# February 2019
# trub@uchicago.edu

import os.path
import numpy as np
import pandas as pd
from os import listdir
from tqdm import tqdm, tqdm_pandas
tqdm.pandas() # Gives us nice progress bars

# DEFINE FUNCTIONS
# --------------------------------------------------
def best_iso_project(row):
    max_dV = 0
    best_proj_name = None
    for f, df in zip(project_iso_files, project_iso_dfs):
        dV = df.set_index('City Name').loc[row['City Name']]['Added land value']
        cur_project_name = f.split(' iso.csv')[0]
        if dV > max_dV:
            max_dV = dV
            best_proj_name = cur_project_name
    row['Project name'] = best_proj_name
    row['Added land value'] = max_dV
    return row


project_iso_files = [x for x in listdir('output/projects') if ' iso.csv' in x and x[:2] != '._']
project_iso_dfs = [pd.read_csv('output/projects/'+filename) for filename in project_iso_files]

baseline = pd.read_csv('output/compare_ma_pre_ma_post.csv')
selection = baseline[baseline['Added land value'] > 0]
# selection = baseline[baseline['Added land value'] > 1e6]

selection = selection.progress_apply(best_iso_project, axis=1)
selection['Added land value, USD Mn'] = selection['Added land value'] / 1e6
selection['Added land value per capita, USD'] = selection['Added land value'] / selection['Population 2015']

# baseline = baseline.drop('GDP 2015', axis=1)
selection = selection.sort_values('Added land value per capita, USD', ascending=False)
my_cols = selection[['City Name', 'Country Code', 'Project name', 'Added land value per capita, USD', 'Added land value, USD Mn', 'Population 2015']]
my_cols.loc[:,'Population 2015'] = my_cols['Population 2015'].apply(int)
my_cols.loc[:,'Added land value, USD Mn'] = my_cols['Added land value, USD Mn'].round(1)
my_cols.loc[:,'City Name'] = my_cols['City Name'].str.replace(',', '')

# my_cols = my_cols[my_cols['Added land value per capita, USD'] > 2.5]
my_cols.loc[:,'Rank'] = my_cols['Added land value per capita, USD'].rank(ascending=False).apply(int)
my_cols = my_cols.set_index('Rank')
my_cols.loc[:,'Added land value per capita, USD'] = my_cols['Added land value per capita, USD'].round(2)
my_cols.to_csv('final_tables_and_figures/table_top_project_for_cities.csv')