import mysql.connector
import ipywidgets as widgets
from mysql.connector import Error
from ipyleaflet import Map, Heatmap, FullScreenControl, LayersControl
from IPython.display import display
import config

# GLOBAL VARIABLES
selectedSpecies = "ALL"
m = Map()

# SQL QUERIES
q1 = """
SELECT *
FROM birds;
"""


# Connect to MySQL database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("--- MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


# Perform a read query on the SQL database
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


# PROGRAM STARTS HERE #############

# Create a connection and store the results of the query
connection = create_db_connection(config.my_host, config.my_user,
                                  config.my_pwd, config.my_db)
results = read_query(connection, q1)

# Create a list from the database results
from_db = []
for result in results:
    result = list(result)
    from_db.append(result)


# Returns a list of GPS coordinates based on the selected species
def heatmapLayerMaker(species="ALL", surface="ALL"):
    global results
    heatmap_list = []
    for entry in results:
        # Only add species if we are displaying it
        if species == entry[1] or species == "ALL":
            current_gps_coord = (entry[3], entry[4])
            heatmap_list.append(current_gps_coord)
    return heatmap_list


# Create a map based on the selected species
def createMap(species="ALL"):
    global m, selectedSpecies

    # Create the map object and set some options
    m = Map(
        center=(43.64632654828124, -79.46253966380962),
        zoom=14,
        scroll_wheel_zoom=True
    )

    m.layout.width = '100%'
    m.layout.height = '400px'
    m.add_control(FullScreenControl())

    # Create the heatmap layer
    heatmap = Heatmap(
        name="heatmap",
        locations=heatmapLayerMaker(selectedSpecies),
        min_opacity=0.01,
        max=1.5,
        radius=10
    )

    # Add all the layers to the map
    m.add_layer(heatmap)
    # Save the map for the checklist
    m.layout.width = '100%'
    m.layout.height = '500px'
    m.save(config.dir_path + '\\maps\\all_birds_map.html',
           title=' All Birds Map')


    return m


createMap()

# Save the map for the checklist
# m.layout.width = '100%'
# m.layout.height = '500px'
# m.save(config.dir_path + '\\maps\\all_birds_map.html', title=' All Birds Map')
