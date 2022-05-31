###############################################################################
#   checklistImporter
###############################################################################

import csv
import os
from tkinter.filedialog import askopenfilename
import tkinter as tk
import re


# Columns of the checklist data is as follows:
#   0       1       2           3                   4               5           6       7         8       9         10              11              12          13
# [Species, Count, Location, Observation type, Observation date, Start Time, Duration, Distance, Area, Elevation, Party Size, Complete Checklist, # of species, Details]


# Imports the data from the checklist
def import_checklist():
    # Create a window
    root = tk.Tk()
    root.withdraw()
    root.update()

    # Open a file select dialog
    filename = askopenfilename(title="Select file",
                               filetypes=[("Checklist CSV Files", "*.csv")])

    # Open checklist file and create an array of the data
    with open(filename, newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        checklist_data = list(csv.reader(csv_file))

    # Find checklist ID in filename
    checklist_match = re.search('(S(.\d*))', filename)
    if checklist_match:
        checklist_id = checklist_match.group(0)

    # Add checklist ID to the end of the list, for easy access
    checklist_data.append(checklist_id)

    root.destroy()

    return checklist_data
