# Alexandr (Sasha) Trubetskoy
# February 2019
# trub@uchicago.edu

import pandas as pd

df = pd.read_csv('output/ma_pre.csv')
df['Initial MA decile'] = pd.qcut(df['ln MA'], 10)
deciles = df.groupby('Initial MA decile')

median_ln_MA = deciles['ln MA'].median().round(2)
idx = df.groupby(['Income Group', 'Initial MA decile'])['Population 2015'].transform(max) == df['Population 2015']
largest_income_city = df[idx].pivot(index='Initial MA decile', columns='Income Group', values='City Name').drop('L', axis=1)
total_pop = deciles['Population 2015'].sum().apply(int)
median_pop = deciles['Population 2015'].median().apply(int)
cagr_05_15 = (100*((deciles['Population 2015'].sum()/deciles['Population 2005'].sum())**(1/10)-1)).round(2)
cagr_15_30 = (100*((deciles['Population 2030'].sum()/deciles['Population 2015'].sum())**(1/15)-1)).round(2)
total_gdp = deciles['Rough GDP 2015'].sum().apply(int)
median_gdp_pc = deciles['GDP per capita (2010 USD) 2015'].median().apply(int)
pct_capital = (100 * deciles['Is Capital'].sum() / deciles.size()).round(1)
pct_port = (100 * deciles['Is Port'].sum() / deciles.size()).round(1)
pct_pop_border = (100 * df[df['Distance to Border'] < 35].groupby('Initial MA decile')['Population 2015'].sum() / total_pop).round(1)

result = pd.concat(
    [median_ln_MA, largest_income_city, total_pop, median_pop, cagr_05_15, cagr_15_30, total_gdp, median_gdp_pc, pct_capital, pct_port, pct_pop_border],
    axis=1)
result.columns = ['Median ln MA', 'High Income', 'Lower Middle Income', 'Upper Middle Income', 'Total pop.', 'Median pop.', 'Pop. %CAGR 2005-15', 'Pop. %CAGR 2015-30', 'Total GDP', 'Median GDP per capita', '% capitals', '% ports', '% of pop. in border cities']

result.to_csv('final_tables_and_figures/table_market_access_deciles.csv')