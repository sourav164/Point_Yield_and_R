import pandas as pd, os

folder = r"E:\Current Work Folder\Field Trip data\Sorted\plot"

#rewrite the data in desired format
for root, dirs, files in os.walk(folder):
    for jfile in files:
        if jfile.endswith("s.xls"):
            file = os.path.join(folder, jfile)
            print (file)
            i,j = os.path.split(file)
            csv_location = os.path.join(folder, j.replace(".xls", ".csv"))
            
            #import all the sheets into dataframe
            Sentinal = pd.read_excel(file, sheet_name="Sentp", header=0)
            Intel = pd.read_excel(file,sheet_name="Intelp",header=0)
            RE = pd.read_excel(file,sheet_name="REp",header=0)
            PSC = pd.read_excel(file,sheet_name="PSCp",header=0)
            
            #concetanate all the dataframes
            new = pd.concat([Intel.iloc[:, :],
                 PSC.iloc[:, 1:], 
                 Sentinal.iloc[:, 1:], 
                 RE.iloc[:, 1:]], axis=1)
            
            #save the file in the same name with csv extension
            new.to_csv(csv_location)
            del new
