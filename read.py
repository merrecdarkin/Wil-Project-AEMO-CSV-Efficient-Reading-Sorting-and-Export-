import matplotlib.pyplot as plt;
from matplotlib.figure import Figure
import numpy as np;
import sqlite3, csv, os, datetime, zipfile
from pathlib import Path
from dateutil.parser import parse
import os.path
import PySimpleGUI as sg





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

image_viewer_column = [
    [sg.Text("Choose an image from the list on the left:")],
    [sg.Text(size=(40,1), key="-TOUT-")],
    [sg.Image(key="-IMAGE")],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),

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
            print(folder)
            for f in file_list:
                if os.path.isfile(os.path.join(folder, f))  and f.lower().endswith((".csv")):
                    print(f)
        except:
            file_list=[]
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".csv"))
        ]
        window["-FILE LIST-"].update(fnames)
window.close()