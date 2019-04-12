# Alexandr (Sasha) Trubetskoy
# April 2019
# trub@uchicago.edu

import numpy as np
import pandas as pd

EUR_TO_USD_2014 = 1.25
EUR_TO_USD_2015 = 1.10
PLN_TO_USD_2015 = 0.30
RMB_TO_USD_2017 = 0.154
FEU_TO_TEU = 0.6


# Emerson, Michael and Evgeny Vinokurov (2009). "Optimisation of Central Asian 
#   and Eurasian Trans-Continental Land Transport Corridor." Emerson and Vinokurov
#   do not include distances, which were estimated by the authors Reed and 
#   Trubetskoy.
EMERSON_DATA = {
    'Origin':       ['Shanghai',    'Shanghai', 'Shanghai', 'Shanghai', 'Shanghai', 'Shanghai',     'Shanghai',         'Shanghai',     'Shanghai'],
    'Destination':  ['Hamburg',     'Kotka',    'Tallinn',  'Riga',     'Klaipeda', 'Novorossiysk', 'St. Petersburg',   'Vladivostok',  'Moscow'],
    'TEU cost, USD':[1475,          1620,       1925,       1925,       1925,       2025,           1980,               1350,           3585],
    'Mode':         ['Sea',         'Sea',      'Sea',      'Sea',      'Sea',      'Sea',          'Sea',              'Sea',          'Rail'],
    'Est dist, km': [20146,         21449,      21672,      21564,      15830,      15830,          19823,              1844,           7621]
}
emerson = pd.DataFrame.from_dict(EMERSON_DATA)
emerson['Cost per km, USD'] = emerson['TEU cost, USD'] / emerson['Est dist, km']
emerson_bounds = pd.concat([emerson.groupby('Mode').min()['Cost per km, USD'], emerson.groupby('Mode').max()['Cost per km, USD']], axis=1)
emerson_bounds.columns = ['lower', 'upper']
emerson_bounds.index = ['Rail cost, USD/TEU/km', 'Sea cost, USD/TEU/km']

# Rodemann, Hendrik and Simon Templar (2014). "The enablers and inhibitors of 
#   intermodal rail freight between Asia and Europe." Rodemann and Templar also 
#   include sea costs for each connection, but the sea path taken is not clear, 
#   so these costs are not considered.
RODEMANN_DATA = {
    'Route':                ['Northern east-west connection',   'Central east-west connection', 'North-south connection'],
    'Rail cost, EUR/FEU':   [5000,                              6500,                           4600],
    'Road cost, EUR/FEU':   [10000,                             10000,                          6000],
    'Distance 1, km':       [9290,                              10900,                          6000],
    'Distance 2, km':       [10000,                             11870,                          6500],
    'Distance 3, km':       [None,                              None,                           7600],
}
rodemann = pd.DataFrame.from_dict(RODEMANN_DATA)
rodemann['Median distance, km'] = rodemann[['Distance 1, km', 'Distance 2, km', 'Distance 3, km']].median(axis=1)
rodemann['Rail cost, USD/FEU/km'] = EUR_TO_USD_2014 * rodemann['Rail cost, EUR/FEU'] / rodemann['Median distance, km']
rodemann['Road cost, USD/FEU/km'] = EUR_TO_USD_2014 * rodemann['Road cost, EUR/FEU'] / rodemann['Median distance, km']
rodemann['Rail cost, USD/TEU/km'] = rodemann['Rail cost, USD/FEU/km'] * FEU_TO_TEU
rodemann['Road cost, USD/TEU/km'] = rodemann['Road cost, USD/FEU/km'] * FEU_TO_TEU
rodemann_bounds = pd.concat([rodemann.min()[['Road cost, USD/TEU/km', 'Rail cost, USD/TEU/km']], rodemann.max()[['Road cost, USD/TEU/km', 'Rail cost, USD/TEU/km']]], axis=1)
rodemann_bounds.columns = ['lower', 'upper']


