# Zonal+Regression+resolutionplot_script.py
Python Version: 2.7 with ArcMap 10.6.

Before running this script load all the NDVI images from the local directories to ArcMap. 

Create a script in the ArcMap catalog, then create two inputs for the script - the folder location of the NDVI file and the point shapefile.

It will create one R^2 plot and one point data in the NDVI folder.


# NDVI_Average.py
Python Version: 3.5 with ArcGIS Pro 2.

It is not necessary to load any data to the ArcGIS. Insert the file path and run the code.

An Excel file will be created in the file directory.

# Data Frame Edit.py
The Excel file created using Zonal+Regression+resolutionplot_script.py is not well organized. This code will organize them and create a single sheet, finally save them into the desired location in CSV format.

# Melt Data.py
It takes multiple inputs manually and it is better not to run before full comments are added (in the current version, some comments are missing).
This script will melt the point NDVI data and then add each point's properties into a new Excel file.

