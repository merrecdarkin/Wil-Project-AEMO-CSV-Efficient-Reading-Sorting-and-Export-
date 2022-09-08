import glob as glob
import os as os
import PySimpleGUI as sg
import pandas as pd
import App as app
import datetime as dt

layout = [
    [   # LEFT MAIN COLUMN: Folder browser bar, CSV file list
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
                ]
            ]
        ),

        sg.VSeperator(), # Vertical line separator between 2 columns

        # RIGHT MAIN COLUMN: Data input filter, Preview console
        sg.Column(
            [   # RIGHT MAIN COLUMN UPPER SECTION: Filter input, Confirmation buttons
                [
                    sg.Column( 
                        [   # Text field input by user as data filter
                            [sg.Text('START DATE (yyyy/mm/dd) e.g. 2022/01/01 (inclusive)')],
                            [sg.InputText(key = '-INPUT DATE START-')],
                            [sg.Text('END DATE (yyyy/mm/dd) e.g. 2022/01/31 (inclusive)')],
                            [sg.InputText(key = '-INPUT DATE END-')],
                            [sg.Text('DUID(s) (separated by space) e.g. BLUFF1 YWPS4 ')],
                            [sg.InputText(key = '-INPUT DUID-')],
                            [sg.Text('BIDTYPE(s) (separated by space) e.g. ENERGY ')],
                            [sg.InputText(key = '-INPUT BIDTYPE-')]
                        ]
                    ),
                    sg.Column(
                        [   # Confirmation buttons
                            [sg.Button(' SET DATE ', key = '-SET DATE-')],
                            [sg.Button('   EXPORT  ', key = '-EXPORT-')]
                            
                        ]
                    )
                ], 
                # RIGHT MAIN COLUMN LOWER SECTION: Preview console
                [sg.Text('Preview Data:')],
                [sg.Listbox(values=['preview section placeholder'], enable_events=True, size=(60,10), key='-PREVIEW LIST-')]
            ]
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
        relativeCSVFilePath = glob.glob('**/PUBLIC_BIDMOVE_COMPLETE*.csv', root_dir=currentFolderPath, recursive=True)
        # Slice CSV file names from full file paths
        CSVFileName = [os.path.basename(f) for f in relativeCSVFilePath]
        # Update CSV file names to file list panel
        window["-FILE LIST-"].update(CSVFileName)
        # Update total file count under file list panel
        window['-FILE TOTAL-'].update(str(len(CSVFileName)))

        print('-------------------------------------')
        print('Root folder updated!')

    if event== "-SET DATE-":
        # Reset/refetch CSV file path (if root directory or date range changed by user)
        relativeCSVFilePath = glob.glob('**/PUBLIC_BIDMOVE_COMPLETE*.csv', root_dir=currentFolderPath, recursive=True)
        # Get date range values
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
        start=dt.datetime.now()
        print('Operation started...')

        # Get absolute CSV file path by concatenating the root folder path with the relative csv file path
        absoluteCSVFilePath = [currentFolderPath + '/' + f for f in relativeCSVFilePath]

        # Get DUID and BIDTYPE filter input from user, split by space and convert to UPPERCASE to match source data format
        DUIDset = [x.upper() for x in values['-INPUT DUID-'].split()]
        BIDTYPEset = [x.upper() for x in values['-INPUT BIDTYPE-'].split()]

        # Read CSV and query based on user filters
        # App.loadCSV() returns a tuple of (price,quantity) dataframes
        output = app.loadCSV(absoluteCSVFilePath, DUIDset, BIDTYPEset)
        
        # Build Excel export structure
        # Price and Quantity written to dedicated sheet  
        with pd.ExcelWriter('output.xlsx') as writer:
            output[0].to_excel(writer, sheet_name='Price', index=False)
            output[1].to_excel(writer, sheet_name='Quantity', index=False)
        
        # Autostart after export, default file type (.xlsx) handler is set by the operating system
        os.startfile('output.xlsx') 
        
        print('Operation complete! Total process runtime:', dt.datetime.now()-start)
        print('-------------------------------------')

window.close()