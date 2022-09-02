import os
import os.path
import pandas as pd


def loadCSV(validCSVFilePath,DUIDset,BIDTYPEset,DATESTARTset,DATEENDset):
    df = pd.read_csv(validCSVFilePath, skiprows=1, skipfooter=1, on_bad_lines='skip', parse_dates=['SETTLEMENTDATE'],engine='python')
    # parse_dates is used to set SETTLEMENTDATE column data type from str to date, so that it can be used to query the DATESTART and DATEEND (both are datetime obj type)
    
    DUIDquery = BIDTYPEquery = DATESTARTquery = DATEENDquery = 'True'
    # If any of the input field is left blank, then a str value of 'True' will be assigned. This is used in the query logic, an empty filter will return ALL data from that filter

    # If the input field is not blank, construct the query string for each of the input field
    if DUIDset:
        DUIDquery = 'DUID in @DUIDset'
        """
        Query explanation:
        DUID is the name of the header column pandas get from pd.read_csv(), in this case we have DUID, BIDTYPE and SETTLEMENTDATE. It is equivalent of calling df['DUID'].
        pandas.query() can interact with variables that are not part of the dataframe, by adding @ before the name.
        Essentially this query mean 'return any rows that have the DUID value in the DUIDset list that we fetch from user input.
        """
    if BIDTYPEset:
        BIDTYPEquery = 'BIDTYPE in @BIDTYPEset'
    if DATESTARTset:
        DATESTARTquery = 'SETTLEMENTDATE >= @DATESTARTset'
    if DATEENDset:
        DATEENDquery = 'SETTLEMENTDATE <= @DATEENDset'

    finalQuery = DUIDquery + ' and ' + BIDTYPEquery + ' and ' + DATESTARTquery + ' and ' + DATEENDquery
    """
    The final query is constructed by concatenating all 4 query conditions
    As previously mentioned, if the user left any field empty, the query string of that field will become 'True'
    It will create an effect when passing in the query to ignore that query field. In other words it will return all the data from that column/field without any filtering
    E.g. If the users enter DUID, DATESTART but left BIDTYPE and DATEEND empty the query will become
    'DUID in @DUIDset and True and SETTLEMENTDATE >= @DATESTARTset and True'
    The output will return ALL rows that matche the DUID list, all BIDTYPE is allowed, SETTLEMENTDATE will range from DATESTART to the rest of the table as no end date is specified
    This implementation is to avoid creating errors when user pass an empty field as input
    """

    return df.query(finalQuery)
     
    """df2 = pd.read_csv(validCSVFilePath, skiprows=len(df. index)+2, skipfooter=1, on_bad_lines='skip', engine='python') #This will fetch the BIDPEROFFER_D 
    for targetDUID in DUIDsets:
        print(df2.loc[df2['DUID'] == targetDUID])"""     

def isValidCSVFile(f, selectedFolderPath):
    """
    This function check for valid CSV file names within the folder selected by users
    selectedFolderPath should be fetched in GUI folder browser callback
    """
    return os.path.isfile(os.path.join(selectedFolderPath, f)) and f.lower().endswith((".csv")) and ("PUBLIC_BIDMOVE_COMPLETE" in f)
    