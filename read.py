import csv
import datetime
import os
import os.path
import sqlite3
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PySimpleGUI as sg
from dateutil.parser import parse
from matplotlib.figure import Figure


def loadCSV(nameOfCSV,DUIDsets,folPath):
    print(folPath)
    PathAndNameFile=folPath+"/"+nameOfCSV
    df = pd.read_csv(PathAndNameFile, skiprows=1, skipfooter=1, on_bad_lines='skip')

    for targetDUID in DUIDsets:
        print(df.loc[df['DUID'] == targetDUID])     
    df2 = pd.read_csv(PathAndNameFile, skiprows=len(df. index)+2, skipfooter=1, on_bad_lines='skip')
    for targetDUID in DUIDsets:
        print(df2.loc[df2['DUID'] == targetDUID])     




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
                        loadCSV(f,DUIDsets,folder)


window.close()
