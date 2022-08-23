import os
import os.path
import PySimpleGUI as sg

import App as app

file_list_column = [  #Most GUI layout will be done in this section
    [
        sg.Text("csv Folder"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40,20),
            key="-FILE LIST-"
        )
    ],
]

input_column = [ #These are input fiels and their corresponding fetch ID to be use later
    [sg.Text("User input pannel Placeholder")],
    [sg.Text(size=(40,1), key="-TOUT-")],
    [sg.Text("Target DUID (seperate via space)")],
    [sg.InputText(key="-INPUT DUID-")],

    [sg.Text("From date d/mm/yyyy")],
    [sg.InputText(key="-INPUT DATE START-")],
    [sg.Text("To date")],
    [sg.InputText(key="-INPUT DATE END-")],
    [sg.Button('Confirm', button_color=('white', 'firebrick3'), key='-CONFIRM-')]

]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(input_column),

    ]
]

window = sg.Window("File Comp",layout)  #This is GUI interaction function section

while True:
    event, values = window.read()
    if event == "Exit" or event ==sg.WIN_CLOSED:
        break
    if event== "-FOLDER-": #This is GUI Folder button (currently perfect and need no change)
        folder= values["-FOLDER-"]
        try:
            file_list= os.listdir(folder)
            

        except:
            file_list=[]
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".csv")) and ("PUBLIC_BIDMOVE_COMPLETE" in f)
        ]
        window["-FILE LIST-"].update(fnames)

    if event== "-CONFIRM-":
        folder= values["-FOLDER-"]
        print(folder)
        for f in file_list:
                if os.path.isfile(os.path.join(folder, f))  and f.lower().endswith((".csv")) and ("PUBLIC_BIDMOVE_COMPLETE" in f):
                    print(f)
                    if values["-INPUT DUID-"] != "": 
                        DUIDsets= values["-INPUT DUID-"].split() #This will fetch Value from inputs, require further expansion
                        app.loadCSV(f,DUIDsets,folder)


window.close()