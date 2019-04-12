#!/bin/bash

# Alexandr (Sasha) Trubetskoy
# April 2019
# trub@uchicago.edu

echo "Running with no terminal handling charges..." # + 25 mins = 25 mins
python code/analysis/get_cost_matrix.py -n prebri -port_fee 0 -o data/csv/cm_pre_handling.csv 
python code/analysis/get_cost_matrix.py -n postbri -port_fee 0 -o data/csv/cm_post_handling.csv 
python code/analysis/get_ma.py   -i data/csv/cm_pre_handling.csv   -o output/ma_pre_handling.csv
python code/analysis/get_ma.py   -i data/csv/cm_post_handling.csv  -o output/ma_post_handling.csv
python code/analysis/compare_outputs.py -a output/ma_pre_handling.csv    -b output/ma_post_handling.csv
echo "Done with no terminal handling charges."

echo "Running with population instead of GDP..." # + 25 mins = 50 mins
python code/analysis/get_ma.py   -i data/csv/cm_pre.csv  -market_size "Population 2015" -o output/ma_pre_pop.csv
python code/analysis/get_ma.py   -i data/csv/cm_post.csv -market_size "Population 2015" -o output/ma_post_pop.csv
python code/analysis/compare_outputs.py -a output/ma_pre_pop.csv    -b output/ma_post_pop.csv
echo "Done with population."

echo "Running with Oxford GDP estimate..." # + 25 mins = 75 mins
python code/analysis/get_ma.py   -i data/csv/cm_pre.csv  -market_size "Oxford GDP 2012" -o output/ma_pre_oxgdp.csv
python code/analysis/get_ma.py   -i data/csv/cm_post.csv -market_size "Oxford GDP 2012" -o output/ma_post_oxgdp.csv
python code/analysis/compare_outputs.py -a output/ma_pre_oxgdp.csv    -b output/ma_post_oxgdp.csv
echo "Done with Oxford GDP estimate."

echo "Running with simple average tariff..." # + 25 mins = 100 mins
python code/analysis/get_cost_matrix.py -n prebri -avg_tariff -o data/csv/cm_pre_avg_tariff.csv
python code/analysis/get_cost_matrix.py -n postbri -avg_tariff -o data/csv/cm_post_avg_tariff.csv 
python code/analysis/get_ma.py   -i data/csv/cm_pre_avg_tariff.csv   -o output/ma_pre_avg_tariff.csv
python code/analysis/get_ma.py   -i data/csv/cm_post_avg_tariff.csv  -o output/ma_post_avg_tariff.csv
python code/analysis/compare_outputs.py -a output/ma_pre_avg_tariff.csv    -b output/ma_post_avg_tariff.csv
echo "Done with simple average tariff."

echo "Running with labor market share β=0.8..." # + 20 mins = 120 mins
python code/analysis/get_ma.py   -i data/csv/cm_pre.csv  -b 0.8 -o output/ma_pre_beta_0.8.csv
python code/analysis/get_ma.py   -i data/csv/cm_post.csv -b 0.8 -o output/ma_post_beta_0.8.csv
python code/analysis/compare_outputs.py -a output/ma_pre_beta_0.8.csv    -b output/ma_post_beta_0.8.csv
echo "Done with labor market share β=0.8."

echo "Running with labor market share β=0..." # + 20 mins = 140 mins
python code/analysis/get_ma.py   -i data/csv/cm_pre.csv  -b 0.0 -o output/ma_pre_beta_0.0.csv
python code/analysis/get_ma.py   -i data/csv/cm_post.csv -b 0.0 -o output/ma_post_beta_0.0.csv
python code/analysis/compare_outputs.py -a output/ma_pre_beta_0.0.csv    -b output/ma_post_beta_0.0.csv
echo "Done with labor market share β=0."

echo "Running with θ=8.11, for agriculture..." # + 20 mins = 160 mins
python code/analysis/get_ma.py   -i data/csv/cm_pre.csv  -t 8.11 -o output/ma_pre_theta_8.11.csv
python code/analysis/get_ma.py   -i data/csv/cm_post.csv -t 8.11 -o output/ma_post_theta_8.11.csv
python code/analysis/compare_outputs.py -a output/ma_pre_theta_8.11.csv    -b output/ma_post_theta_8.11.csv
echo "Done with θ=8.11."

