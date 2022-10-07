import glob as glob
import os as os
import PySimpleGUI as sg
import pandas as pd
import App as app
import datetime as dt

### GLOBAL VARIABLES ###
currentFolderPath = ''
currentOutputPath = ''
relativeCSVFilePath = []

layout = [
    [   # LEFT COLUMN: Folder browser bar, CSV file list
        sg.Column( 
            [ 
                [   # Folder browser bar
                    sg.Text('CSV Folder'),
                    sg.Input(size=(20,1), enable_events=True, key='-FOLDER-'),
                    sg.FolderBrowse(button_text='BROWSE'),
                ],
                [   # File list panel: display all CSV file names
                    sg.Listbox(values=[], enable_events=True, size=(40,20), key='-FILE LIST-')
                ],
                [   # Total file count under file list
                    sg.Text('Total files:'),
                    sg.Text('0', enable_events=True, key='-FILE TOTAL-')
                ],
                [   # Folder browser bar for out put
                    sg.Text('Output Folder'),
                    sg.Input(size=(20,1), enable_events=True, key='-OUTPUT PATH-'),
                    sg.FolderBrowse(button_text='BROWSE'),
                ]
            ]
        ),

        sg.VSeperator(), # Vertical line separator between 2 columns

        # MIDDLE COLUMN: Data input filter, Preview console
        sg.Column(
            [   # MIDDLE COLUMN UPPER: Filter text field input
                [
                    sg.Column( 
                        [   # Text field input by user as data filter
                            [sg.Text('START DATE (yyyy/mm/dd) e.g. 2022/01/01 (inclusive)')],
                            [sg.InputText(key='-INPUT DATE START-'), sg.CalendarButton('⮟', no_titlebar=False, title='Set Start Date', target='-INPUT DATE START-', format='%Y/%m/%d', button_color=('black','white'))],
                            [sg.Text('END DATE (yyyy/mm/dd) e.g. 2022/01/31 (inclusive)')],
                            [sg.InputText(key='-INPUT DATE END-'), sg.CalendarButton('⮟', no_titlebar=False, title='Set End Date', target='-INPUT DATE END-', format='%Y/%m/%d', button_color=('black','white'))],
                            [sg.Text('DUID(s) (separated by space) e.g. BLUFF1 YWPS4 ')],
                            [sg.InputText(key = '-INPUT DUID-')],
                            [sg.Text('Specify export file name (optional) ')],
                            [sg.InputText(key = '-OUTPUT NAME-')],
                            [sg.Checkbox('Autostart Excel file after export?',key="-AUTO OPEN-")]
                        ]
                    ),
                ], 
                # MIDDLE COLUMN LOWER: Preview section
                [sg.Text('Preview Data:')],
                [sg.Listbox(values=[], enable_events=True, size=(50,10), key='-PREVIEW LIST-')]
            ]
        ),

        # RIGHT COLUMN: Bidtype selection listbox, Confirmation buttons
        sg.Column(
            [
                [sg.Text('Select BIDTYPE(s):')],
                [sg.Listbox(['ENERGY','LOWER5MIN','LOWER60SEC','LOWER6SEC','LOWERREG','RAISE5MIN','RAISE60SEC','RAISE6SEC','RAISEREG'], enable_events=True, size=(20,9), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key="-INPUT BIDTYPE-")],
                [sg.VPush()],
                [sg.Button(' SET DATE ', size=(10,4), key = '-SET DATE-')],
                [sg.VPush()],
                [sg.Button('   EXPORT  ', size=(10,4), key = '-EXPORT-')]
            ], element_justification='c'
        )

    ]
]

window = sg.Window('AEMO Data Extraction Tool', layout)

