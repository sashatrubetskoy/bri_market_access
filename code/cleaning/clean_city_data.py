# Alexandr (Sasha) Trubetskoy
# February 2019
# trub@uchicago.edu

import string
import json
import math
# import pyproj
import pandas as pd
from unidecode import unidecode
from functools import reduce
from itertools import combinations
from geopy.distance import vincenty
from scipy.spatial import cKDTree

def remove_non_ascii(s):
    rep = repr(s)
    rep = rep.replace('\\', '')
    rep = rep.replace("'", "")
    rep = rep.replace('"', '')
    return rep

# Read files
print('Reading files...')
gdp = pd.read_excel('data/other/raw_city_data/API_NY.GDP.PCAP.KD_DS2_en_excel_v2_9986143.xls', skiprows=3)
reg = pd.read_excel('data/other/raw_city_data/CLASS.xls', skiprows=4)
inc = pd.read_excel('data/other/raw_city_data/OGHIST.xls', sheet_name=1, skiprows=10)
wup = pd.read_excel('data/other/raw_city_data/WUP2018-F12-Cities_Over_300K.xls', skiprows=16)
iso = pd.read_csv('data/other/raw_city_data/iso.csv')

oxf = pd.read_csv('data/other/raw_city_data/oxford_economics_global_cities.csv', thousands=',', encoding = 'utf8')
oxf = oxf[oxf['indicator']=='Gross domestic product']
oxf = oxf[oxf['units']=='US$']
oxf = oxf[oxf['scale']=='Millions: Constant 2012 prices']
oxf['location'] = oxf['location'].apply(remove_non_ascii)
oxf_conv = pd.read_csv('data/other/raw_city_data/oxford_gdp_city_name_convert.csv', encoding = 'utf8')
oxf_conv['Oxford City Name'] = oxf_conv['Oxford City Name'].apply(remove_non_ascii)
oxf_conv = oxf_conv.set_index('My City Name').to_dict()['Oxford City Name']

capitals = pd.read_excel('data/other/raw_city_data/WUP2018-F13-Capital_Cities.xls', skiprows=16)
capitals = capitals[capitals['Capital Type'] == 'Capital']['Capital City'].tolist()

ports = []
with open('data/other/raw_city_data/ports.txt', 'r') as p:
    for line in p.readlines():
        ports.append(line.strip())
print('Files read.')

# Filter data
print('Processing data...')
gdp.loc[1, '2000'] =  gdp.loc[1, '2002'] # Afghanistan has no data for 2000
gdp = gdp[['Country Code', '2000', '2012', '2015']]
gdp.columns = ['Country Code', 'GDP per capita (2010 USD) 2000', 'GDP per capita (2010 USD) 2012', 'GDP per capita (2010 USD) 2015']

reg = reg[['Code', 'Region']]
reg.columns = ['Country Code', 'Region']

wup = wup[['Country Code', 'Country or area', 'Urban Agglomeration', 'Latitude', 'Longitude', 2000, 2005, 2015, 2030]]
wup.columns = ['Country Num', 'Country Name', 'City Name', 'Latitude', 'Longitude', 'Population 2000', 'Population 2005', 'Population 2015', 'Population 2030']

inc.columns = ['Country Code', 'Country Name'] + list(range(1987, 2018))
inc = inc[['Country Code', 2015]]
inc.columns = ['Country Code', 'Income Group']

iso = iso[['Country Code', 'Country Num']].set_index('Country Num').to_dict()['Country Code']

# Merge country data
country_dfs = [gdp, reg, inc]
df_merged = reduce(lambda left,right: pd.merge(left,right,on='Country Code'), country_dfs)

# Add info to cities
wup = wup[wup['Population 2015'] > 300]
wup['Country Code'] = wup['Country Num'].map(iso) # Translate UN country numbers to ISO3
df = pd.merge(wup, df_merged, on='Country Code', how='left')

# Select cities
MY_REGIONS = [
    'Middle East & North Africa',
    'Europe & Central Asia',
    'South Asia',
    'East Asia & Pacific'
    ]
EXCLUDE_COUNTRY_CODES = ['DZA', 'AUS', 'BHR', 'PRK', 'DJI', 'EGY', 'IDN', 
    'IRQ', 'ISR', 'JPN', 'JOR', 'KWT', 'LBN', 'LBY', 'MAR', 'NZL', 'OMN', 
    'PNG', 'PHL', 'QAT', 'KOR', 'SAU', 'PSE', 'SYR', 'ARE', 'YEM', 'TUN']
EXCLUDE_CITIES = ['Las Palmas Gran Canaria', 'Sandakan', 'Kota Kinabalu', 
    'Kuching', 'Cagliari', 'Palma']

df = df[df['Region'].isin(MY_REGIONS)]
df = df[-df['Country Code'].isin(EXCLUDE_COUNTRY_CODES)]
df = df[-df['City Name'].isin(EXCLUDE_CITIES)]

# Fix name of Xinyi, China (there are two)
df.loc[507, 'City Name'] = 'Xinyi, Guangdong'
df.loc[506, 'City Name'] = 'Xinyi, Jiangsu'

# Fix name of Hyderabad (India, Pakistan)
df.loc[795, 'City Name'] = 'Hyderabad, India'
df.loc[1223, 'City Name'] = 'Hyderabad, Pakistan'
print('Data processed.')

