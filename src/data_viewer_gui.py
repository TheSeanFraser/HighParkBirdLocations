###############################################################################
#   mainMenuGUI
#   Started: 2021-JUL-18
#   Updated: 2021-JUL-18
###############################################################################

from tkinter import *
import tkinter as tk

def start_data_viewer_gui(main_menu_root):
    # Set the main window of the application
    root = main_menu_root

    root.geometry('1200x1000')
    root.resizable(width=False, height=False)
    root.title("High Park Bird Locations -- Data Viewer")
    root.lift()
    root.attributes("-topmost", True)