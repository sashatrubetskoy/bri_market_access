import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from os import listdir
from itertools import permutations

cities = pd.read_csv('data/csv/cities.csv')
cm = pd.read_csv('data/csv/cm_pre_no_intl.csv', index_col=0)

idx = cities.groupby(['Country Code'])['Population 2015'].transform(max) == cities['Population 2015']
max_cities = cities.loc[idx].set_index('Country Code')['ID']

# countries = [s.split('.csv')[0] for s in listdir('data/other/raw_comtrade')]
countries = max_cities.index.tolist()
trade_data = {f.split('.csv')[0]: pd.read_csv('data/other/raw_comtrade/{}'.format(f)).set_index('Partner ISO')['Trade Value (US$)'] for f in listdir('data/other/raw_comtrade')}

EU_MARKET = ['IRL', 'NOR', 'SWE', 'FIN', 'DNK', 'GBR', 'IRL', 'EST', 'LVA',
             'LTU', 'POL', 'CZE', 'DEU', 'SVK', 'CHE', 'AUT', 'NLD', 'BEL',
             'BGR', 'ROU', 'GRC', 'ITA', 'ESP', 'PRT', 'HRV', 'HUN']

costs = []
trade_vals = []
for pair in permutations(countries, 2):
    a, b = pair
    if '{}.csv'.format(a) in listdir('data/other/raw_comtrade'):
        if b in trade_data[a].index:
            city_a = max_cities.loc[a]
            city_b = max_cities.loc[b]
            transport_cost = (1 + cm.loc[city_a, city_b])**5.03
            trade_val = trade_data[a].loc[b]

            costs.append(np.log(transport_cost))
            trade_vals.append(np.log(trade_val))

# RUN REGRESSION
X = sm.add_constant(costs)
y = trade_vals
model = sm.OLS(y, X).fit()

fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(costs, trade_vals, scatter_kws={'alpha':0.3})

ax.text(0.20, 25, s='Slope: {:.2f} ({:.2f}), R-squared fit = {:.2f}'.format(model.params[1],
                                                                            model.bse[1], 
                                                                            model.rsquared))

ax.set_xlabel(r'$\ln(\tau^{\theta})$, $\theta=5.03$')
ax.set_ylabel(r'$\ln(trade)$')

plt.tight_layout()
plt.savefig('final_tables_and_figures/figure_cost_vs_trade.png')
plt.close()