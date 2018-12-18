#import necessary libraries
from datetime import datetime
import arcpy, os, fnmatch, csv
from arcpy.sa import *
from scipy import stats
import numpy as np, pandas as pd, matplotlib.pyplot as plt, matplotlib.dates as mdates 
from matplotlib.dates import DateFormatter

#things are subjected to change 
#the following two lines of codes should be kept as it is if used as script in ArcMAP
#if you want to use it as a raw code in python window then replace arcpy.GetParameterAsText(0) with appropriate text
#point - point shapefile of the yield map, path - where NDVI files are located
point = arcpy.GetParameterAsText(0)
path = arcpy.GetParameterAsText(1)

# dump folder - where unnecessary files will be saved
#a - python list contains yield data, xmin and xmax are the plotting date range
# Environment is geodatabase file
dump_folder = r"C:\GIS DUMP"
a = [i[0] for i in arcpy.da.SearchCursor(point, "Yield_bu_a")]
xmin = datetime(2018,4,15,0,0,0)
xmax = datetime(2018,9,30,0,0,0)
Environment = r'C:\GIS DUMP\script.gdb'
arcpy.env.workspace = Environment
arcpy.env.overwriteOutput = True
#no changes are necessary after this line

#create temporary file path
buffer_shape = os.path.join(dump_folder, "temp.shp")
poly_shape = os.path.join(Environment, "temp2")
temp_raster = os.path.join(Environment, "ts")

#csv and image save path
point_data = os.path.join(path, str(point+"_pt_based2_s.xls"))
writer = pd.ExcelWriter(point_data)
image = os.path.join(path, str(point+"_R_Square_s.png"))

#creating polygon from the point. If necessary adjust the buffer_distance_or_field for change in the polygon size
arcpy.Buffer_analysis(in_features=point, out_feature_class=buffer_shape, buffer_distance_or_field="3 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field="", method="PLANAR")
arcpy.FeatureEnvelopeToPolygon_management(in_features=buffer_shape, out_feature_class=poly_shape, single_envelope="SINGLEPART")

satellite = {"*Intel*": ["IntelinAir - 0.16m","ko"], "*PSC*":["PlanetScope - 3m","gv"],  "*Sent*":["Sentinal - 10m", "mp"],  "*RE*":["Rapid-Eye - 5m", "rd"]}


fig, ax = plt.subplots()

for item in satellite:
    #two dataframe will be created here
    df = pd.DataFrame()
    point_id = [i[0] for i in arcpy.da.SearchCursor(point, "Point_ID")]
    df["Point_ID"] = point_id
    df1 = pd.DataFrame()
    df1["Date"] = ["STD_Curve" , "Slope"  , "Intercept"  , "SAT", "R value"]
    
    #run each satellite data sources at once
    print (item)
    date_lst = []
    r_sq_lst = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, item) and file.endswith("V1NDVI.tif"):
                    Raster = os.path.join(root, file)
                    table = os.path.join(dump_folder, "tablea")
                    
                    #intel is high resolution, but for coarse resolution resampling are necessary for zonal statistics
                    if item=="*Intel*":
                        arcpy.gp.ZonalStatisticsAsTable_sa(poly_shape, "Point_ID", file, table, "DATA", "MEAN")
                    else:     
                        arcpy.Resample_management(in_raster=Raster, out_raster=temp_raster, cell_size="0.1 0.1", resampling_type="BILINEAR")
                        arcpy.gp.ZonalStatisticsAsTable_sa(poly_shape, "Point_ID", temp_raster, table, "DATA", "MEAN")
                    
                    #just - result of zonal statistics as a list to compare it with yield list 
                    just = [m[0] for m in arcpy.da.SearchCursor(table, "MEAN")]
                    
                    #some statistical info. Details are available here - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html                    
                    m = stats.linregress(a,just)[0]
                    c = stats.linregress(a,just)[1]
                    square_r = stats.linregress(a,just)[2]**2
                    std = stats.linregress(a,just)[4]
                    
                    #get the satellite name
                    sat =item.replace("*", "")
                    
                    #deal with the dates properly then append them to the list
                    da = file[-19:-11]
                    date =str(da[0:4]+"/"+da[4:6]+"/"+da[6:])
                    date_lst.append(date)
                    r_sq_lst.append(square_r)
                    
                    #add data to the pandas dataframe
                    df[date] = pd.Series(just)
                    df1[date] = [std, m, c, sat, square_r]
                    del table
                    print (Raster)
                    
    #write the dataframe into the excell file
    df.to_excel(writer,str(sat+"p"))
    df1.to_excel(writer,str(sat+"rR"))
    del df, df1
    
    #plot R^2 value for one satellite at a time
    if len(r_sq_lst)>0:
        #processing dates
        myDates= [datetime.strptime(date, '%Y/%m/%d').date() for date in date_lst]
        #plotting
        plt.plot(myDates, r_sq_lst, satellite[item][1], label = satellite[item][0])
        del date_lst, r_sq_lst
        #dealing with date format
        myFmt = DateFormatter("%m/%d")
        ax.xaxis.set_major_formatter(myFmt)
        fig.autofmt_xdate()

#plotting and cosmetic manipulation of the graph
plt.title("Spatial Resolution vs $R^2$ Value")
plt.xlabel("Dates")
plt.ylabel("$R^2$ Values")
ax.tick_params(axis='both', which='major', labelsize=8)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
plt.xlim([xmin, xmax])
plt.legend(bbox_to_anchor=(0.01, 0.99), loc=2, borderaxespad=0., prop={'size': 7})
plt.savefig(image, dpi = 1000, quality = 100, edgecolor= 'red', )

#save the spreedsheet file
writer.save()
