### Replication files for Reed, Tristan; Trubetskoy, Alexandr. 2019. _Assessing the Value of Market Access from Belt and Road Projects (English)_.

The files in this folder produce the tables and figures in the paper. 

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

## Step 0
> Make sure you have doen this before starting the replication procedure.

First, download the raw data by [clicking here](https://drive.google.com/open?id=1Vf128LuV_80CAubukTDQ9Mb-xls082RZ). Unzip the file, then move the folder `data` into the top-level, `bri_market_access` directory.

## Step 1
> ⏳ This step takes approximately **30 minutes** to run.

Step 1 generates the following tables and figures:

  + Table: **Transport cost sources**
  + Table: **Baseline assumptions**
  + Table: **Market acccess deciles**
  + Figure: **Trade vs. size**
  + Figure: **Trade cost asymmetry**
  + Figure: **Added value by country**
  + Figure: **Trade cost vs. distance**
  + Figure: **Pop. growth vs MA change**

These tables and figures do not require significant calculations beyond running the baseline scenario. From the `bri_ma_replication` directory, run

```bash
./step_1.sh
```

## Step 2
> ⏳ This step takes approximately **4.5 hours** to run.

Step 2 generates the following tables and figures:

  + Table: **Sensitivity**
  + Table: **Trade cost distributoins**

These tables require running the various sensitivity scenarios. From the `bri_ma_replication` directory, run

```bash
./step_2.sh
```

## Step 3
> ⏳ This step takes approximately **50 hours** to run.

Step 3 generates the following figure:

  + Table: **Top project for cities**
  + Table: **Top projects**

These require calculating the effects of 71 projects under two different scenarios each.

```bash
./step_3.sh
```

## Remaining tables and figures
Table "Representation" is not generated from data.

Tables "Current status of top projects" and "Projects reduced or scaled down" contain discussion of results from Table "Top projects" and are created manually. 

Figures "BRI overview", "Change in log market access" and "Change in land value" are maps that can be created from the shapefiles and data provided.