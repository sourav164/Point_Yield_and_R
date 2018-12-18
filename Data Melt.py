
# coding: utf-8

# In[155]:


import os, pandas as pd, numpy as np, fnmatch, glob
glob.glob('*.csv')


# In[182]:


#inputs
input_file = 'Point_West_bilsland.csv'
output_file = os.path.join("Output", input_file)
raster = pd.read_csv(input_file)
df = pd.DataFrame(raster)

lent, wid = df.shape
sat_name = []
for i in range(15*lent):
    sat_name.append("Intel")

for i in range(10*lent):
    sat_name.append("PSC")
    
for i in range(7*lent):
    sat_name.append("Senti")
    
for i in range(2*lent):
    sat_name.append("RE")


# In[183]:


lst = []
for i in df.dtypes.index:
    m = str(i)
    if ".1" in m:
        lst.append(i)


# In[184]:


df2 = pd.melt(df,id_vars=['Point_ID'], var_name='Image Date', value_name='NDVI')
for i in lst:
    new = i.replace(".1", "")
    df2= df2.replace(i, new)
df2["SAT"] = sat_name
df2.head()


# In[185]:


ha = pd.read_csv("harvest.csv")
har = pd.DataFrame(ha)
df3 = pd.merge(df2, har, on='Point_ID')
df3.to_csv(output_file)

