import numpy as np
import pandas as pd

def loadCSV(nameOfCSV,DUIDsets,folPath):
    print(folPath)
    PathAndNameFile=folPath+"/"+nameOfCSV
    df = pd.read_csv(PathAndNameFile, skiprows=1, skipfooter=1, on_bad_lines='skip')#This will fetch the BIDDAYOFFER_D

    for targetDUID in DUIDsets:
        print(df.loc[df['DUID'] == targetDUID])     
    df2 = pd.read_csv(PathAndNameFile, skiprows=len(df. index)+2, skipfooter=1, on_bad_lines='skip') #This will fetch the BIDPEROFFER_D 
    for targetDUID in DUIDsets:
        print(df2.loc[df2['DUID'] == targetDUID])     
