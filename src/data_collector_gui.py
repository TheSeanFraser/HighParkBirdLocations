import string
import random
from tkinter import *
import tkinter as tk
import config
from PIL import ImageTk, Image
from sql_manager import insert_data_to_sql
from resources import birdColors
from checklist_maps import checklist_map_maker
from species_maps import map_all_species
from species_charts import make_all_species_charts
from threading import *

###############################################################################
#                   -- DataCollectorGUI Class --
#   Builds a GUI to collect GPS coordinates from the checklist data
#   Draws dots on the map to show recorded birds
###############################################################################


class DataCollectorGUI:
    # Initialize object with data and create GUI
    def __init__(self, master_root, checklist, output_data):
        self.surface = "AIR"
        self.data_output_complete = False
        self.checklist = checklist
        self.output_data = output_data
        self.build_gui(master_root)
        master_root.mainloop()

    # Builds the GUI to display on screen
    def build_gui(self, master_root):
        master_root.geometry('1200x1000')
        master_root.resizable(width=False, height=False)
        master_root.title("High Park Bird Locations -- Data Collector")
        master_root.lift()
        master_root.attributes("-topmost", True)

        self.map_frame = Frame(master_root, width=700, height=1000)
        self.map_frame.pack_propagate(0)
        self.map_frame.pack(side=LEFT, fill=Y)

        # Get and set the map image canvas
        self.image = Image.open(config.map_path)
        self.map_image = ImageTk.PhotoImage(self.image)
        self.map_canvas = Canvas(self.map_frame, bg="grey", width=670,
                                 height=900)
        self.map_canvas.pack(fill=BOTH, expand=YES)
        self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map_image)
        self.map_canvas.bind("<Button-1>", self.left_click)

        # Make a frame for the list on the right
        self.list_frame = Frame(master_root, width=700, height=980)
        self.list_frame.pack_propagate(0)
        self.list_frame.pack(fill=Y)

        # Make a frame for the top of the list
        self.list_frame_top = Frame(self.list_frame, width=700, height=80)
        self.list_frame_top.pack(side=TOP)

        # Set the top of the checklist & status
        self.list_label_text = StringVar()
        self.set_species_and_count_text()
        self.list_label = Label(self.list_frame_top,
                                font=('arial', 12, 'bold'),
                                textvariable=self.list_label_text,
                                bd=5,
                                anchor=W)
        self.list_label.pack(side=LEFT)

        # Make a button for skipping to the next species
        self.skip_species_button = Button(self.list_frame_top,
                                          text='Skip To Next Species',
                                          command=self.skip_species_button_handler)
        self.skip_species_button.pack(side=RIGHT)

        # Make a frame for the SURFACE radio buttons
        self.surface_buttons_frame = Frame(self.list_frame)
        self.surface_buttons_frame.pack(side=TOP)
        self.surface_var = IntVar()
        self.air_r_btn = Radiobutton(self.surface_buttons_frame,
                                     text="AIR",
                                     variable=self.surface_var,
                                     value=1,
                                     command=self.surface_radio_buttons_handler)
        self.ground_r_btn = Radiobutton(self.surface_buttons_frame,
                                        text="GROUND",
                                        variable=self.surface_var,
                                        value=2,
                                        command=self.surface_radio_buttons_handler)
        self.tree_r_btn = Radiobutton(self.surface_buttons_frame,
                                      text="TREE",
                                      variable=self.surface_var,
                                      value=3,
                                      command=self.surface_radio_buttons_handler)
        self.water_r_btn = Radiobutton(self.surface_buttons_frame,
                                       text="WATER",
                                       variable=self.surface_var,
                                       value=4,
                                       command=self.surface_radio_buttons_handler)
        self.structure_r_btn = Radiobutton(self.surface_buttons_frame,
                                           text="STRUCTURE",
                                           variable=self.surface_var,
                                           value=5,
                                           command=self.surface_radio_buttons_handler)

        self.air_r_btn.pack(side=LEFT, anchor=W)
        self.ground_r_btn.pack(side=LEFT, anchor=W)
        self.tree_r_btn.pack(side=LEFT, anchor=W)
        self.water_r_btn.pack(side=LEFT, anchor=W)
        self.structure_r_btn.pack(side=LEFT, anchor=W)
        self.air_r_btn.select()

        self.species_list_labels = []
        for row in self.checklist.data:
            label = tk.Label(self.list_frame, text=row[0] + ' : ' + row[1])
            label.pack()
            self.species_list_labels.append(label)

    # Updates the GUI element to display the current species
    # Executes data output to SQL if collection complete
    def set_species_and_count_text(self):
        if self.checklist.end_of_checklist_reached:
            if not self.data_output_complete:
                self.list_label_text.set("Complete ")
                # media_making_thread = Thread(self.output_data.upload_data_and_make_media(self.output_data))
                # media_making_thread.start()
                self.output_data.upload_data_and_make_media(self.output_data)
                self.data_output_complete = True
        else:
            self.list_label_text.set(
                "Current species: "
                + self.checklist.data[self.checklist.current_species][0]
                + " "
                + str(self.checklist.count_of_current_species))

    # Handles the surface radio buttons
    def surface_radio_buttons_handler(self):
        if self.surface_var.get() == 1:
            self.surface = "AIR"
        elif self.surface_var.get() == 2:
            self.surface = "GROUND"
        elif self.surface_var.get() == 3:
            self.surface = "TREE"
        elif self.surface_var.get() == 4:
            self.surface = "WATER"
        elif self.surface_var.get() == 5:
            self.surface = "STRUCTURE"

    # Handles the skip species button
    def skip_species_button_handler(self):
        self.species_list_labels[self.checklist.current_species].pack_forget()
        self.checklist.__next__()
        self.set_species_and_count_text()

    # Draws a dot on the map to represent a bird
    def draw_dot(self, x, y):
        # Set the colors of the dot based on saved colors list
        if self.checklist.data[self.checklist.current_species][0] in birdColors:
            outline = birdColors[self.checklist.data[self.checklist.current_species][0]][0]
            fill = birdColors[self.checklist.data[self.checklist.current_species][0]][1]
        else:
            outline = 'red'
            fill = 'red'

        dot = self.map_canvas.create_oval(x + 4, y + 4, x - 4, y - 4, width=2,
                                          outline=outline, fill=fill)

    # Handles the left click events: draw a dot, update list position
    def left_click(self, event):
        if not self.checklist.end_of_checklist_reached:
            if int(self.checklist.count_of_current_species) > 1:
                self.draw_dot(event.x, event.y)
                # (species, gps_lat, gps_lon, surface):
                self.output_data.add_bird(self.checklist.data[self.checklist.current_species][0],
                                          event.x,
                                          event.y,
                                          self.surface)
                self.checklist.count_of_current_species -= 1
                self.set_species_and_count_text()
            else:
                self.draw_dot(event.x, event.y)
                self.species_list_labels[self.checklist.current_species].pack_forget()
                self.set_species_and_count_text()
                self.output_data.add_bird(
                    self.checklist.data[self.checklist.current_species][0],
                    event.x,
                    event.y,
                    self.surface)
                self.checklist.__next__()

