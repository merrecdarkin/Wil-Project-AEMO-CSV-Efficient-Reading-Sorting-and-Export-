import pandas as pd


def loadCSV(validCSVFilePath,DUIDset,BIDTYPEset,DATESTARTset,DATEENDset):
    """
    Process to read multiple CSV files from validCSVFilePath list and merge into one final dataframe:
    - Init an empty list 'dfs' to hold each dataframe loaded from individual CSV file
    - Loop through each CSV file and append each dataframe to the dfs list
    - Merge all dataframe in dfs using pd.concat() and assign to one final dataframe 'df'
    """
    dfs = []
    for f in validCSVFilePath:
        dfs.append(pd.read_csv(f, skiprows=1, skipfooter=1, on_bad_lines='skip', parse_dates=['SETTLEMENTDATE'],engine='python'))
        # parse_dates is used to set SETTLEMENTDATE column data type from str to date, so that it can be used to query the DATESTART and DATEEND (both are datetime obj type)
    df = pd.concat(dfs, ignore_index=True)

    # Data query construction
    DUIDquery = BIDTYPEquery = DATESTARTquery = DATEENDquery = 'True'
    # If any of the input field is left blank, then a str value of 'True' will be assigned. This is used in the query logic, an empty filter will return ALL data from that filter
    # If the input field is not blank, construct the query string for each of the input field
    if DUIDset:
        DUIDquery = 'DUID in @DUIDset'
        """
        Query explanation:
        DUID is the name of the header column pandas get from pd.read_csv(), in this case we have DUID, BIDTYPE and SETTLEMENTDATE. It is equivalent to calling df['DUID'].
        pandas.query() can interact with variables that are not part of the dataframe, by adding @ before the name.
        Essentially this query mean 'return any rows that have the DUID value in the DUIDset list, that was fetched from user input.
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
    It will create an effect to ignore that empty query field. In other words it will return all the data from that column/field without filtering
    E.g. If the users enter DUID, DATESTART but left BIDTYPE and DATEEND empty, the query will become:
    df.query('DUID in @DUIDset and True and SETTLEMENTDATE >= @DATESTARTset and True')
    The output will return rows that match the DUID list, all BIDTYPE is allowed (no filter), SETTLEMENTDATE will range from DATESTART to the rest of the table as no DATEEND cut-off is specified
    This implementation is to avoid errors when user pass an empty field as input
    """

    return df.query(finalQuery)
     
    """df2 = pd.read_csv(validCSVFilePath, skiprows=len(df. index)+2, skipfooter=1, on_bad_lines='skip', engine='python') #This will fetch the BIDPEROFFER_D 
    for targetDUID in DUIDsets:
        print(df2.loc[df2['DUID'] == targetDUID])"""     