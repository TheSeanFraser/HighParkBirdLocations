from tkinter import *
import tkinter as tk
from import_checklist import import_checklist
from data_viewer_gui import start_data_viewer_gui
from data_collector_gui import start_new_gui

main_menu_root = None
menu_frame = None


# Create the main menu
def main_menu_gui():
    global main_menu_root, menu_frame

    main_menu_root = tk.Tk()
    main_menu_root.geometry('400x300')
    main_menu_root.resizable(width=False, height=False)
    main_menu_root.title("High Park Bird Locations")

    menu_frame = Frame(main_menu_root)
    menu_frame.pack()

    collect_data_button = Button(menu_frame, text="Import Data", command=start_data_collection)
    collect_data_button.pack()

    view_data_button = Button(menu_frame, text="View Data", command=start_data_viewer)
    view_data_button.pack()

    main_menu_root.mainloop()


# Start the data collection GUI
def start_data_collection():
    global main_menu_root, menu_frame
    checklist_data = import_checklist()
    menu_frame.destroy()
    start_new_gui(main_menu_root, checklist_data)


# Start the data viewer GUI - currently does nothing
def start_data_viewer():
    global main_menu_root, menu_frame
    start_data_viewer_gui(main_menu_root)
    menu_frame.destroy()

main_menu_gui()