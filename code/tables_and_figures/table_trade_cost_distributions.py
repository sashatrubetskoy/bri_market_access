# Alexandr (Sasha) Trubetskoy
# February 2019
# trub@uchicago.edu

import pandas as pd
import numpy as np
PARAMS = pd.read_csv('parameters/market_access_parameters.csv').set_index('parameter').to_dict()['value']

result = {}

# Baseline
costs = pd.read_csv('data/csv/cm_pre.csv', index_col=0).sort_index(axis=1).sort_index(axis=0)
tau_od = np.ndarray.flatten(np.tril(costs.values).T)
tau_od = tau_od[tau_od!=0] + 1
values = [min(tau_od), np.percentile(tau_od, 10), np.percentile(tau_od, 25), np.percentile(tau_od, 50),
          np.percentile(tau_od, 75), np.percentile(tau_od, 90), max(tau_od)]
result['Baseline'] = values

# No tariffs or border costs
costs = pd.read_csv('data/csv/cm_pre_no_intl.csv', index_col=0).sort_index(axis=1).sort_index(axis=0)
tau_od = np.ndarray.flatten(np.tril(costs.values).T)
tau_od = tau_od[tau_od!=0] + 1
values = [min(tau_od), np.percentile(tau_od, 10), np.percentile(tau_od, 25), np.percentile(tau_od, 50),
          np.percentile(tau_od, 75), np.percentile(tau_od, 90), max(tau_od)]
result['No tariffs or border costs'] = values

# ESCAP-WB trade costs
costs = pd.read_csv('data/csv/cm_pre_escap.csv', index_col=0).sort_index(axis=1).sort_index(axis=0)
tau_od = np.ndarray.flatten(np.tril(costs.values).T)
tau_od = tau_od[tau_od!=0] + 1
values = [min(tau_od), np.percentile(tau_od, 10), np.percentile(tau_od, 25), np.percentile(tau_od, 50),
          np.percentile(tau_od, 75), np.percentile(tau_od, 90), max(tau_od)]
result['ESCAP-WB trade costs'] = values

# Add retail distribution
costs = pd.read_csv('data/csv/cm_pre.csv', index_col=0).sort_index(axis=1).sort_index(axis=0)
tau_od = np.ndarray.flatten(np.tril(costs.values).T)
tau_od = tau_od[tau_od!=0] + 1
tau_od = tau_od*PARAMS['distribution_cost']
values = [min(tau_od), np.percentile(tau_od, 10), np.percentile(tau_od, 25), np.percentile(tau_od, 50),
          np.percentile(tau_od, 75), np.percentile(tau_od, 90), max(tau_od)]
result['Add retail distribution'] = values

res_df = pd.DataFrame(result).T
res_df.columns = ['Min', '10', '25', '50', '75', '90', 'Max']
res_df = res_df.round(5)
res_df.to_csv('final_tables_and_figures/table_trade_cost_distributions.csv')