# Alexandr (Sasha) Trubetskoy
# February 2019
# trub@uchicago.edu

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-poster')

ma = pd.read_csv('output/compare_ma_pre_ma_post.csv')
ma = ma[ma['iso3']!='MNG']

total_added_v = ma.groupby('iso3')['Added land value'].sum()
top = total_added_v.sort_values(ascending=False)[:15]
# top.index = top.index.to_series().map(COUNTRY_NAMES)
rest = total_added_v.sum() - top.sum()
top.loc['Others'] = rest

fig, ax = plt.subplots(figsize=(10,10))
top.iloc[::-1].plot.barh(color='#63c04b', ax=ax)

rects = ax.patches
labels = [str(int(t/1e6)) + ' Mn' for t in top][::-1]

for rect, label in zip(rects, labels):
    x = rect.get_x() + rect.get_width() + 1e7
    y = rect.get_y() + rect.get_height() / 16
    ax.text(x, y, label, color='white', fontweight='bold', size=16, ha='left', va='bottom')
for rect, label in zip(rects, labels):
    x = rect.get_x() + rect.get_width() + 1e7
    y = rect.get_y() + rect.get_height() / 16
    ax.text(x, y, label, size=16, ha='left', va='bottom')

plt.gca().xaxis.grid(True)
plt.ylabel('')
plt.xticks([n for n in range(0, int(6.1e8), int(1e8))], [n for n in range(0, 610, 100)])
plt.xlabel('Annual urban land rents generated (USD Mn)')

plt.tick_params(top=False, bottom=False, left=False, right=False)
plt.box(on=None)

plt.tight_layout()
plt.savefig('final_tables_and_figures/figure_added_value_by_country.png')