echo "Running with halfway reduction in costs..." # + 25 mins = 145 mins
python code/analysis/get_cost_matrix.py -n prebri -tcosts '_half' -o data/csv/cm_pre_half.csv
python code/analysis/get_cost_matrix.py -n postbri -tcosts '_half' -o data/csv/cm_post_half.csv 
python code/analysis/get_ma.py   -i data/csv/cm_pre_half.csv   -o output/ma_pre_half.csv
python code/analysis/get_ma.py   -i data/csv/cm_post_half.csv  -o output/ma_post_half.csv
python code/analysis/compare_outputs.py -a output/ma_pre_half.csv    -b output/ma_post_half.csv
echo "Done with halfway reduction in costs."

echo "Running with θ=15.72, for mining..." # + 20 mins = 165 mins
python code/analysis/get_ma.py   -i data/csv/cm_pre.csv  -t 15.72 -o output/ma_pre_theta_15.72.csv
python code/analysis/get_ma.py   -i data/csv/cm_post.csv -t 15.72 -o output/ma_post_theta_15.72.csv
python code/analysis/compare_outputs.py -a output/ma_pre_theta_15.72.csv    -b output/ma_post_theta_15.72.csv
echo "Done with θ=15.72."

echo "Running with no cost to switch between road and rail" # + 25 mins = 190 mins
python code/analysis/get_cost_matrix.py -n prebri -sw_fee 0 -o data/csv/cm_pre_sw0.csv
python code/analysis/get_cost_matrix.py -n postbri -sw_fee 0 -o data/csv/cm_post_sw0.csv 
python code/analysis/get_ma.py   -i data/csv/cm_pre_sw0.csv   -o output/ma_pre_sw0.csv
python code/analysis/get_ma.py   -i data/csv/cm_post_sw0.csv  -o output/ma_post_sw0.csv
python code/analysis/compare_outputs.py -a output/ma_pre_sw0.csv    -b output/ma_post_sw0.csv
echo "Done with no cost to switch between road and rail."

echo "Running with no tariffs or border costs..." # + 25 mins = 215 mins = 3.6 hrs
python code/analysis/get_cost_matrix.py -n prebri -no_intl_cost -o data/csv/cm_pre_no_intl.csv
python code/analysis/get_cost_matrix.py -n postbri -no_intl_cost -o data/csv/cm_post_no_intl.csv 
python code/analysis/get_ma.py   -i data/csv/cm_pre_no_intl.csv   -o output/ma_pre_no_intl.csv
python code/analysis/get_ma.py   -i data/csv/cm_post_no_intl.csv  -o output/ma_post_no_intl.csv
python code/analysis/compare_outputs.py -a output/ma_pre_no_intl.csv    -b output/ma_post_no_intl.csv
echo "Done with no tariffs or border costs."

echo "Running with ESCAP trade costs..." # + 25 mins = 240 mins = 4 hrs
python code/analysis/get_cost_matrix.py -n prebri -escap_wb -o data/csv/cm_pre_escap.csv
python code/analysis/get_cost_matrix.py -n postbri -escap_wb -o data/csv/cm_post_escap.csv 
python code/analysis/get_ma.py   -i data/csv/cm_pre_escap.csv   -o output/ma_pre_escap.csv
python code/analysis/get_ma.py   -i data/csv/cm_post_escap.csv  -o output/ma_post_escap.csv
python code/analysis/compare_outputs.py -a output/ma_pre_escap.csv    -b output/ma_post_escap.csv
echo "Done with ESCAP trade costs."

echo "Running with retail distribution costs..." # + 25 mins = 265 mins = 4.4 hrs
python code/analysis/get_ma.py   -i data/csv/cm_pre.csv -distribution_costs -o output/ma_pre_distrib.csv
python code/analysis/get_ma.py   -i data/csv/cm_post.csv -distribution_costs -o output/ma_post_distrib.csv
python code/analysis/compare_outputs.py -a output/ma_pre_distrib.csv    -b output/ma_post_distrib.csv
echo "Done with retail distribution costs."

echo "Creating sensitivity table..."
python code/tables_and_figures/table_sensitivity.py
echo "Sensitivity table created."

echo "Creating trade cost distribution table..."
python code/tables_and_figures/table_trade_cost_distributions.py
echo "Trade cost distribution table created."

# echo "Preparing files for Hummels & Schaur comparison..."
# python py/clean_hummels_schaur_data.py
# echo "Calculating market access baseline using H&S cities..."
# python py/get_ma.py -run -hs -matrix "_hs_baseline"
# echo "Calculating market access using H&S costs..."
# python py/get_ma.py -run -hs -matrix "_hs"
# echo "Exporting Hummels & Schaur result..."
# python py/tables_and_figures/table10note.py

echo "Done."