while True: # GUI event loop

    event, values = window.read()

    if event == "Exit" or event ==sg.WIN_CLOSED:
        break

    ### FOLDER BROWSER CALLBACK EVENT ###
    if event== "-FOLDER-":
        
        # Read the folder path
        currentFolderPath= values["-FOLDER-"]
        
        # Get all valid CSV file paths relatively to the current dir (recursive match in all sub-dir)
        rawRelativeCSVFilePath = glob.glob('**/PUBLIC_BIDMOVE_COMPLETE*.csv', root_dir=currentFolderPath, recursive=True)
        # Remove duplicate csv file name in subdir
        [relativeCSVFilePath.append(f) for f in rawRelativeCSVFilePath if os.path.basename(f) not in relativeCSVFilePath]
        
        # Slice CSV file names from full file paths
        CSVFileName = [os.path.basename(f) for f in relativeCSVFilePath]
        
        # Update CSV file names to file list panel
        window["-FILE LIST-"].update(CSVFileName)
        
        # Update total file count under file list panel
        window['-FILE TOTAL-'].update(str(len(CSVFileName)))
        
        print('-------------------------------------')
        print('Root folder updated!')

    ### OUTPUT FOLDER BROWSER CALLBACK EVENT ###
    if event== "-OUTPUT PATH-":
        currentOutputPath= values["-OUTPUT PATH-"]+'/'

    ### SET DATE CALLBACK EVENT ###
    if event== "-SET DATE-":
        
        # Flag to check for any present errors
        errSetDate = False

        # If no root dir selected, stall and print err message
        if not currentFolderPath and not errSetDate:
            errSetDate = True
            sg.Popup('Root folder not found. Please click BROWSE to try again!', title='Error!')

        # Execute callback when no errors found
        if not errSetDate:    
            # Reset/refetch CSV file path (if root directory or date range changed by user)
            rawRelativeCSVFilePath = glob.glob('**/PUBLIC_BIDMOVE_COMPLETE*.csv', root_dir=currentFolderPath, recursive=True)
            # Remove duplicate csv file name in subdir
            [relativeCSVFilePath.append(f) for f in rawRelativeCSVFilePath if os.path.basename(f) not in relativeCSVFilePath]
            # Check for invalid date format
            if app.invalidDateFormat(values['-INPUT DATE START-']) or app.invalidDateFormat(values['-INPUT DATE END-']):
                sg.Popup('Wrong date format detected. Please try "YYYY/MM/DD" again!', title='Error!')

            else: #proceed with cb event

                # Get Date range values
                dateStart = values['-INPUT DATE START-'].replace('/', '')
                dateEnd = values['-INPUT DATE END-'].replace('/', '')

                # Filter valid CSV path in date range
                relativeCSVFilePath = app.filterCSVDate(relativeCSVFilePath, dateStart, dateEnd)
                
                # Update CSV file names and total file count
                CSVFileName = [os.path.basename(f) for f in relativeCSVFilePath]
                window["-FILE LIST-"].update(CSVFileName)
                window['-FILE TOTAL-'].update(str(len(CSVFileName)))
                
                print('CSV file list updated!')

    ### EXPORT BUTTON CALLBACK EVENT ###
    if event== "-EXPORT-":
        
        # Flag to check for any present errors
        errExport = False

        # If no root dir selected, stall and print err message
        if not currentFolderPath and not errExport:
            errExport = True
            sg.Popup('Root folder not found. Please click BROWSE to try again!', title='Error!')
        # If empty CSV file list found, stall and print err message
        if not relativeCSVFilePath and not errExport:
            errExport = True
            sg.Popup('No CSV file detected. Please change Date range or select different root Folder to try again!', title='Error!')

        # Execute callback when no errors found
        if not errExport:
            print('Operation started...')

            # Get absolute CSV file path by concatenating the root folder path with the relative csv file path
            absoluteCSVFilePath = [currentFolderPath + '/' + f for f in relativeCSVFilePath]
            
            # Get DUID and BIDTYPE filter input from user, split by space and convert to UPPERCASE to match source data format
            DUIDset = [x.upper() for x in values['-INPUT DUID-'].split()]
            BIDTYPEset = values['-INPUT BIDTYPE-']
            
            # Read CSV and query based on user filters
            # App.loadCSV() returns a tuple of (price,quantity) dataframes
            output = app.loadCSV(absoluteCSVFilePath, DUIDset, BIDTYPEset)

            # Cancel if empty output detected
            if len(output[0]) == 0 and len(output[1]) == 0:
                print('Operation cancelled!')
                print('-------------------------------------')
                sg.Popup('Output table appeared to be empty. Please check DUID and BIDTYPE input and try again!', title='Error!')
            else: #process continued

                # Preview Function
                previewData = []
                previewData.append('Query processed on '+str(len(absoluteCSVFilePath))+' CSV file(s).')
                previewData.append('Price table contained '+str(len(output[0]))+' row(s).')
                previewData.append('Quantity table contained '+str(len(output[1]))+' row(s)')
                if len(DUIDset)==0:
                    previewData+=["All DUID will be exported."]
                else:
                    for DUID in DUIDset:
                        previewData += ['',DUID,'-- appeared in Price table for '+app.rowCount(output[0],DUID)+' row(s).','-- appeared in Quantity table for '+app.rowCount(output[1],DUID)+' row(s).','-- featured BIDTYPE: ']
                        previewData += ['                           '+BIDTYPE for BIDTYPE in app.getUniqueBIDTYPE(output[1],DUID)]
                window["-PREVIEW LIST-"].update(previewData)
        
                # Confirmation popup check
                CONFRIMATION=sg.popup_yes_no('Please preview output data before proceed. Click Yes to Export and No to Cancel.', title='Confirmation!')

                if CONFRIMATION == 'Yes':
                    # Build Excel export structure
                    # Price and Quantity written to dedicated sheet
                    print('Writing data to Excel...')
                    start1 = dt.datetime.now()
                    # Check and compile full output path and file names
                    outputName = values['-OUTPUT NAME-'].replace('/', '')
                    if not outputName:
                        outputName = 'output'
                    outputPath = currentOutputPath + outputName +'.xlsx'
                    # Export to Excel format
                    print(outputPath)
                    with pd.ExcelWriter(outputPath) as writer:
                        output[0].to_excel(writer, sheet_name='Price', index=False)
                        output[1].to_excel(writer, sheet_name='Quantity', index=False)
                    print('Data successfully exported in:', dt.datetime.now()-start1)
                    # Autostart file if checked by user
                    if values['-AUTO OPEN-']:
                        os.startfile(outputPath) 
                    print('Operation complete!')
                    print('-------------------------------------')
                else:
                    print('Operation cancelled!')
                    print('-------------------------------------')

window.close()