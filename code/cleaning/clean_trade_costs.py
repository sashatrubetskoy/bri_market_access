import pickle
import pandas as pd
import numpy as np

print('Reading data/other/20180521-ESCAP-WB-tradecosts-dataset.xlsx...')
df = pd.read_excel('data/other/20180521-ESCAP-WB-tradecosts-dataset.xlsx')
print('File read.')


print('Filtering data...')
gtt = df[df['sector']=='GTT']
print('Data filtered.')


print('Filling missing data for...')
def copy_country_data(gtt, source, target):
    df_src = gtt[(gtt['reporter']==source) | (gtt['partner']==source)]
    df_copy = df_src.replace({source: target}, regex=True)
    gtt_fixed = pd.concat([gtt, df_copy], axis=0)
    return gtt_fixed

# Create data for SERBIA by copying CROATIA
print('\tSerbia...')
gtt2 = copy_country_data(gtt, source='BIH', target='SRB')
print('\tCopied BIH to Serbia.')

# Create data for AFGHANISTAN by copying PAKISTAN
print('\tAfghanistan...')
gtt3 = copy_country_data(gtt2, source='PAK', target='AFG')
print('\tCopied Pakistan to Afghanistan.')

# Repair data for ROMANIA
print('\tRomania...')
gtt4 = copy_country_data(gtt3, source='ROM', target='ROU')
print('\tCopied code [ROM] to code [ROU].')

# Create data for MACEDONIA by copying ALBANIA
print('\tMacedonia...')
gtt_last = copy_country_data(gtt4, source='ALB', target='MAC')
print('\tCopied Albania to Macedonia.')

# Create data for TURKMENISTAN by copying UZBEKISTAN
print('\tTurkmenistan...')
gtt_last = copy_country_data(gtt4, source='TKM', target='UZB')
print('\tCopied Uzbekistan to Turkmenistan.')

print('Missing data filled.')


print('Constructing tariff matrix...')
gtt_multiindex = gtt_last.set_index(['reporter', 'partner', 'year']).sort_index()
tariff_matrix = np.zeros((gtt_last['reporter'].unique().shape[0], gtt_last['reporter'].unique().shape[0]))
latest_years = gtt_last.groupby(['reporter', 'partner'])['year'].max()

idx = {iso : sorted(gtt_last['reporter'].unique().tolist()).index(iso) for iso in gtt_last['reporter'].unique()}
pickle.dump(idx, open('data/other/index_converter.p', 'wb'))

for iso_a in gtt_last['reporter'].unique():
    if iso_a in gtt_multiindex.index:
        for iso_b in gtt_last['reporter'].unique():
            if iso_b not in gtt_multiindex.loc[iso_a].index:
                tariff_matrix[idx[iso_a]][idx[iso_b]] = 99 # Represents unfeasible trade
            else:
                val = gtt_multiindex.loc[iso_a, iso_b, latest_years[iso_a][iso_b]]['tij'].values[0]
                tariff_matrix[idx[iso_a], idx[iso_b]] = val/100
print('Tariff matrix constructed.')

print('Writing new file...')
np.savetxt('parameters/tariff_matrix.csv', tariff_matrix, delimiter=',')
print('New file written.')
print('Done.')