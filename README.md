### Replication files for Reed, Tristan, and Alexandr Trubetskoy (2018) “The Belt and Road Initiative and the Value of Urban Land.”

The files in this folder produce the tables and figures in the paper. 

## Contents
- **Required Packages**
- **Replication Procedure**
	1. Prepare data
	2. Generate Tables 2, 4
	3. Generate Table 8
	4. Generate Tables X, X and X
- **Description of Files**
	1. Data
		- 1.1 `city_data`
		- 1.2 `shapefiles_bri`
		- 1.3 `shapefiles_general`
	2. Cleaning

## Required Packages

All code is in python. The instructions assume that Python 3.4 is default, being run from Terminal on MacOS High Sierra 10.13. Some versions of python later than 3.4 are known to cause problems.

The following non built-in python packages are required:

| Package | Version used | Purpose |
|:------- |:------------ |:------- |
|NumPy    |1.14.2        |Mathematical operations|
|Pandas   |0.22          |Read and manipulate CSV and Excel data|
|Xlrd     |1.1.0         |Required for Pandas to read Excel|
|Unidecode|1.0.22        |Convert Unicode strings with accents into simple ASCII characters|
|GeoPy    |1.14.0        |Geographical distance calculation|
|SciPy    |1.0.1         |Ne﻿arest neighbor calculations|
|NetworkX |2.1           |Network analysis, shortest path|
|Tqdm     |4.23.0        |Draws progress bars|
|PyProj   |1.9.5.1       |Converts ﻿coordinates to X, Y|
|Matplotlib|2.2.3        |Generates graphs|
|Statsmodels|0.9.0       |Runs regressions|
|Seaborn  |0.9.0         |Runs nonparametric estimation|

The above packages can all be installed using pip. For convenience, a script has been provided, which can be run from the `bri_ma_replication` directory:

```bash
./install_packages.sh
```

# Replication Procedure

Due to the large computation time required to produce the results, the replication procedure is split into 6 steps.

It is important that the steps be followed in order, since each requires the results from the previous step.

## Step 0 (data prep)
> ⏳ This step takes approximately **3 minutes** to run.

