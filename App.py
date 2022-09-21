import datetime as dt
import pandas as pd


def loadCSV(absoluteCSVFilePath,DUIDset,BIDTYPEset):

    # List for later multi CSV merge
    priceTables = []
    quantityTables = []

    for f in absoluteCSVFilePath:
        start = dt.datetime.now()
        
        # Read price table (BIDDAYOFFER_D)
        priceTable = pd.read_csv(f, skiprows=1, on_bad_lines='skip', engine='c')
        # Read quantity table (BIDPEROFFER_D), drop duplicate data
        quantityTable = pd.read_csv(f, skiprows=len(priceTable)+1, on_bad_lines='skip', engine='c').drop_duplicates(subset=['DUID','BIDTYPE','LASTCHANGED'])
        # Add each dataframe to merger-list accordingly
        priceTables.append(priceTable)
        quantityTables.append(quantityTable)

        print('Loaded', f, 'in:', dt.datetime.now()-start)

    print('All CSV loaded!')
    print('Merging data...')
    start = dt.datetime.now()

    # Merge all CSV data into one dataframe
    priceTable = pd.concat(priceTables, ignore_index=True)
    quantityTable = pd.concat(quantityTables, ignore_index=True)
    
    print('Dataframes successfully merged in:', dt.datetime.now()-start)

    # Data query construction
    print('Querying database...')
    start = dt.datetime.now()

    # If any of the input field is left blank, then a str value of 'True' will be assigned, to be used in df query statement
    # It will create an effect to ignore that empty query field, and return all the data from that column without filtering
    DUIDquery = BIDTYPEquery = 'True'

    # If the input filter is not blank, construct the query string for each of the input filter
    if DUIDset:
        DUIDquery = 'DUID in @DUIDset'
    if BIDTYPEset:
        BIDTYPEquery = 'BIDTYPE in @BIDTYPEset'

    # Concatenate all filter into one query statement
    finalQuery = DUIDquery + ' and ' + BIDTYPEquery
    # Query the merged dataframes, drop unnecessary columns, sort by DUID then SETTLEMENTDATE
    # If filter parameters left as empty input, only drop and sort, no query
    if len(DUIDset) == 0 and len(BIDTYPEset) == 0:
        priceTable = priceTable.drop(columns=['I','BID','BIDDAYOFFER_D','2','VERSIONNO']).sort_values(by=['DUID','SETTLEMENTDATE'])
        quantityTable = quantityTable.drop(columns=['I','BID','BIDPEROFFER_D','2','PERIODID','INTERVAL_DATETIME']).sort_values(by=['DUID','SETTLEMENTDATE'])
    else:
        priceTable = priceTable.query(finalQuery).drop(columns=['I','BID','BIDDAYOFFER_D','2','VERSIONNO']).sort_values(by=['DUID','SETTLEMENTDATE'])
        quantityTable = quantityTable.query(finalQuery).drop(columns=['I','BID','BIDPEROFFER_D','2','PERIODID','INTERVAL_DATETIME']).sort_values(by=['DUID','SETTLEMENTDATE'])

    print('Data query successfully executed in:', dt.datetime.now()-start)

    return (priceTable,quantityTable)

#################################################################
def filterCSVDate(relativeCSVFilePath,dateStart,dateEnd):
    
    # Convert str values from date filter to int for comparison
    # If empty date arg is passed, set default min/max for start and end date
    if dateStart:
        dateStart = int(dateStart)
    else: dateStart = 00000000
    if dateEnd:
        dateEnd = int(dateEnd)
    else: dateEnd = 99999999

    validCSVFilePath = [] # List for valid CSV path in between date range

    for f in relativeCSVFilePath:
        # Get the date string part from each CSV file name
        dateStringInCSV = f[f.find('_COMPLETE_')+10:f.find('_COMPLETE_')+18]
        # Convert date string to int and compare in date range, add to output list if valid
        if dateStart <= int(dateStringInCSV) <= dateEnd:
            validCSVFilePath.append(f)
    
    return(validCSVFilePath)

#################################################################
def invalidDateFormat(dateString):

    # If empty date string is passed, return as valid format (False)
    if not dateString:
        return False
    # If non-empty date string is passed, check for format
    else:
        try:
            # If strptime can convert the string, return as valid format (False)
            dt.datetime.strptime(dateString, '%Y/%m/%d')
            return False
        except:
            # If exception raised, return as invalid format (True)
            return True

#################################################################
def countRowFeature(sheet,DUID):
    return(len(sheet[sheet['DUID'] == DUID])) #count row featured this DUID

#################################################################
def findTypeFeature(sheet,DUID):
    typeColection=[]
    dfSheet= (pd.DataFrame(sheet))
    queryCommand='DUID =='+'"'+ DUID+'"'
    dfSheet=dfSheet.query(queryCommand)
    dfSheet.drop_duplicates(subset=['BIDTYPE'], inplace=True) #set aside bitype in this DUID
    typeColection=dfSheet['BIDTYPE'].to_numpy()
    return(typeColection)