import json
import pandas as pd
import numpy as np
from unidecode import unidecode

TAU_PER_DAY = 0.021

print('Reading data (may take a moment)...')
df = pd.read_stata('data/raw_hummels_schaur_data/City_pair_Regional_dataset_Lower_Bound.dta')
base_pre = pd.read_csv('data/cost_matrices/overall/matrix_pre.csv', index_col=0)
base_post = pd.read_csv('data/cost_matrices/overall/matrix_post.csv', index_col=0)
cities = pd.read_csv('data/csv/cities.csv')
with open('data/raw_hummels_schaur_data/city_name_conversions.txt', 'r') as f:
    city_convert = eval(f.read())
with open('data/raw_hummels_schaur_data/iso2_to_iso3.json', 'r') as f:
    iso2_to_iso3 = json.loads(f.read())
iso3_to_iso2 = {iso2_to_iso3[iso2]['iso3']: iso2 for iso2 in iso2_to_iso3}


print('Filtering city pairs...')
my_iso3 = cities['Country Code'].unique().tolist()
my_iso2 = [iso3_to_iso2[iso3] for iso3 in my_iso3]
df = df[(df['d_iso'].isin(my_iso2)) & (df['o_iso'].isin(my_iso2))]
df = df.set_index(['o_city', 'd_city'])

all_hs_cities = list(city_convert.keys())
ignore = []
for city in all_hs_cities:
    if df.loc[city_convert[city]].shape[0] < 1437:
        ignore.append(city)
ok_cities = [c for c in all_hs_cities if c not in ignore]

print('\tExporting cities_hummels_schaur.csv...')
cities[cities['City Name'].isin(ok_cities)].to_csv('data/csv/cities_hummels_schaur.csv', index=False)


print('Creating cost matrices...')

print('\tCreating Hummels & Schaur PRE matrix...')
hs_pre = np.ones([573,573])
for i, city_a in enumerate(ok_cities):
    print('\t\t{} of {}'.format(i+1, len(ok_cities)), end='\r')
    for j, city_b in enumerate(ok_cities):
        if i == j:
            hs_pre[i, j] = -1
        else:
            c_a = city_convert[city_a]
            c_b = city_convert[city_b]
            try:
                hs_pre[i, j] = TAU_PER_DAY * (df.loc[(c_a, c_b)]['hr_pre_BRI'] / 24)
            except KeyError: 
                print(city_a, c_a, city_b, c_b)

print('\tCreating Hummels & Schaur POST matrix...')
hs_post = np.ones([573,573])
for i, city_a in enumerate(ok_cities):
    print('\t\t{} of {}'.format(i+1, len(ok_cities)), end='\r')
    for j, city_b in enumerate(ok_cities):
        if i == j:
            hs_pre[i, j] = -1
        else:
            c_a = city_convert[city_a]
            c_b = city_convert[city_b]
            try:
                hs_post[i, j] = TAU_PER_DAY * (df.loc[(c_a, c_b)]['hr_post_BRI'] / 24)
            except KeyError: 
                print(city_a, c_a, city_b, c_b)

print('\tCreating matched baseline PRE matrix...')
matched_baseline_pre = base_pre.loc[ok_cities][ok_cities]

print('\tCreating matched baseline PRE matrix...')
matched_baseline_post = base_post.loc[ok_cities][ok_cities]


print('Exporting cost matrices...')
hs_pre_df = pd.DataFrame(hs_pre, index=ok_cities, columns=ok_cities)
hs_post_df = pd.DataFrame(hs_post, index=ok_cities, columns=ok_cities)
hs_pre_df.to_csv('data/cost_matrices/hummels_schaur/matrix_pre_hs.csv')
hs_post_df.to_csv('data/cost_matrices/hummels_schaur/matrix_post_hs.csv')
matched_baseline_pre.to_csv('data/cost_matrices/hummels_schaur/matrix_pre_hs_baseline.csv')
matched_baseline_post.to_csv('data/cost_matrices/hummels_schaur/matrix_post_hs_baseline.csv')

print('Done.')