# Seo, Young Joon et al. (2017). "Multimodal Transportation: The Case of Laptop from 
#   Chongqing in China to Rotterdam in Europe." Seo et al. cite a shipping cost
#   from Chongqing to Shanghai via inland waterway. These are not considered.
SEO_DATA = {
    'Origin':       ['Shanghai',     'Chongqing',    'Chongqing',    'Chongqing',    'Yantian Port', 'Chongqing',    'Chongqing',    'Duisburg',     'Duisburg'],
    'Destination':  ['Rotterdam',    'Shanghai',     'Shanghai',     'Shenzhen',     'Rotterdam',    'Shenzhen',     'Duisburg',     'Rotterdam',    'Rotterdam'],
    'Mode':         ['Sea',          'Road',         'Rail',         'Road',         'Sea',          'Rail',         'Rail',         'Road',         'Rail'],
    'Distance, km': [19378.67,       1728,           1919,           1587,           18064.6,        2002,           11179,          200,            362],
    'Cost, USD/FEU':[1100,           1486,           1106,           1392,           1100,           1121.1,         4300,           180,            271.2]
}
seo = pd.DataFrame.from_dict(SEO_DATA)
seo['Cost, USD/FEU/km'] = seo['Cost, USD/FEU'] / seo['Distance, km']
seo['Cost, USD/TEU/km'] = FEU_TO_TEU * seo['Cost, USD/FEU/km']
seo_bounds = pd.concat([seo.groupby('Mode').min()['Cost, USD/TEU/km'], seo.groupby('Mode').max()['Cost, USD/TEU/km']], axis=1)
seo_bounds.columns = ['lower', 'upper']
seo_bounds.index = ['Rail cost, USD/TEU/km', 'Road cost, USD/TEU/km', 'Sea cost, USD/TEU/km']

# Sladkowski, Aleksander and Maria Ciesla (2015). "Influence of a Potential 
#   Railway Line Connecting the Caspian Sea with the Black Sea on the Development
#   of Eurasian Trade". Some costs are converted from other currencies. Costs for 
#   containers less than 20 tons are not included. In cases where a range of 
#   values was cited for a single journey (e.g. "3,465 – 3,635 USD"), the mean
#   was taken.
C = EUR_TO_USD_2015
D = PLN_TO_USD_2015
SLADKOWSKI_DATA = {
    'Origin':       ['Shanghai',    'Shanghai', 'Hamburg',  'Shanghai', 'Gdynia',   'Shanghai',     'Vladivostok',  'Vladivostok',  'Ningbo',   'Gdynia',   'Qingdao',  'Gdynia'],
    'Destination':  ['Warsaw',      'Hamburg',  'Warsaw',   'Gdynia',   'Warsaw',   'Vladivostok',  'Moscow',       'Rostov',       'Gdynia',   'Lublin',   'Gdynia',   'Lodz'],
    'Mode':         ['Rail',        'Sea',      'Road',     'Sea',      'Road',     'Sea',          'Rail',         'Rail',         'Sea',      'Road',     'Sea',      'Road'],
    'Distance, km': [7967,          20216,      852,        20822,      383,        1845,           9300,           10538,          20592,      557,        21303,      350],
    'Cost, USD/FEU':[7500,          1250,       1100,       1600,       C*350,      2140,           3550,           4455,           1800,       C*1500,     1800,       None],
    'Cost, USD/TEU':[None,          None,       None,       None,       None,       None,           None,           None,           None,       None,       None,       D*1750]
}
sladkowski = pd.DataFrame.from_dict(SLADKOWSKI_DATA)
sladkowski['Cost, USD/FEU/km'] = sladkowski['Cost, USD/FEU'] / sladkowski['Distance, km']
sladkowski['Cost, USD/TEU/km'] = FEU_TO_TEU * sladkowski['Cost, USD/FEU/km']
usd_row = -sladkowski['Cost, USD/TEU'].isnull()
sladkowski.loc[usd_row, 'Cost, USD/TEU/km'] = sladkowski.loc[usd_row, 'Cost, USD/TEU'] / sladkowski.loc[usd_row, 'Distance, km']

sladkowski_bounds = pd.concat([sladkowski.groupby('Mode').min()['Cost, USD/TEU/km'], sladkowski.groupby('Mode').max()['Cost, USD/TEU/km']], axis=1)
sladkowski_bounds.columns = ['lower', 'upper']
sladkowski_bounds.index = ['Rail cost, USD/TEU/km', 'Road cost, USD/TEU/km', 'Sea cost, USD/TEU/km']


