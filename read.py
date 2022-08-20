import matplotlib.pyplot as plt;
from matplotlib.figure import Figure
import numpy as np;
import sqlite3, csv, os, datetime, zipfile
from pathlib import Path
from dateutil.parser import parse
import os.path
import PySimpleGUI as sg

def loadCSV(nameOfCSV,DUIDsets):
    with open(nameOfCSV,'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            for targetDUID in DUIDsets:
                if line[5]==targetDUID :
                    print(line)



file_list_column = [
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

input_column = [
    [sg.Text("User input pannel Placeholder")],
    [sg.Text(size=(40,1), key="-TOUT-")],
    [sg.Text("Target DUID")],
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

window = sg.Window("File Comp",layout)

while True:
    event, values = window.read()
    if event == "Exit" or event ==sg.WIN_CLOSED:
        break
    if event== "-FOLDER-":
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
                        DUIDsets= values["-INPUT DUID-"].split()
                        loadCSV(f,DUIDsets)


window.close()