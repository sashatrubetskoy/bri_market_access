import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

GDP_FILE = 'data/other/raw_china_trade/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_10515210.csv'
TRADE_FILE = 'data/other/raw_china_trade/comtrade.csv'

gdp = pd.read_csv(GDP_FILE, skiprows=3)[['Country Code', '2017']].set_index('Country Code')
trade = pd.read_csv(TRADE_FILE)
imports = trade[trade['Trade Flow']=='Import'][['Partner ISO', 'Trade Value (US$)']].set_index('Partner ISO')
exports = trade[trade['Trade Flow']=='Export'][['Partner ISO', 'Trade Value (US$)']].set_index('Partner ISO')

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

EURASIA_COUNTRIES = ['AFG', 'NPL', 'MDA', 'TJK', 'BIH', 'GEO', 'MKD', 'KGZ', 'MAC',
                     'LVA', 'HRV', 'LTU', 'EST', 'ALB', 'ARM', 'LKA', 'GRC', 'BGD',
                     'BLR', 'AZE', 'BGR', 'UZB', 'KHM', 'LAO', 'MNG', 'FIN', 'MMR',
                     'UKR', 'SVK', 'PRT', 'PAK', 'POL', 'TUR', 'HUN', 'KAZ', 'CZE',
                     'DNK', 'HKG', 'IRL', 'SWE', 'ESP', 'IND', 'ITA', 'GBR', 'FRA',
                     'RUS', 'DEU', 'CHE', 'IRN', 'THA', 'SGP', 'MYS', 'VNM', 'NOR',
                     'AUT', 'BEL', 'TKM', 'NLD']


# Set GRC at (0, 0)
log_exp_GRC = np.log(exports.loc['GRC', 'Trade Value (US$)'])
log_imp_GRC = np.log(imports.loc['GRC', 'Trade Value (US$)'])
log_gdp_GRC = np.log(gdp.loc['GRC', '2017'])

for iso3 in EURASIA_COUNTRIES:
    conditions = [iso3 in df.index for df in [exports, imports, gdp]]
    if not all(conditions):
        continue

    log_exp = np.log(exports.loc[iso3, 'Trade Value (US$)']) - log_exp_GRC
    log_imp = np.log(imports.loc[iso3, 'Trade Value (US$)']) - log_imp_GRC
    log_gdp = np.log(gdp.loc[iso3, '2017']) - log_gdp_GRC

    if (not np.isinf(log_exp)) and (not np.isinf(log_imp)):
        axs[0].scatter(log_gdp, log_exp, color='white')
        axs[0].text(log_gdp, log_exp, s=iso3)
        axs[1].scatter(log_gdp, log_imp, color='white')
        axs[1].text(log_gdp, log_imp, s=iso3)


# RUN REGRESSION
sel_gdp = gdp.loc[EURASIA_COUNTRIES]
sel_imp = imports.loc[EURASIA_COUNTRIES]
sel_exp = exports.loc[EURASIA_COUNTRIES]
XX = np.log(sel_gdp['2017']).values - log_gdp_GRC
G = np.array([XX, np.ones(len(EURASIA_COUNTRIES))]).T
Y_0 = np.log(sel_exp['Trade Value (US$)'])-log_exp_GRC
Y_1 = np.log(sel_imp['Trade Value (US$)'])-log_imp_GRC
x = np.array([-4, 4])

result_0 = np.linalg.lstsq(G, Y_0)
m0, c0 = result_0[0]
axs[0].plot(x, m0*x + c0, 'r', label='Fitted line')

result_1 = np.linalg.lstsq(G, Y_1)
m1, c1 = result_1[0]
axs[1].plot(x, m1*x + c1, 'r', label='Fitted line')

# NOTE SLOPE, STDERR, R2
resids_0 = [y - (m0*x + c0) for x, y in zip(XX, Y_0)]
stderr_0 = np.sqrt(np.var(resids_0) / sum([x**2 for x in XX]))
ss_res = sum([x**2 for x in resids_0])
ss_tot = sum([(y - np.mean(Y_0))**2 for y in Y_0])
r2_0 = 1 - ss_res/ss_tot
axs[0].text(-3, -5.5, s='Slope: {:.2f} ({:.2f}), R-squared fit = {:.2f}'.format(m0, stderr_0, r2_0))

resids_1 = [y - (m1*x + c1) for x, y in zip(XX, Y_1)]
stderr_1 = np.sqrt(np.var(resids_1) / sum([x**2 for x in XX]))
ss_res = sum([x**2 for x in resids_1])
ss_tot = sum([(y - np.mean(Y_1))**2 for y in Y_1])
r2_1 = 1 - ss_res/ss_tot
axs[1].text(-3, -5.5, s='Slope: {:.2f} ({:.2f}), R-squared fit = {:.2f}'.format(m1, stderr_1, r2_1))

# SET TITLES AND BOUNDS
axs[0].title.set_text("(a) China's exports in 2017")
axs[0].set_xlim([-4, 4])
axs[0].set_ylim([-6, 6])

axs[1].title.set_text("(b) China's imports in 2017")
axs[1].set_xlim([-4, 4])
axs[1].set_ylim([-6, 6])

plt.tight_layout()
plt.savefig('final_tables_and_figures/figure_trade_vs_size.png')