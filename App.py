import datetime as dt
import pandas as pd


def loadCSV(absoluteCSVFilePath,DUIDset,BIDTYPEset,DATESTARTset,DATEENDset):

    # List for later multi CSV merge
    priceTables = []
    quantityTables = []

    for f in absoluteCSVFilePath:
        start = dt.datetime.now()
        
        # Read price table (BIDDAYOFFER_D)
        priceTable = pd.read_csv(f, skiprows=1, on_bad_lines='skip', parse_dates=['SETTLEMENTDATE'], engine='c')
        # Read quantity table (BIDPEROFFER_D)
        quantityTable = pd.read_csv(f, skiprows=len(priceTable)+1, on_bad_lines='skip', parse_dates=['SETTLEMENTDATE'], engine='c')
        # Add each dataframe to merger-list accordingly
        priceTables.append(priceTable)
        quantityTables.append(quantityTable)

        print('Loaded', f, 'in:', dt.datetime.now()-start)

    print('All CSV loaded! Merging data...')
    start = dt.datetime.now()

    # Merge all CSV data into one dataframe, purge replications in quantity table
    priceTable = pd.concat(priceTables,ignore_index=True)
    quantityTable = pd.concat(quantityTables,ignore_index=True).drop_duplicates(subset=['DUID','BIDTYPE','LASTCHANGED'])
    
    print('Dataframes successfully merged in:', dt.datetime.now()-start)

    # Data query construction
    start = dt.datetime.now()

    # If any of the input field is left blank, then a str value of 'True' will be assigned, to be used in df query statement
    # It will create an effect to ignore that empty query field, and return all the data from that column without filtering
    DUIDquery = BIDTYPEquery = DATESTARTquery = DATEENDquery = 'True'

    # If the input filter is not blank, construct the query string for each of the input filter
    if DUIDset:
        DUIDquery = 'DUID in @DUIDset'
    if BIDTYPEset:
        BIDTYPEquery = 'BIDTYPE in @BIDTYPEset'
    if DATESTARTset:
        DATESTARTquery = 'SETTLEMENTDATE >= @DATESTARTset'
    if DATEENDset:
        DATEENDquery = 'SETTLEMENTDATE <= @DATEENDset'

    # Concatenate all filter into one query statement
    finalQuery = DUIDquery + ' and ' + BIDTYPEquery + ' and ' + DATESTARTquery + ' and ' + DATEENDquery

    # Query the merged dataframes, sort by DUID then date
    priceTable = priceTable.query(finalQuery).sort_values(by=['DUID','SETTLEMENTDATE'])
    quantityTable = quantityTable.query(finalQuery).sort_values(by=['DUID','SETTLEMENTDATE'])

    print('Data query executed in:', dt.datetime.now()-start)
    return (priceTable,quantityTable)