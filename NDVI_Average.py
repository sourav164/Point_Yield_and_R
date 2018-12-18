#import necessary libraries
import os, fnmatch, arcpy, numpy, pandas as pd
import numpy as np
from arcpy.sa import *

#insert path of the folders where NDVI files are located
l_list = []

for path in l_list:
    i, j = os.path.split(path)
    print (j)
    
    satellite = {"*Intel*": ["IntelinAir - 0.16m","ko"], "*PSC*":["PlanetScope - 3m","gv"],  "*Sent*":["Sentinal - 10m", "mp"],  "*RE*":["Rapid-Eye - 5m", "rd"]}
    #create a excel file to write
    point_data = os.path.join(path, str(j+"_average.xls"))
    writer = pd.ExcelWriter(point_data)
    
    #one satelite at a time
    for item in satellite:
        df1 = pd.DataFrame()
        df1["Date"] = ["Mean",    "5 Percentile"   , "95 Percentile" ,  "Standard Deviation", "SAT" ]
        
        print (item)
        for root, dirs, files in os.walk(path):
                for file in files:
                        if fnmatch.fnmatch(file, item) and file.endswith("V1NDVI.tif"):
                                #convert the raster into a numpy array then get properties
                                original = os.path.join(root, file)
                                array = arcpy.RasterToNumPyArray(Raster(original),nodata_to_value=9999)
                                marray = np.ma.masked_values(array,9999)
                                mean = np.mean(marray)
                                five = np.percentile(marray.compressed(),(5))
                                ninefive= np.percentile(marray.compressed(),(95))
                                std= np.std(marray)
                                sat_name =item.replace("*", "")
                                

                                #write data to the file
                                da = file[-19:-11]
                                date =str(da[0:4]+"/"+da[4:6]+"/"+da[6:])
                                df1[date] = [mean, five, ninefive, std, sat_name]

                                del marray, array

        df1.to_excel(writer,str(sat_name+"r"))
        del  df1
    writer.save()