###############################################################################
#                       -- Checklist Class --
#   Contains the data from the checklist and can iterate through it
###############################################################################


class Checklist:
    def __init__(self, checklist_data):
        print("New Checklist Data Imported")
        self.checklist_id = checklist_data.pop()
        self.date = checklist_data[0][4]
        self.time = checklist_data[0][5]
        self.duration = checklist_data[0][6]
        self.location = checklist_data[0][2]
        self.data = checklist_data
        self.total_species = len(checklist_data)
        self.current_species = 0
        self.count_of_current_species = int(checklist_data[0][1])
        self.end_of_checklist_reached = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self.end_of_checklist_reached:
            if int(self.current_species) >= (int(self.total_species) - 1):
                # Set collection to complete
                self.end_of_checklist_reached = True
            else:
                self.current_species += 1
                self.count_of_current_species = int(self.data[self.current_species][1])
        else:
            print("All species already completed.")


###############################################################################
#                       -- OutputData Class --
#   Stores the data collected in the GUI, modifies it to be in the storage
#   format, and sends it to the SQL server & makes media
###############################################################################


class OutputData:
    # Create the OutputData object
    def __init__(self):
        self.data = []
        self.date = None
        self.time = None
        self.duration = None
        self.location = None
        self.checklist_id = None
        self.checklist_species = {}

    # Generates a random id for storage
    def generate_bird_id(self):
        bird_id = random.choice(string.ascii_uppercase) \
                  + random.choice(string.ascii_uppercase) \
                  + random.choice(string.ascii_uppercase) \
                  + '-' + str(random.randint(3, 2147483647))
        return bird_id

    # Calculate the actual GPS coordinates based on the position clicked
    def calculate_gps_coord(self, x, y):
        # Convert the coordinates to work on the lat/lon plane
        converted_x_coord = x - 699
        converted_y_coord = 998 - y
        # GPS coordinates calculated using Affine Translation
        # https://math.stackexchange.com/questions/2085093/
        # translation-between-two-coordinate-system-which-are-not-aligned
        gps_lat = (converted_x_coord * 0.000004327901773) \
                  + (converted_y_coord * 0.00001508376391) \
                  + 43.63997574
        gps_lon = (converted_x_coord * 0.00002080738607) \
                  + (converted_y_coord * -0.000006308317804) \
                  + -79.45284574
        return gps_lat, gps_lon

    # Adds a bird to the output data list
    def add_bird(self, species, x, y, surface):
        # Calculate actual GPS coordinates
        gps_lat, gps_lon = self.calculate_gps_coord(x, y)
        # (id, species, checklist id, gpsLat, gpsLon, surface)
        bird_tuple = (self.generate_bird_id(),
                      species,
                      self.checklist_id,
                      gps_lat,
                      gps_lon,
                      surface)
        # Add the bird to the output_data list
        self.data.append(bird_tuple)
        # Add species to the checklist_species dictionary (so only one entry)
        self.checklist_species[species] = 0

    # Copies the effort details from the checklist
    def copy_effort_details(self, checklist):
        self.date = checklist.date
        self.time = checklist.time
        self.duration = checklist.duration
        self.location = checklist.location
        self.checklist_id = checklist.checklist_id

    # Uploads data to SQL server and makes maps and charts
    def upload_data_and_make_media(self,output_data):
        insert_data_to_sql(self.data,
                           self.checklist_id,
                           self.date,
                           self.time,
                           self.duration,
                           self.location)
        print("==========================================================")
        checklist_map_maker(self.checklist_id)
        print("==========================================================")
        map_all_species(self.checklist_species)
        print("==========================================================")
        make_all_species_charts(self.checklist_species)
        print("==========================================================")
        print("==========================================================")
        print("                All media created!")


###############################################################################
#   Main Function
#   Starts the GUI with the checklist and output_data objects
###############################################################################
def start_new_gui(root, checklist_data):
    # Create a checklist object with the data imported from the checklist file
    checklist = Checklist(checklist_data)
    # Create an output_data object to store the collected data in
    output_data = OutputData()
    # Grab the effort details from the checklist object
    output_data.copy_effort_details(checklist)
    # Create the GUI object
    data_collector_gui = DataCollectorGUI(root, checklist, output_data)
