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
                    sg.FolderBrowse(),
                ],
                [   # File list panel: display CSV file names
                    sg.Listbox(values=[], enable_events=True, size=(40,20), key='-FILE LIST-')
                ],
                [
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
                            [sg.Text("Enter DUID (separated by space):")],
                            [sg.InputText(key = "-INPUT DUID-")],
                            [sg.Text("Enter BIDTYPE (separated by space):")],
                            [sg.InputText(key = "-INPUT BIDTYPE-")],
                            [sg.Text("From SETTLEMENTDATE (dd/mm/yyyy)")],
                            [sg.InputText(key = "-INPUT DATE START-")],
                            [sg.Text("To SETTLEMENTDATE (dd/mm/yyyy)")],
                            [sg.InputText(key = "-INPUT DATE END-")]
                        ]
                    ),
                    sg.Column(
                        [   # Confirmation buttons
                            [sg.Button('Export', key = '-CONFIRM-')],
                            [sg.Button('Preview', key = '-PREVIEW-')]
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

window = sg.Window('AEMO Data Manipulation Tool', layout)

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
        # Update total file number under file list panel
        window['-FILE TOTAL-'].update(str(len(CSVFileName)))

        print('-------------------------------------')
        print('CSV dataset updated!')

    ### EXPORT BUTTON CALLBACK EVENT ###
    if event== "-CONFIRM-":
        start=dt.datetime.now()
        print('Operation started...')

        # Get absolute CSV file path by concatenating the root folder path with the relative csv file path
        absoluteCSVFilePath = [currentFolderPath + '/' + f for f in relativeCSVFilePath]

        # Get DUID and BIDTYPE filter input from user, split by space and convert to UPPERCASE to match source data format
        DUIDset = [x.upper() for x in values['-INPUT DUID-'].split()]
        BIDTYPEset = [x.upper() for x in values['-INPUT BIDTYPE-'].split()]

        DATESTARTset = DATEENDset = ''
        if values['-INPUT DATE START-']:
            DATESTARTset = dt.datetime.strptime(values['-INPUT DATE START-'],'%d/%m/%Y')  
        if values['-INPUT DATE END-']:
            DATEENDset = dt.datetime.strptime(values['-INPUT DATE END-'],'%d/%m/%Y')

        # Read CSV and query based on user filters
        # App.loadCSV() returns a tuple of (price,quantity) dataframes
        output = app.loadCSV(absoluteCSVFilePath, DUIDset, BIDTYPEset, DATESTARTset, DATEENDset)
        
        # Build Excel export structure
        # Price and Quantity written to dedicated sheet  
        with pd.ExcelWriter('output.xlsx') as writer:
            output[0].to_excel(writer, sheet_name='Price')
            output[1].to_excel(writer, sheet_name='Quantity')
        
        # Autostart after export, default file type (.xlsx) handler is set by the operating system
        os.startfile('output.xlsx') 
        
        print('Operation complete! Total process runtime:', dt.datetime.now()-start)
        print('-------------------------------------')

window.close()