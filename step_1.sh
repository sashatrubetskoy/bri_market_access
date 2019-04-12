#!/bin/bash

# Alexandr (Sasha) Trubetskoy
# April 2019
# trub@uchicago.edu

echo "Cleaning city data..."
python code/cleaning/clean_city_data.py
echo "City data cleaned."

echo "Creating transport costs sources table..."
python code/tables_and_figures/table_transport_cost_sources.py
echo "Table created: Transport cost sources."

echo "Creating basic assumptions table..."
python code/tables_and_figures/table_baseline_assumptions.py
echo "Table created: Baseline assumptions."

echo "Calculating cost matrices for baseline..." # + 5 mins = 5 mins
python code/analysis/get_cost_matrix.py -o data/csv/cm_pre.csv -n prebri -f
python code/analysis/get_cost_matrix.py -o data/csv/cm_post.csv -n postbri
echo "Calculating market access for baseline..." # + 20 mins = 25 mins
python code/analysis/get_ma.py     -i data/csv/cm_pre.csv            -o output/ma_pre.csv
python code/analysis/get_ma.py     -i data/csv/cm_post.csv           -o output/ma_post.csv
python code/analysis/compare_outputs.py -a output/ma_pre.csv    -b output/ma_post.csv
echo "Market access baseline done."

echo "Creating trade vs size figure..."
python code/tables_and_figures/figure_trade_vs_size.py
echo "Table created: Baseline assumptions."

echo "Creating MA deciles table..."
python code/tables_and_figures/table_market_access_deciles.py
echo "Table created: MA deciles."

echo "Creating figure: Trade cost asymmetry..."
python code/tables_and_figures/figure_trade_cost_asymmetry.py
echo "Figure created: Trade cost asymmetry"

echo "Creating figure: Added value by country..."
python code/tables_and_figures/figure_added_value_by_country.py
echo "Figure created: Added value by country"

echo "Creating figure: Added value by country..."
echo "Calculating distance matrix..." # + 2 mins = 27 mins
python code/analysis/get_cost_matrix.py -o data/csv/distance_pre.csv -n prebri -distance
python code/tables_and_figures/figure_trade_cost_vs_distance.py
echo "Figure created: Added value by country"

echo "Creating figure: Pop. growth vs MA change..."
echo "Calculating market access in year 2000..."
python code/analysis/get_ma.py   -i data/csv/cm_pre.csv    -o output/ma_pre_2000.csv -market_size "Rough GDP 2000"
python code/tables_and_figures/figure_growth_vs_ma_change.py
echo "Figure created: Pop. growth vs MA change."

echo "Done."