import os
import os.path
import pandas as pd


def loadCSV(validCSVFilePath,DUIDset,BIDTYPEset,DATESTARTset,DATEENDset):
    df = pd.read_csv(validCSVFilePath, skiprows=1, skipfooter=1, on_bad_lines='skip', parse_dates=['SETTLEMENTDATE'],engine='python')#This will fetch the BIDDAYOFFER_D
    DUIDquery = BIDTYPEquery = DATESTARTquery = DATEENDquery = 'True'
    if DUIDset:
        DUIDquery = 'DUID in @DUIDset'
    if BIDTYPEset:
        BIDTYPEquery = 'BIDTYPE in @BIDTYPEset'
    if DATESTARTset:
        DATESTARTquery = 'SETTLEMENTDATE >= @DATESTARTset'
    if DATEENDset:
        DATEENDquery = 'SETTLEMENTDATE <= @DATEENDset'
    finalQuery = DUIDquery + ' and ' + BIDTYPEquery + ' and ' + DATESTARTquery + ' and ' + DATEENDquery

    return df.query(finalQuery)
     
    #df2 = pd.read_csv(validCSVFilePath, skiprows=len(df. index)+2, skipfooter=1, on_bad_lines='skip', engine='python') #This will fetch the BIDPEROFFER_D 
    #for targetDUID in DUIDsets:
    #    print(df2.loc[df2['DUID'] == targetDUID])     

def isValidCSVFile(f, selectedFolderPath):
    """
    This function check for valid CSV file names within the folder selected by users
    selectedFolderPath should be fetched in GUI folder browser callback
    """
    return os.path.isfile(os.path.join(selectedFolderPath, f)) and f.lower().endswith((".csv")) and ("PUBLIC_BIDMOVE_COMPLETE" in f)
    