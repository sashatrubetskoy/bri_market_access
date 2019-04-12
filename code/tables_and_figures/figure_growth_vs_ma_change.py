# Alexandr (Sasha) Trubetskoy
# November 2018
# trub@uchicago.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
import seaborn as sns
plt.style.use('seaborn-whitegrid')

# READ DATA
#----------------------------------------------------------
df_00 = pd.read_csv('output/ma_pre_2000.csv').set_index('ID')
sel_00 = df_00[['Country Code', 'Longitude', 'Latitude', 'ln MA', 'Population 2000', 'Population 2015', 
    'GDP per capita (2010 USD) 2000', 'GDP per capita (2010 USD) 2015']]
sel_00.columns = ['Country Code', 'Longitude', 'Latitude', 'ln MA initial 2000', 'Population 2000', 'Population 2015', 'GDP per capita (2010 USD) 2000', 'GDP per capita (2010 USD) 2015']

df_15 = pd.read_csv('output/ma_pre.csv').set_index('ID')
sel_15 = df_15[['ln MA']]
sel_15.columns = ['ln MA initial 2015']

# CALCULATE RAW COLUMNS
#----------------------------------------------------------
m = sel_00.join(sel_15, how='outer')
m['Delta_log_Pop'] = np.log(m['Population 2015']) - np.log(m['Population 2000'])
m['Delta_log_GDP'] = np.log(m['Population 2015']*m['GDP per capita (2010 USD) 2015']) - np.log(m['Population 2000']*m['GDP per capita (2010 USD) 2000'])
m['Delta_log_MA'] = m['ln MA initial 2015'] - m['ln MA initial 2000']


# REGRESS ON COUNTRY FIXED EFFECTS AND LON, LAT
#----------------------------------------------------------
model_pop = sm.mixedlm(formula='Delta_log_Pop ~ Longitude + Latitude', groups='Country Code', data=m).fit()
model_MA = sm.mixedlm(formula='Delta_log_MA ~ Longitude + Latitude', groups='Country Code', data=m).fit()

m['Pop_Resid'] = model_pop.resid
m['MA_Resid'] = model_MA.resid

p95 = m['MA_Resid'].quantile(0.99)
p05 = m['MA_Resid'].quantile(0.01)
m = m.replace([np.inf, -np.inf], np.nan)
m = m[~m['Pop_Resid'].isnull()]
m = m[(m['MA_Resid']>p05) & (m['MA_Resid']<p95)]

fig, ax = plt.subplots(figsize=(8, 5))

g = sns.regplot(
    x='MA_Resid',
    y='Pop_Resid',
    data=m,
    # lowess=True,
    scatter_kws={'alpha': 0.2},
    line_kws={'color':'red'})
# g.set(xlim=(-0.75, 0.75))
g.set(ylim=(-0.4,0.4))

result = sm.ols(formula="Pop_Resid ~ 0 + MA_Resid", data=m).fit()

# r_sq_text = 'R-squared: {:.3f}'.format(m.corr().loc['Pop_Resid']['MA_Resid'])
coef_text = 'coef.: {:.3f}'.format(result.params['MA_Resid'])
serr_text = 'std err.: {:.3f}'.format(result.bse['MA_Resid'])
# ax.text(0.003, 0.64, s=r_sq_text, color='r', weight='demibold')
ax.text(-0.0061, 0.32, s=coef_text, color='r', weight='demibold')
ax.text(-0.0061, 0.28, s=serr_text, color='r', weight='demibold')

plt.tight_layout()
plt.xlabel('Residual difference in log market access (2000–2015)')
plt.ylabel('Residual difference in log population (2000–2015)')
plt.savefig('final_tables_and_figures/figure_growth_vs_ma_change.png')