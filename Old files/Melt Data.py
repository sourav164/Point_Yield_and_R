#import necessary libraries
import os, pandas as pd, numpy as np, fnmatch, 

#inputs the csv file and the location of the NDVI folder, finally create an output file
#following two lines must be changed
input_file = 'West_Bilsland_Point.csv'
path = r'F:\Sourav\All field Trip Data\WB'
#an output folder must be in the directory or create personal output location
output_file = os.path.join("Output", input_file)

#create dataframe and empty list 
raster = pd.read_csv(input_file)
df = pd.DataFrame(raster)
lent, wid = df.shape
sat_name = []

#num is list where number of the satellite image info will be stored and used
sats = ["*Intel*", "*PSC*",  "*Sent*",  "*RE*"]
num = []
for i in sats:
    m = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, i) and file.endswith("V1NDVI.tif"):
                m = m+1
    print (i, m)
    num.append(m)

# sat_name - A new column will contain name of the satellite for each data point
for i in range(num[0]*lent):
    sat_name.append("Intel")

for i in range(num[1]*lent):
    sat_name.append("PSC")
    
for i in range(num[2]*lent):
    sat_name.append("Senti")
    
for i in range(num[3]*lent):
    sat_name.append("RE")

#data frame melt
df2 = pd.melt(df,id_vars=['Point_ID'], var_name='Image Date', value_name='NDVI')
df2.shape

#take care of the duplicate dates
# multiple satellite images from different satellite image may contain the same day data. Thus, index will be the same
# Panda does not allow to have same index for multiple column. Thus, it adds .1 for the next duplicate index
for i in lst:
    new = i.replace(".1", "")
    df2= df2.replace(i, new)
df2["SAT"] = sat_name
lst = []
for i in df.dtypes.index:
    m = str(i)
    if ".1" in m:
        lst.append(i)

#data to keep and data to melt
df2 = pd.melt(df,id_vars=['Point_ID'], var_name='Image Date', value_name='NDVI')
for i in lst:
    new = i.replace(".1", "")
    df2= df2.replace(i, new)
df2["SAT"] = sat_name


#marge the point characterstics file and the melted data
ha = pd.read_csv("2018-11-26_PlotCombine_AllData_sorted.csv")
har = pd.DataFrame(ha)
df3 = pd.merge(df2, har, on='Point_ID')
df3.to_csv(output_file)