# Sun, Feng et al. (2017) "Improvement of Rail-sea Multimodal Transport with Dry
#   Port Construction: Case Study of Ningbo-Zhoushan Port". Some per-kilometer 
#   costs derived implicitly using a system of equations:
#   C_rail*D_NZ-Cq  + C_road*D_Cq-Ch = 2488*C_rail + 325*C_road = 5786.04    (1)
#   C_water*D_NZ-Cq + C_road*D_Cq-Ch = 2547*C_water + 325*C_road = 5111      (2)
#   C_water*D_NZ-Cq + C_rail*D_Cq-Ch = 2547*C_water + 315*C_rail = 3834.45   (3)
#            ==>  C_water = 1.307,  C_rail = 1.609,  C_road = 5.487 (RMB/TEU/km)
SUN_DATA = {
    'Origin':           [None,      'Ningbo-Zhoushan',  'Ningbo-Zhoushan',  'Ningbo-Zhoushan',  'Chongqing',    'Chongqing',    'Ningbo-Zhoushan',  'Ningbo-Zhoushan'],
    'Destination':      [None,      'Chongqing',        'Chongqing',        'Chongqing',        'Chengdu',      'Chengdu',      'Chengdu',          'Chengdu'],
    'Mode':             ['Rail',    'Road',             'Rail',             'Inland Waterway',  'Road',         'Rail',         'Road',             'Rail'],
    'Distance, km':     [None,      1830.4,             2488,               2547,               325,            315,            2107,               2803],
    'Cost, RMB/TEU':    [None,      10043,              4003,               1783,               1783,           507,            12642,              4294.49],
    'Cost, RMB/TEU/km': [0.9274,    None,               None,               None,               None,           None,           None,               None,]
}
sun = pd.DataFrame.from_dict(SUN_DATA)
empty_row = sun['Cost, RMB/TEU/km'].isnull()
sun.loc[empty_row, 'Cost, RMB/TEU/km'] = sun['Cost, RMB/TEU'] / sun['Distance, km']
sun['Cost, USD/TEU/km'] = RMB_TO_USD_2017 * sun['Cost, RMB/TEU/km']

sun_bounds = pd.concat([sun.groupby('Mode').min()['Cost, USD/TEU/km'], sun.groupby('Mode').max()['Cost, USD/TEU/km']], axis=1)
sun_bounds = sun_bounds.drop('Inland Waterway')
sun_bounds.columns = ['lower', 'upper']
sun_bounds.index = ['Rail cost, USD/TEU/km', 'Road cost, USD/TEU/km']

bounds = [emerson_bounds, rodemann_bounds, seo_bounds, sladkowski_bounds, sun_bounds]
bounds = [b.reindex(['Road cost, USD/TEU/km', 'Rail cost, USD/TEU/km', 'Sea cost, USD/TEU/km']) for b in bounds]
rail_final = pd.concat(bounds, axis=0).loc['Rail cost, USD/TEU/km'].median()
road_final = pd.concat(bounds, axis=0).loc['Road cost, USD/TEU/km'].median()
sea_cost = np.median(pd.concat(bounds, axis=0).loc['Sea cost, USD/TEU/km'].values)
names = ['Emerson (2009)', 'Rodemann (2014)', 'Seo (2017)', 'Sladkowski (2015)', 'Sun (2017)']

with open('final_tables_and_figures/table_transport_cost_sources.csv', 'w') as f:
    f.write('Estimated cost (USD/TEU/km)\n')
    f.write(',Road,Road,Rail,Rail,Sea,Sea\n')
    f.write('Ref.,Lower,Upper,Lower,Upper,Lower,Upper\n')
    for i, bound in enumerate(bounds):
        values = [names[i]] + list(np.round(bound.values.flatten().astype(np.double), 2))
        f.write('{},{},{},{},{},{},{}\n'.format(*values))
    final_values = [np.round(v, 2) for v in [road_final[0], road_final[1], rail_final[0], rail_final[1], sea_cost]]
    f.write('Median,{},{},{},{},,{}\n'.format(*final_values))


