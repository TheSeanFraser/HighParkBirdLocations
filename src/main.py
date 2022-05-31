from tkinter import *
import tkinter as tk
from import_checklist import import_checklist
from data_collector_gui import start_new_gui


# Create the GUI
def start_gui():
    main_menu_root = tk.Tk()
    main_menu_root.geometry('400x300')
    main_menu_root.resizable(width=False, height=False)
    main_menu_root.title("High Park Bird Locations")

    checklist_data = import_checklist()
    start_new_gui(main_menu_root, checklist_data)

    main_menu_root.mainloop()


start_gui()
