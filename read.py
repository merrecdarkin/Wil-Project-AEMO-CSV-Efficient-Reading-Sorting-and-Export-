import csv
import matplotlib.pyplot as plt;
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np;
import pandas as pd
import sqlite3, csv, os, datetime, wx, wx.adv
from wx.adv import CalendarCtrl
from pathlib import Path
from dateutil.parser import parse
import wx
import wx.grid as gridlib


from logging import PlaceHolder
with open('PlaceHolder.csv', newline='') as csvfile:
    readline= csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in readline:
        print(', '.join(row))