# Iteratively combine cities within 30 kilometers of each other
DIST = 30
print('Combining cities within {} km of each other...'.format(DIST))
df = df.sort_values('Population 2015')
counter = 0
l = sum([len(list(combinations(df[df['Country Code'] == country].index.tolist(), 2))) for country in df['Country Code'].unique()])
for i, country in enumerate(df['Country Code'].unique()):
    ccdf = df[df['Country Code'] == country]
    country_cities_l = ccdf.index.tolist()

    already_merged = []
    for a, b in combinations(country_cities_l, 2):
        print('    {:.1f}% complete...'.format(100*counter/l), end='\r')
        counter += 1
        a_loc = (ccdf.loc[a]['Latitude'], ccdf.loc[a]['Longitude'])
        b_loc = (ccdf.loc[b]['Latitude'], ccdf.loc[b]['Longitude'])
        d = vincenty(a_loc, b_loc).km

        # City A is smaller, B is bigger
        if d < DIST and a not in already_merged:
            already_merged.append(a)
            # Combine names
            df.loc[b, 'City Name'] = '-'.join([df.loc[b, 'City Name'], df.loc[a, 'City Name']])
            # Combine populations
            for col in ['Population 2000', 'Population 2005', 'Population 2015', 'Population 2030']:
                df.loc[b, col] += df.loc[a, col]
            # Delete old city
            df = df.drop(a)
print('Cities combined.       ')

# Get true population numbers
for col in ['Population 2000', 'Population 2005', 'Population 2015', 'Population 2030']:
    df.loc[:,col] = 1000*df[col]

# Calculate GDP and drop unneeded columns
print('Adding necessary columns...')
df['Population 2012'] = df['Population 2000'] + (12/15)*((df['Population 2015']-df['Population 2000'])/15)
df['Rough GDP 2000'] = df['GDP per capita (2010 USD) 2000'] * df['Population 2000']
df['Rough GDP 2012'] = df['GDP per capita (2010 USD) 2012'] * df['Population 2012']
df['Rough GDP 2015'] = df['GDP per capita (2010 USD) 2015'] * df['Population 2015']
df = df.drop(['Country Num'], axis=1)

# Add port and capital columns
df['Is Capital'] = df['City Name'].isin(capitals)
df['Is Port'] = df['City Name'].isin(ports)

# Add border distance column. note: this approximation is less accurate when farther from border
with open('data/geojson/borders.geojson', 'r') as f:
    b = json.load(f)
border_pts = []
for i in b['features']:
    border_pts.extend(i['geometry']['coordinates'][0])
tree = cKDTree(border_pts)
def get_border_distance(row):
    # the geojson is in (lon, lat) or x, y format
    lon = row['Longitude']
    lat = row['Latitude']
    nearest_pt = tree.data[tree.query([lon, lat])[1]]
    nearest_pt = (nearest_pt[1], nearest_pt[0])
    return vincenty((lat, lon), nearest_pt).km
df['Distance to Border'] = df.apply(get_border_distance, axis=1)
print('Necessary columns added.')

# # Project coordinates to Eurasia Conformal Conic projection to get X, Y
# deg = pyproj.Proj('+init=EPSG:4326')
# ecc = pyproj.Proj('+proj=lcc +lat_1=5 +lat_2=55 +lat_0=20 +lon_0=80 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs')

def get_xy(row):
    # xy = pyproj.transform(deg, ecc, row['Longitude'], row['Latitude'])
    # row['X'] = xy[0]
    # row['Y'] = xy[1]
    row['X'] = row['Longitude']
    row['Y'] = row['Latitude']
    return row

df = df.apply(get_xy, axis=1)

# Add Oxford city GDP estimates
df['Oxford GDP 2000'] = df['Rough GDP 2000']
df['Oxford GDP 2012'] = df['Rough GDP 2012']
for my_city in oxf_conv:
    oxf_city = oxf_conv[my_city]
    if oxf_city != 'none':
        oxf_2000 = 1e6*sum([oxf.loc[oxf['location']==c, 'v9'].values[0] for c in oxf_city.split('+')])
        oxf_2012 = 1e6*sum([oxf.loc[oxf['location']==c, 'v21'].values[0] for c in oxf_city.split('+')])
        df.loc[df['City Name']==my_city, 'Oxford GDP 2000'] = oxf_2000
        df.loc[df['City Name']==my_city, 'Oxford GDP 2012'] = oxf_2012

# Rearrange columns and export
print('Exporting...')
cols = ['X', 'Y', 'Longitude', 'Latitude', 'City Name', 'Country Name', 'Country Code', 'Region',
        'Income Group', 'GDP per capita (2010 USD) 2000', 'GDP per capita (2010 USD) 2015',
        'Oxford GDP 2000', 'Oxford GDP 2012',
        'Rough GDP 2000', 'Rough GDP 2012', 'Rough GDP 2015', 
        'Population 2000', 'Population 2005', 'Population 2012', 'Population 2015',
        'Population 2030', 'Distance to Border', 'Is Capital', 'Is Port']
df = df[cols]
df['iso3'] = df['Country Code']
df['ID'] = df['Country Code'].str.cat(df.index.values.astype(str))
df.to_csv('data/csv/cities.csv', index=False)
print('Done.')