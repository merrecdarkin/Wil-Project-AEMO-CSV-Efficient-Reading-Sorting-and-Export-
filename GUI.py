import glob
import os
import os.path
import PySimpleGUI as sg
import pandas as pd
import App as app
from datetime import datetime

"""
The app GUI is divided into 2 main column
Left column is the file browser column with browser bar and list box for CSV files
Right column is user input field, preview section, and confirmation buttons
This block of code is the LEFT column of the GUI
"""
fileBrowserColumn = [ 
    [ # Folder browser bar
        sg.Text("CSV Folder"),
        sg.Input(size=(20,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [ # Display CSV file names from selected folder
        sg.Listbox(values=[], enable_events=True, size=(40,20), key="-FILE LIST-")
    ],
]

"""
This block of code is a subcolumn in the main RIGHT column of the GUI
Based on the GUI design, user input and confirmation buttons are placed in a single row as 2 side-by-side column
"""   
dataQueryColumnInput = [
    # Text field to be input by the users as query params
    [sg.Text("Enter DUID (separated by space):")],
    [sg.InputText(key = "-INPUT DUID-")],
    [sg.Text("Enter BIDTYPE (separated by space):")],
    [sg.InputText(key = "-INPUT BIDTYPE-")],
    [sg.Text("From SETTLEMENTDATE (dd/mm/yyyy)")],
    [sg.InputText(key = "-INPUT DATE START-")],
    [sg.Text("To SETTLEMENTDATE (dd/mm/yyyy)")],
    [sg.InputText(key = "-INPUT DATE END-")],
]

dataQueryColumnButton = [
    [sg.Button('Export', key = '-CONFIRM-')],
    [sg.Button('Preview', key = '-PREVIEW-')]
]

"""
The app GUI is divided into 2 main column
This block of code is the RIGHT column of the GUI
Right column contains user input field, preview section, and confirmation buttons
"""
dataQueryColumn = [   
    [sg.Column(dataQueryColumnInput),sg.Column(dataQueryColumnButton)],
    [sg.Text('Preview Data:')],
    [sg.Listbox(values = ['preview section placeholder'], enable_events=True, size = (60,10), key = "-PREVIEW LIST-")]
]

layout = [
    [sg.Column(fileBrowserColumn), sg.VSeperator(),sg.Column(dataQueryColumn)]
]

window = sg.Window("AEMO Data Manipulation Tool",layout) # Window creation. GUI follows "Persistent Window with updates" design pattern with a single main window

while True: # Event loop - read window events and inputs

    event, values = window.read()

    if event == "Exit" or event ==sg.WIN_CLOSED:
        break

    if event== "-FOLDER-": # Folder browser callback event
        """
        Workflow of the callback event, when the Browse button is click and a folder had been selected, do as follow:
        - Read the folder path
        - Retrieve all valid CSV file paths within the folder path using glob() pattern matching
        - Retrieve only the CSV file names from the CSV file paths
        - Update valid CSV file names to the side panel in GUI
        """
        selectedFolderPath= values["-FOLDER-"]
        validCSVFilePath = glob.glob(selectedFolderPath + "/PUBLIC_BIDMOVE_COMPLETE*.csv")
        validCSVFileName = [os.path.basename(f) for f in validCSVFilePath]
        window["-FILE LIST-"].update(validCSVFileName)

    if event== "-CONFIRM-": # Export button callback event

        #First, read the folder path and retrive all valid CSV file paths
        selectedFolderPath= values["-FOLDER-"]
        validCSVFilePath = glob.glob(selectedFolderPath + "/PUBLIC_BIDMOVE_COMPLETE*.csv")
        
        """
        After getting CSV file paths, the app now fetch the user input data from the input text fields:
        - DUIDset and BIDTYPEset are separated by space, .split() method is used to split each of them and add to the query list
        - DUIDset and BIDTYPEset str values are converted into UPPERCASE with .upper()
        - DATESTARTset and DATEENDset need to be init as an empty string, this is to make sure they can be passed to app.loadCSV() if the user left them blank
        - If any of DATE field is specified, convert them from str to datetime type with datetime.strptime()
        """
        DUIDset = [x.upper() for x in values['-INPUT DUID-'].split()]
        BIDTYPEset = [x.upper() for x in values['-INPUT BIDTYPE-'].split()]
        DATESTARTset = DATEENDset = ''
        if values['-INPUT DATE START-']:
            DATESTARTset = datetime.strptime(values['-INPUT DATE START-'],'%d/%m/%Y')  
        if values['-INPUT DATE END-']:
            DATEENDset = datetime.strptime(values['-INPUT DATE END-'],'%d/%m/%Y')
        
        """
        After fetching input data, pass them along with the CSV file paths to loadCSV() function
        The loadCSV() function returns a tuple of 2 queried/processed dataframes (price,quantity) based on user input data
        Use to_excel() to write the output dataframe to a xlsx file
        Use ExcelWriter to construct the structure of output xlsx:
        - output[0] returns priceTable dataframe, written to 'Price' sheet
        - output[1] returns quantityTable dataframe, written to 'Quantity' sheet
        """
        output = app.loadCSV(validCSVFilePath,DUIDset,BIDTYPEset,DATESTARTset,DATEENDset)
        with pd.ExcelWriter('output.xlsx') as writer:
            output[0].to_excel(writer, sheet_name='Price')
            output[1].to_excel(writer, sheet_name='Quantity')
        os.startfile('output.xlsx') # Autostart, file handling depends on user OS settings, will use MS Excel if installed and set as default xlsx handler

window.close()