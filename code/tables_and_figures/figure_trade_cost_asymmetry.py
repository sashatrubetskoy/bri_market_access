# Alexandr (Sasha) Trubetskoy
# February 2019
# trub@uchicago.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

costs = pd.read_csv('data/csv/cm_pre.csv', index_col=0).sort_index(axis=1).sort_index(axis=0)

# Take the lower triangle of the costs matrix, the flip it up, so that costs for i, j
# line up with costs for j, i
tau_od = np.ndarray.flatten(np.tril(costs.values).T)# + 1
tau_do = np.ndarray.flatten(np.triu(costs.values))# + 1

df = pd.DataFrame.from_dict({'tau_od': tau_od, 'tau_do':tau_do})
df = df[(df['tau_od'] < 10) & (df['tau_do'] < 10)]
df = df[df['tau_od']>0]
df['tau_max'] = df[['tau_od', 'tau_do']].max(axis=1)
df['tau_min'] = df[['tau_od', 'tau_do']].min(axis=1)

fig, ax = plt.subplots(figsize=(6,6))

ax.scatter(
    x=df['tau_min']+1, 
    y=df['tau_max']+1, 
    alpha=0.005, 
    s=2)

ax.plot(np.unique(df['tau_min']+1), np.poly1d(np.polyfit(df['tau_min']+1, df['tau_max']+1, 1))(np.unique(df['tau_min']+1)),
    color='r',
    linewidth=2)
r_sq_text = 'R-squared: {:.3f}'.format(df.corr().loc['tau_min']['tau_max'])
ax.text(1.17, 1.02, s=r_sq_text, color='r', size='large', weight='demibold')

plt.xlim(1.0, 1.25)
plt.ylim(1.0, 1.25)
 
# plt.title(r'Cost symmetry if border costs and tariffs are removed – $\tau_{od}$ vs $\tau_{do}$')
plt.xlabel(r'min$(\tau_{od},\tau_{do})$')
plt.ylabel(r'max$(\tau_{od},\tau_{do}) $')
plt.tight_layout()
plt.savefig('final_tables_and_figures/figure_trade_cost_asymmetry.png')