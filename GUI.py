import os
import os.path
import PySimpleGUI as sg

import App as app

fileBrowserColumn = [ 
    
    # The app GUI is divided into 2 main column
    # Left column is the file browser column with browser bar and list box for CSV files
    # Right column is user input field, preview section, and confirmation buttons
    # This block of code is the LEFT column of the GUI
    
    [ # Folder browser bar
        sg.Text("CSV Folder"),
        sg.Input(size=(20,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [ # Display CSV file names from selected folder
        sg.Listbox(
            values=[], enable_events=True, size=(40,20),
            key="-FILE LIST-"
        )
    ],
]

dataQueryColumnInput = [
    
    # This block of code is a subcolumn in the main RIGHT column of the GUI
    # Based on the GUI design, user input and confirmation buttons are placed in a single row
    # as 2 side-by-side column
    
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

dataQueryColumn = [
    
    # The app GUI is divided into 2 main column
    # Left column is the file browser column with browser bar and list box for CSV files
    # Right column is user input field, preview section, and confirmation buttons
    # This block of code is the RIGHT column of the GUI
    
    [sg.Column(dataQueryColumnInput),sg.Column(dataQueryColumnButton)],
    [sg.Text('Preview Data:')],
    [sg.Listbox(values = ['preview section placeholder'], size = (60,10))]
]

layout = [
    [sg.Column(fileBrowserColumn), sg.VSeperator(),sg.Column(dataQueryColumn)]
]

window = sg.Window("AEMO Data Manipulation Tool",layout) # Window creation
# GUI follows "Persistent Window with updates" design pattern with a single main window

while True: # Event loop - read window events and inputs

    event, values = window.read()

    if event == "Exit" or event ==sg.WIN_CLOSED:
        break

    if event== "-FOLDER-": # Folder browser callback event
        selectedFolderPath= values["-FOLDER-"]
        fileInSelectedFolder = os.listdir(selectedFolderPath)
        validCSVFile = [f for f in fileInSelectedFolder if app.isValidCSVFile(f,selectedFolderPath)]
        window["-FILE LIST-"].update(validCSVFile)

    if event== "-CONFIRM-": # Export button callback event
        selectedFolderPath= values["-FOLDER-"]
        fileInSelectedFolder = os.listdir(selectedFolderPath)
        validCSVFile = [f for f in fileInSelectedFolder if app.isValidCSVFile(f,selectedFolderPath)]
        validCSVFilePath = [os.path.join(selectedFolderPath, f) for f in validCSVFile]

        for f in validCSVFilePath:
            if values["-INPUT DUID-"]: 
                DUIDsets= values["-INPUT DUID-"].split() #This will fetch Value from inputs, require further expansion
                app.loadCSV(f,DUIDsets)

window.close()