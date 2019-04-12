# Alexandr (Sasha) Trubetskoy
# February 2019
# trub@uchicago.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')

costs = pd.read_csv('data/csv/cm_pre.csv', index_col=0).sort_index(axis=0).sort_index(axis=1)
dists = pd.read_csv('data/csv/distance_pre.csv', index_col=0).sort_index(axis=0).sort_index(axis=1)

co = np.ndarray.flatten(np.tril(costs.values)) + 1
di = np.ndarray.flatten(np.tril(dists.values))

df = pd.DataFrame.from_dict({'cost': co, 'dist':di})
df = df[df['cost'] < 2]

fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(x=df['dist'], y=df['cost'], alpha=0.01, s=1)
# df.plot.hexbin(x='dist', y='cost', gridsize=60, ax=ax, bins='log', cmap='gist_yarg')
ax.plot(np.unique(df['dist']), np.poly1d(np.polyfit(df['dist'], df['cost'], 1))(np.unique(df['dist'])),
    color='r',
    linewidth=2)
r_sq_text = 'R-squared: {:.3f}'.format(df.corr().loc['cost']['dist'])
ax.text(10500, 1.23, s=r_sq_text, color='r', weight='demibold')

plt.ylim(1.0, 1.25)
plt.xlim(0, 14000)

plt.xlabel('Distance (km)')
plt.ylabel(r'Pre-BRI trade cost ($\tau_{od}$)')
plt.tight_layout()
plt.savefig('final_tables_and_figures/figure_trade_cost_vs_distance.png')