# Alexandr (Sasha) Trubetskoy
# November 2018
# trub@uchicago.edu

import os
import sys
import pickle
import pandas as pd

projects = pickle.load(open('data/other/projects.p', 'rb'))

project_files = [x for x in os.listdir('output/projects') if x[:2] != '._']
project_dfs = [pd.read_csv('output/projects/'+filename) for filename in project_files]
project_info = {name:{'Countries':countries, 'Length, km':length} for name, _, countries, length in projects}
# project_names = list(set([x.split('.')[0][:-4] for x in project_files]))

result = {
    'Project name': [],
    'Countries': [],
    'In isolation, Total ΔV, USD Mn': [],
    'In isolation, % of ΔV in proj. country': [],
    'In isolation, % of ΔV in China': [],
    'In isolation, % of ΔV in all other countries': [],
    'In complement, Total ΔV, USD Mn': [],
    'In complement, % of ΔV in proj. country': [],
    'In complement, % of ΔV in China': [],
    'In complement, % of ΔV in all other countries': []
}

for file, df in zip(project_files, project_dfs):
    project_name = file.split('.')[0][:-4]
    iso_or_com = file.split('.')[0][-3:]

    df.loc[df['dif'] < 0, 'Added land value'] = 0

    project_countries_except_china = [c for c in project_info[project_name]['Countries'] if c != 'CHN']
    proj_country_pct = 100 * df[df['Country Code'].isin(project_countries_except_china)]['Added land value'].sum() / df['Added land value'].sum()
    china_pct = 100 * df[df['Country Code'] == 'CHN']['Added land value'].sum() / df['Added land value'].sum()
    if iso_or_com == 'iso':
        result['Project name'].append(project_name)
        result['Countries'].append(project_info[project_name]['Countries'])

        result['In isolation, Total ΔV, USD Mn'].append(df['Added land value'].sum() / 1e6)
        result['In isolation, % of ΔV in proj. country'].append(proj_country_pct)
        result['In isolation, % of ΔV in China'].append(china_pct)
        result['In isolation, % of ΔV in all other countries'].append(100 - proj_country_pct - china_pct)
    if iso_or_com == 'com':
        result['In complement, Total ΔV, USD Mn'].append(df['Added land value'].sum() / 1e6)
        result['In complement, % of ΔV in proj. country'].append(proj_country_pct)
        result['In complement, % of ΔV in China'].append(china_pct)
        result['In complement, % of ΔV in all other countries'].append(100 - proj_country_pct - china_pct)

result_df = pd.DataFrame.from_dict(result, orient='columns')
result_df['Ratio of ΔV iso./ΔV comp.'] = result_df['In isolation, Total ΔV, USD Mn'] / result_df['In complement, Total ΔV, USD Mn']

result_df = result_df[['Project name',
                       'Countries',
                       'In isolation, Total ΔV, USD Mn',
                       'In isolation, % of ΔV in proj. country',
                       'In isolation, % of ΔV in China',
                       'In isolation, % of ΔV in all other countries',
                       'In complement, Total ΔV, USD Mn',
                       'In complement, % of ΔV in proj. country',
                       'In complement, % of ΔV in China',
                       'In complement, % of ΔV in all other countries',
                       'Ratio of ΔV iso./ΔV comp.']]


result_df['In isolation, Total ΔV, USD Mn'] = (result_df['In isolation, Total ΔV, USD Mn']).round(1)
result_df['In complement, Total ΔV, USD Mn'] = (result_df['In complement, Total ΔV, USD Mn']).round(1)
result_df[[c for c in result_df.columns.tolist() if '%' in c]] = result_df[[c for c in result_df.columns.tolist() if '%' in c]].round(0)

result_df.sort_values('In isolation, Total ΔV, USD Mn', ascending=False).to_csv('final_tables_and_figures/table_top_projects.csv', index=False)
