#import necessary libraries
import os, pandas as pd, numpy as np, fnmatch, 

#inputs the csv file then create a new dataframe
input_file = 'Point_West_bilsland.csv'
output_file = os.path.join("Output", input_file)
raster = pd.read_csv(input_file)
df = pd.DataFrame(raster)

lent, wid = df.shape
sat_name = []

#the following integer inside the range must be inserted manually by observing the number of NDVI file for each satellite
for i in range(15*lent):
    sat_name.append("Intel")

for i in range(10*lent):
    sat_name.append("PSC")
    
for i in range(7*lent):
    sat_name.append("Senti")
    
for i in range(2*lent):
    sat_name.append("RE")


#take care of the duplicate dates
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
df2.head()

#marge the point characterstics file and the melted data
ha = pd.read_csv("harvest.csv")
har = pd.DataFrame(ha)
df3 = pd.merge(df2, har, on='Point_ID')
df3.to_csv(output_file)
