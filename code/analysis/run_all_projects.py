import logging
import pickle
import os.path
import pandas as pd
from random import shuffle
from get_ma import *
from get_cost_matrix import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_CSV_STEM = 'output/projects/'
# RANKINGS_CSV = 'results/.csv'

UNIQUE = 'ID'
PARAMS = pd.read_csv('parameters/market_access_parameters.csv').set_index('parameter').to_dict()['value']
MARKET_SIZE = 'Rough GDP 2015'

e = 2.718281828459045

def get_all_project_names(G):
    projects = []
    project_names = set([G.edges[e]['project'] for e in G.edges if 'project' in G.edges[e]])
    while project_names:
        p = project_names.pop()
        if p == 'all':
            continue
        if p:
            # print([G.edges[e] for e in G.edges if 'project' not in G.edges[e]])
            proj_edges = [e for e in G.edges if G.edges[e]['project'] == p]
            countries = list(set([G.edges[e]['country'] for e in proj_edges]))
            length = sum([G.edges[e]['length'] for e in proj_edges])
            projects.append((p.replace('/', '_'), proj_edges, countries, length)) # Replace prevents messing things up with filenames
    return projects


def modify_g(base, mod, mask):
    R = base.copy()
    for edge in mask:
        for property_ in R.edges[edge]:
            R.edges[edge][property_] = mod.edges[edge][property_]
    return R


def compare(df1, df2):
    df1 = df1.set_index(UNIQUE)
    df2 = df2.set_index(UNIQUE)

    df1['new ln MA'] = df2['ln MA']
    df1['dif'] = df1['new ln MA'] - df1['ln MA']

    a = PARAMS['alpha']
    th = PARAMS['theta']
    df1['Added land value'] = a*df1[MARKET_SIZE]*(((np.e**df1['dif'])**(1/(1+a*th)))-1)
    return df1.copy()


print('------------------ RUNNING  SETUP ------------------')
road, rail, sea, G_pre = read_geojsons('data/geojson/roads_prebri.geojson', 'data/geojson/rails_prebri.geojson', 'data/geojson/sea_prebri.geojson')
road, rail, sea, G_post = read_geojsons('data/geojson/roads_postbri.geojson', 'data/geojson/rails_postbri.geojson', 'data/geojson/sea_postbri.geojson')
for G in [G_pre, G_post]:
    cities, road_nodes, rail_nodes, sea_nodes, any_nodes = match_cities_with_nodes(road, rail, sea, G)
    G = add_costs_to_graph(G)
    G = create_border_crossings(road_nodes, G)
    G = create_road_rail_transfers(cities, G)
    G = create_sea_transfers(cities, G)
projects = get_all_project_names(G_pre)
pickle.dump(projects, open('data/other/projects.p', 'wb'))
print('------------------ SETUP COMPLETE ------------------')


print('------------- CALCULATING COST MATRICES -------------')
for proj, proj_edges, countries, len_km in projects:
    if os.path.isfile('data/csv/projects/'+proj+'_post_iso.csv'): # Don't waste time rerunning projects
        continue
    proj = proj.replace('/', '_') # Prevents errors with filenames
    print('-'*((50-len(proj))//2), proj, '-'*(50 - len(proj) - (50-len(proj))//2))
    
    G_iso = modify_g(base=G_pre, mod=G_post, mask=proj_edges) # Only the project is completed
    G_comp = modify_g(base=G_post, mod=G_pre, mask=proj_edges) # Everything but the project is completed
    # pre_matrix_iso = get_cost_matrix(cities, G_pre)
    post_matrix_iso = get_cost_matrix(cities, G_iso)
    pre_matrix_com = get_cost_matrix(cities, G_comp)
    # post_matrix_com = get_cost_matrix(cities, G_post)
    
    # pre_matrix_iso.to_csv('data/csv/projects/'+proj+'_pre_iso.csv')
    post_matrix_iso.to_csv('data/csv/projects/'+proj+'_post_iso.csv')
    pre_matrix_com.to_csv('data/csv/projects/'+proj+'_pre_com.csv')
    # post_matrix_com.to_csv('data/csv/projects/'+proj+'_post_com.csv')
    print('-'*52)
print('-------------- COST MATRICES  COMPLETE --------------')


print('------------- CALCULATING  MARKET ACCESS -------------')
shuffle(projects)
cities_pre = pd.read_csv('output/ma_pre.csv')
cities_post = pd.read_csv('output/ma_post.csv')
effect_dict = {}

for proj, proj_edges, countries, len_km in projects:
    if os.path.isfile(OUTPUT_CSV_STEM + proj + ' iso.csv'):
        continue
    print('-'*((50-len(proj))//2), proj, '-'*(50 - len(proj) - (50-len(proj))//2))
    post_matrix_iso = read_cost_matrix('data/csv/projects/'+proj+'_post_iso.csv')
    pre_matrix_com = read_cost_matrix('data/csv/projects/'+proj+'_pre_com.csv')

    cities, externals = read_cities_and_externals()
    logger.info('Calculating market access...')
    cities_iso = cities.progress_apply(add_ma_cols, axis=1, args=(post_matrix_iso, cities, externals))    
    cities_com = cities.progress_apply(add_ma_cols, axis=1, args=(pre_matrix_com, cities, externals))    
    logger.info('Market access calculated.')

    logger.info('Processing results...')
    compare_iso = compare(cities_pre, cities_iso)
    compare_com = compare(cities_com, cities_post)

    # effect_iso = compare_iso.groupby('Country Code')['Added land value'].sum()
    # effect_com = compare_com.groupby('Country Code')['Added land value'].sum()
    # countries = [c for c in countries if c in effect_iso]
    # # effect_dict[proj] = [
    # #     list(countries),
    # #     len_km,
    # #     effect_iso.sum(),
    # #     effect_com.sum(),
    # #     100 * sum([effect_iso[c] for c in countries if c])/effect_iso.sum() if effect_iso.sum() else -1,
    # #     100 * effect_iso['CHN']/effect_iso.sum() if effect_iso.sum() else -1
    # #     ]
    # logger.info('Results processed.')

    OUTPUT_CSV_ISO = OUTPUT_CSV_STEM + proj + ' iso.csv'
    OUTPUT_CSV_COM = OUTPUT_CSV_STEM + proj + ' com.csv'
    logger.info('Exporting to {}...'.format(OUTPUT_CSV_ISO))
    compare_iso.to_csv(OUTPUT_CSV_ISO, index=False)
    compare_com.to_csv(OUTPUT_CSV_COM, index=False)
    print('-'*52)
print('-------------- MARKET ACCESS COMPLETE --------------')