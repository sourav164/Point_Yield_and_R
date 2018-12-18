from datetime import datetime
import arcpy, os, fnmatch, csv
from arcpy.sa import *
from scipy import stats
import numpy as np, pandas as pd, matplotlib.pyplot as plt, matplotlib.dates as mdates 
from matplotlib.dates import DateFormatter

#things are subjected to change
point = arcpy.GetParameterAsText(0)
path = arcpy.GetParameterAsText(1)

dump_folder = r"C:\GIS DUMP"
a = [i[0] for i in arcpy.da.SearchCursor(point, "Yield_bu_a")]
xmin = datetime(2018,4,15,0,0,0)
xmax = datetime(2018,9,30,0,0,0)
#input things above
Environment = r'C:\GIS DUMP\script.gdb'
arcpy.env.workspace = Environment
arcpy.env.overwriteOutput = True


buffer_shape = os.path.join(dump_folder, "temp.shp")
poly_shape = os.path.join(Environment, "temp2")
temp_raster = os.path.join(Environment, "ts")

#csv and image save path
point_data = os.path.join(path, str(point+"_pt_based2_s.xls"))
writer = pd.ExcelWriter(point_data)


image = os.path.join(path, str(point+"_R_Square_s.png"))

arcpy.Buffer_analysis(in_features=point, out_feature_class=buffer_shape, buffer_distance_or_field="3 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field="", method="PLANAR")
arcpy.FeatureEnvelopeToPolygon_management(in_features=buffer_shape, out_feature_class=poly_shape, single_envelope="SINGLEPART")

satellite = {"*Intel*": ["IntelinAir - 0.16m","ko"], "*PSC*":["PlanetScope - 3m","gv"],  "*Sent*":["Sentinal - 10m", "mp"],  "*RE*":["Rapid-Eye - 5m", "rd"]}


fig, ax = plt.subplots()

for item in satellite:

    df = pd.DataFrame()
    point_id = [i[0] for i in arcpy.da.SearchCursor(point, "Point_ID")]
    df["Point_ID"] = point_id

    df1 = pd.DataFrame()
    df1["Date"] = ["STD_Curve" , "Slope"  , "Intercept"  , "SAT", "R value"]

    print (item)
    date_lst = []
    r_sq_lst = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, item) and file.endswith("V1NDVI.tif"):
                    Raster = os.path.join(root, file)
                    #table_name = "a"+file[-19:-11]+'.dbf'
                    table = os.path.join(dump_folder, "tablea")
                    if item=="*Intel*":
                        arcpy.gp.ZonalStatisticsAsTable_sa(poly_shape, "Point_ID", file, table, "DATA", "MEAN")
                    else:     
                        arcpy.Resample_management(in_raster=Raster, out_raster=temp_raster, cell_size="0.1 0.1", resampling_type="BILINEAR")
                        arcpy.gp.ZonalStatisticsAsTable_sa(poly_shape, "Point_ID", temp_raster, table, "DATA", "MEAN")
                    just = [m[0] for m in arcpy.da.SearchCursor(table, "MEAN")]

                    #some statistical info
                    m = stats.linregress(a,just)[0]
                    c = stats.linregress(a,just)[1]
                    square_r = stats.linregress(a,just)[2]**2
                    std = stats.linregress(a,just)[4]
                    
                    #edit for right name
                    sat =item.replace("*", "")
                    
                    #deal with the dates properly
                    da = file[-19:-11]
                    date =str(da[0:4]+"/"+da[4:6]+"/"+da[6:])
                    date_lst.append(date)
                    r_sq_lst.append(square_r)
                    

                    #sq.update({file[-19:-8]: square_r})
                    df[date] = pd.Series(just)
                    df1[date] = [std, m, c, sat, square_r]
                    del table
                    print (Raster)
                    
    df.to_excel(writer,str(sat+"p"))
    df1.to_excel(writer,str(sat+"rR"))
    del df, df1
    
    
    if len(r_sq_lst)>0:
        #processing dates
        myDates= [datetime.strptime(date, '%Y/%m/%d').date() for date in date_lst]
        #plotting
        plt.plot(myDates, r_sq_lst, satellite[item][1], label = satellite[item][0])
        del date_lst, r_sq_lst
        #ax.legend()
        myFmt = DateFormatter("%m/%d")
        ax.xaxis.set_major_formatter(myFmt)
        fig.autofmt_xdate()
        #plotting with dates  
plt.title("Spatial Resolution vs $R^2$ Value")
plt.xlabel("Dates")
plt.ylabel("$R^2$ Values")
ax.tick_params(axis='both', which='major', labelsize=8)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
plt.xlim([xmin, xmax])
plt.legend(bbox_to_anchor=(0.01, 0.99), loc=2, borderaxespad=0., prop={'size': 7})
plt.savefig(image, dpi = 1000, quality = 100, edgecolor= 'red', )


writer.save()