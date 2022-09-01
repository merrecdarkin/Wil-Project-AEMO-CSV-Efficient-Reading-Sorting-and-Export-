import os
import os.path

import numpy as np
import pandas as pd

def loadCSV(validCSVFilePath,DUIDsets):
    df = pd.read_csv(validCSVFilePath, skiprows=1, skipfooter=1, on_bad_lines='skip', engine='python')#This will fetch the BIDDAYOFFER_D
    for targetDUID in DUIDsets:
        print(df.loc[df['DUID'] == targetDUID])     
    df2 = pd.read_csv(validCSVFilePath, skiprows=len(df. index)+2, skipfooter=1, on_bad_lines='skip', engine='python') #This will fetch the BIDPEROFFER_D 
    for targetDUID in DUIDsets:
        print(df2.loc[df2['DUID'] == targetDUID])     

def isValidCSVFile(f, selectedFolderPath):
    """
    This function check for valid CSV file names within the folder selected by users
    selectedFolderPath should be fetched in GUI folder browser callback
    """
    return os.path.isfile(os.path.join(selectedFolderPath, f)) and f.lower().endswith((".csv")) and ("PUBLIC_BIDMOVE_COMPLETE" in f)