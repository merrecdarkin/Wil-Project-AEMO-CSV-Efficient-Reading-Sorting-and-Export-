import csv
from logging import PlaceHolder
with open('PlaceHolder.csv', newline='') as csvfile:
    readline= csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in readline:
        print(', '.join(row))