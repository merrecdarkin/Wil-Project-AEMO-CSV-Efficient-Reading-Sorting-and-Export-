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
        - List all the directories within that folder path (this will include both files and sub-folders)
        - Check for valid CSV file from the directory list (check app.isValidCSVFile for function explanation)
        - After getting all the valid CSV file name, update it to the side panel in GUI
        """
        selectedFolderPath= values["-FOLDER-"]
        fileInSelectedFolder = os.listdir(selectedFolderPath)
        validCSVFile = [f for f in fileInSelectedFolder if app.isValidCSVFile(f,selectedFolderPath)]
        window["-FILE LIST-"].update(validCSVFile)

    if event== "-CONFIRM-": # Export button callback event
        """
        Workflow of this callback event is initially similar to folder browser event
        After getting all the valid CSV file name, it will construct a full file path for each of the CSV, so that they can be read later
        """
        selectedFolderPath= values["-FOLDER-"]
        fileInSelectedFolder = os.listdir(selectedFolderPath)
        validCSVFile = [f for f in fileInSelectedFolder if app.isValidCSVFile(f,selectedFolderPath)]
        validCSVFilePath = [os.path.join(selectedFolderPath, f) for f in validCSVFile] # Construct full file path for CSV files
        
        """
        After getting CSV file paths, the app now fetch the user input data from the input text fields
        DUIDset and BIDTYPEset are separated by space so .split() method is used to split each of them and add to the query list
        DATESTARTset and DATEENDset need to be init as an empty string, this is to make sure they can be passed to app.loadCSV() method if the user left them blank
        If any of DATE field is specified, convert them from str to datetime type with datetime.strptime()
        """
        DUIDset = values['-INPUT DUID-'].split()
        BIDTYPEset = values['-INPUT BIDTYPE-'].split()
        DATESTARTset = DATEENDset = ''
        if values['-INPUT DATE START-']:
            DATESTARTset = datetime.strptime(values['-INPUT DATE START-'],'%d/%m/%Y')  
        if values['-INPUT DATE END-']:
            DATEENDset = datetime.strptime(values['-INPUT DATE END-'],'%d/%m/%Y')
        """
        Since there will be multiple CSV file loaded, this is the current workflow to merge all the data to a single output:
        - Init an empty output list (this is needed because pd.concat() methods read a list of pd.dataframe obj and merge them)
        - Read each of the CSV file one-by-one (use for loop to loop through the list of CSV file path)
        - For each CSV file, we cann app.loadCSV() and pass the query data as params to the function
        - For each loop, we loop through a single CSV file, and the function return a df.dataframe object as the queried result
        - We add the result dataframe object to the output list
        - Finally we call pd.concat() to merge all the separated dataframe in the output list to a unified dataframe/output table
        - to_excel() method is called to write the table into an output excel file, this requires openpyxl library
        """
        output = []
        for f in validCSVFilePath:
            output.append(app.loadCSV(f,DUIDset,BIDTYPEset,DATESTARTset,DATEENDset))
        pd.concat(output).to_excel("output.xlsx")
        os.startfile("output.xlsx") # Autorun the output excel after export

window.close()
