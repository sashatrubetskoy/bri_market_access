#!/bin/bash

# Alexandr (Sasha) Trubetskoy
# January 2019
# trub@uchicago.edu

echo "Installing packages..."
pip3 install --force-reinstall numpy==1.14.2
pip3 install --force-reinstall pandas==0.24.1
pip3 install --force-reinstall xlrd==1.1.0
pip3 install --force-reinstall unidecode==1.0.22
pip3 install --force-reinstall geopy==1.14.0
pip3 install --force-reinstall scipy==1.0.1
pip3 install --force-reinstall networkx==2.1
pip3 install --force-reinstall tqdm==4.31.1
pip3 install --force-reinstall pyproj==1.9.5.1
pip3 install --force-reinstall seaborn==0.9.0

echo "Necessary packages installed."
echo "Done."