First, download the Hummels & Schaur trade cost dataset by [clicking here](https://drive.google.com/file/d/1beTfqVwBnDOCKq4_IR8BNsyFXfQw633u/view?usp=sharing). Unzip the file if necessary, then move it into the following directory: `data/raw_hummels_schaur_data/`

Next, from the `bri_ma_replication` directory, run

```bash
python py/clean_city_data.py
```

This will take the raw city data and combine it into the file that we need. It will also project the city coordinates to add X, Y columns. The result will be located at `data/cleaning_outputs/cities_xy.csv`.

## Step 1
Step 1 generates the following tables:

  + Table: **Transport cost sources**
  + Table: **Baseline assumptions**  

These tables do not require significant calculations. From the `bri_ma_replication` directory, run

```bash
./step_1.sh
```

## Step 2
> ⏳ This step takes approximately **40 minutes** to run.

Step 2 generates the following tables and figures:

  + Table: **Market acccess deciles**
  + Figure: **Trade cost asymmetry**
  + Figure: **Added value by country**

These tables and figures only require running the baseline scenario. From the `bri_ma_replication` directory, run

```bash
./step_2.sh
```

## Step 3
> ⏳ This step takes approximately **20 minutes** to run.

Step 3 generates the following figure:

  + Figure: **Trade cost vs. distance**

This requires creating a distance matrix, in addition to the baseline. From the `bri_ma_replication` directory, run

```bash
./step_3.sh
```

## Step 4
> ⏳ This step takes approximately **40 minutes** to run.

Step 4 generates the following figure:

  + Figure: **Growth vs. MA change**

This requires running the baseline model for the year 2000. From the `bri_ma_replication` directory, run

```bash
./step_4.sh
```

## Step 5
> ⏳ This step takes approximately **5 hours** to run.

Step 4 generates the following table:

  + Table: **Sensitivity**

This requires running all of the sensitivity scenarios. From the `bri_ma_replication` directory, run

```bash
./step_5.sh
```

## Step 6
> ⏳ This step takes approximately **70 hours** to run.

Step 6 generates the following table:

  + Table: **Top projects**
  + Table: **Top projects for cities**

Tables 6 and 7 require calculating the effects of 71 projects under two different scenarios each. 

```bash
./step_6.sh
```

## Step 7 (no computation)
Table "Representation" is not generated from data.

Tables "Current status of top projects" and "Projects reduced or scaled down" contain discussion of results from Table "Top projects" and are created manually. 

Figures "BRI overview", "Change in log market access" and "Change in land value" are maps that can be created from the shapefiles and data provided.


# Description of Files
### 1. Data
#### 1.1 `cost_matrices`
`cost_matrices/hummels_schaur` contains cost matrices for cities with trade costs derived from data by De Soyres, per Hummels and Schaur 2014.

`cost_matrices/overall` will contain cost matrices for BRI under baseline and various sensitivity scenarios.

`cost_matrices/projects` will contain cost matrices for the construction of each of 71 BRI projects in complement and in isolation.

#### 1.2 `csv`
`csv/border_costs.csv` contains tariffs (ad valorem) and border costs (USD) for country pairs per Doing Business Indicators.

`csv/cities_hummels_schaur.csv` contains data on a subset of Eurasian cities that match with De Soyres data.

`csv/cities.csv` contains data on Eurasian cities. It is the result of running `clean_city_data.py`.

#### 1.3 `gis_data_bri`
`gis_data_bri/ports.geojson` has all top-100 world ports by throughput, according to Lloyd's List, that are within the contiguous Eurasian transport network. It also contains several ports proposed under BRI that are not in the top 100.

`gis_data_bri/rail_len.geojson` has the contiguous Eurasian railway network.

`gis_data_bri/road_len.geojson` has the contiguous Eurasian road network.

`gis_data_bri/sea_links.geojson` has major shipping routes that connect the ports in `ports.geojson`.

#### 1.4 `gis_data_general`
`gis_data_bri/borders.geojson` has borders between countries as recognized by the World Bank in GeoJSON format. This file is used to calculate border distance for cities.

#### 1.5 `market_access`
This folder contains the outputs of `py/get_ma.py`.

#### 1.6 `raw_city_data`
`raw_city_data/API_NY.GDP.PCAP.KD_DS2_en_excel_v2_9986143.xls` contains World Bank estimates for GDP per capita in constant 2010 US dollars for years 1960–2017. It is available on the [World Bank Open Data website](https://data.worldbank.org/indicator/ny.gdp.pcap.kd).

`raw_city_data/CLASS.xls` contains the World Bank classification of countries into regions, as well as 2018 income classifications which are not used. It can be downloaded from the [World Bank Data Help Desk](http://databank.worldbank.org/data/download/site-content/OGHIST.xls).

`raw_city_data/iso.csv` contains ISO numeric codes (used by the UN) and three-letter codes (used by the World Bank). Data was copy-pasted from the [ISO website](https://www.iso.org/obp/ui/#search).

`raw_city_data/lloyds_2016` is a screenshot of the “One Hundred Ports 2016, Digital Edition”, which contains the top 100 container ports by annual throughput in 2015. The original publication can be viewed on the [Lloyd’s List website](https://lloydslist.maritimeintelligence.informa.com/one-hundred-container-ports-2016/one-hundred-digital-edition-2016).

`raw_city_data/OGHIST.xls` contains historical World Bank income classifications of countries. The classifications for calendar year 2015 are used. It can be downloaded from the [World Bank Data Help Desk](http://databank.worldbank.org/data/download/site-content/OGHIST.xls).

`raw_city_data/ports.txt` contains a list of cities whose ports handled more than 5 million TEU in 2015 according to One Hundred Ports 2016, saved in city_data/lloyds_2016.

`raw_city_data/WUP2018-F12-Cities_Over_300K.xls` contains populations of urban agglomerations with 300,000 inhabitants or more for years 1950–2035. It can be downloaded at the World Urbanization Prospects 2018 [downloads page](https://esa.un.org/unpd/wup/Download/) under “Urban Agglomerations”.

`raw_city_data/WUP2018-F13-Capital_Cities.xls` contains a list of capital cities as recognized by the United Nations. It can be downloaded at the World Urbanization Prospects 2018 [downloads page](https://esa.un.org/unpd/wup/Download/) under “Urban Agglomerations”.

#### 1.7 `raw_hummels_schaur_data`
`raw_hummels_schaur_data/city_name_conversions.txt` contains a dictionary for conversion between the Hummels and Schaur and UN dataset city names.

`raw_hummels_schaur_data/City_pair_Regional_dataset_Lower_Bound.dta`, _when placed into this folder,_ is to have city pair trade costs expressed in hours in Stata format.

`raw_hummels_schaur_data/iso2_to_iso3.json` has a conversion from ISO2 to ISO3 country codes, since the Stata file uses ISO2, while the World Bank data uses ISO3.

### 2. `install_packages.sh`
Running this file installs the necessary packages via pip.

### 3. `py`
`py/clean_city_data.py` takes files from `data/raw_city_data` and creates `data/csv/cities.csv`.

`py/clean_hummels_schaur_data.py` takes files from `data/raw_hummels_schaur_data` and creates `data/csv/cities_hummels_schaur.csv`.

`py/get_cost_matrices.py` computes ad valorem costs between cities and outputs the pre- and post-BRI cost matrices to `data/cost_matrices`.

`py/get_ma.py` calculates the market access for every city given a specified cost matrix, taking `csv/cities.csv`, adding market access data, and exporting to `data/market_access`.

`py/run_all_projects.py` runs a cost matrix and market access calculation for each project in isolation and in complement, in order to generate project rankings.

`py/tables_and_figures` contains python files to generate every table and figure.

`py/unused` contains miscellaneous python files which are not used in the final paper but may be of use to analysts attempting to generate other charts.

### 4. `results`
This folder contains the final outputted figures and tables.

### 5. `step_x.sh`
These shell files run the appropriate scripts to generate the tables and figures sequentially.
