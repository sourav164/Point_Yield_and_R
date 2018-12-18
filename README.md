# Zonal+Regression+resolutionplot_script.py
Python Version: 2.7 with ArcMap 10.6.

Before running this script load all the NDVI images from the local directories to ArcMap. 

Create a script in the ArcMap catalog then create two input for the script - folder location of the NDVI file and the point shapefile.

It will create one R^2 plot and one point data in the NDVI folder.


# NDVI_Average.py
Python Version: 3.5 with ArcGIS Pro 2.

Not necessary to load any data to the ArcGIS. Just insert the file path and run the code.

A excel file will be created on the file directory.

# Data Frame Edit.py
The excell file created using Zonal+Regression+resolutionplot_script.py are not well organized. This code will organize them and create single sheet, finally save them into the desired location in csv format.

# Melt Data.py
Takes multiple input manually and better not to run before full comments are added (in current version, some comments are missing).

This script will melt the point NDVI data then add each points properties into a new excel file.

# Rplot.rmd
Must not be used at any case. Details description will be added.
