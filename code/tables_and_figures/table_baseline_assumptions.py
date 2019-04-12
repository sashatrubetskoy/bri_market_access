# Alexandr (Sasha) Trubetskoy
# February 2019
# trub@uchicago.edu

import numpy as np

THETA = 5.03 # Elasticity parameter
ALPHA = 0.05 # Share of income paid to land
BETA = 0.65 # Labor share of market
SWITCHING_COST = 25

with open('final_tables_and_figures/table_transport_cost_sources.csv', 'r') as f:
    trade_costs = f.readlines()[-1].split(',')

with open('final_tables_and_figures/table_baseline_assumptions.csv', 'w') as f:
    f.write(',Parameter name,Explanation,Value\n')
    f.write('Freight rates,"Road, low quality",Single carriageway,{}\n'.format(trade_costs[2]))
    f.write('(USD/TEU/km),"Road, high quality",Motorway or dual carriageway,{}\n'.format(trade_costs[1]))
    f.write(',"Rail, low quality","Single-track, not electrified",{}\n'.format(trade_costs[4]))
    f.write(',"Rail, high quality",Double track or electrified,{}\n'.format(trade_costs[3]))
    f.write(',Sea,Maritime shipping route,{}\n'.format(trade_costs[6]))
    f.write('Other parameters,Theta,Intercity trade elasticity,{}\n'.format(THETA))
    f.write(',Alpha,Share of income paid to land,{}\n'.format(ALPHA))
    f.write(',Beta,Labor share of market,{}\n'.format(BETA))
    f.write(',Switching cost,Cost to switch between road and rail (USD),{}'.format(SWITCHING_COST))