# Alexandr (Sasha) Trubetskoy
# February 2019
# trub@uchicago.edu

import pandas as pd

dfs = []
filenames = [
    'output/compare_ma_pre_ma_post.csv',
    'output/compare_ma_pre_beta_0.8_ma_post_beta_0.8.csv',
    'output/compare_ma_pre_theta_8.11_ma_post_theta_8.11.csv',
    'output/compare_ma_pre_sw0_ma_post_sw0.csv',
    'output/compare_ma_pre_beta_0.0_ma_post_beta_0.0.csv',
    'output/compare_ma_pre_distrib_ma_post_distrib.csv',
    'output/compare_ma_pre_half_ma_post_half.csv',
    'output/compare_ma_pre_theta_15.72_ma_post_theta_15.72.csv',
    'output/compare_ma_pre_handling_ma_post_handling.csv',
    'output/compare_ma_pre_avg_tariff_ma_post_avg_tariff.csv',
    'output/compare_ma_pre_external_ma_post_external.csv',
    'output/compare_ma_pre_pop_ma_post_pop.csv',
    'output/compare_ma_pre_oxgdp_ma_post_oxgdp.csv',
    'output/compare_ma_pre_escap_ma_post_escap.csv',
    'output/compare_ma_pre_no_intl_ma_post_no_intl.csv'
    ]

for filename in filenames:
    dfs.append(pd.read_csv(filename)[['ID', 'dif']].set_index('ID'))

a = pd.concat(dfs, axis=1)
a.columns = [
    'Baseline',
    'Labor market share β=0.8',
    'θ=8.11, for agriculture', 
    'No cost to switch between road and rail', 
    'Labor market share β=0',
    'Add retail distribution costs',
    'Halfway reduction in trade costs',
    'θ=15.72, for mining', 
    'No terminal handling charges', 
    'Using simple average tariff',
    'Add external markets',
    'Using population instead of GDP for market size',
    'Oxford Economics GDP',
    'ESCAP-WB tariffs and border costs',
    'No tariffs or border costs'
    ]

a.corr('spearman').round(2).to_csv('final_tables_and_figures/table_sensitivity.csv')