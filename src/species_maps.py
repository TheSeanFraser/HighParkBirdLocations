import timeit
from ipywidgets import HTML
import config
from ipyleaflet import Map, Heatmap, FullScreenControl, Marker, LayersControl, MarkerCluster
from sql_manager import create_db_connection, read_query

# Generated species list based on SQL database results
def create_species_list(connection):
    # SQL query to get the list of distinct species seen
    qSpeciesList = """
    SELECT DISTINCT birds.species, species.species_protected
    FROM birds 
    INNER JOIN species 
    ON birds.species = species.species_name;
    """

    species_list_result = read_query(connection, qSpeciesList)

    # List for making maps for non-protected species
    species_list_non_protected = []

    # Store list of species for website
    species_text_file = open(config.web_path + "maps\\species\\speciesList.txt", "w")
    for species in species_list_result:
        # If species is protected, skip it for the map making
        if(species[1]):
            print(species[0] + " is protected. Skipping species.")
        else:
            species_list_non_protected.append(species[0])
            species_text_file.write(species[0] + "\n")
    species_text_file.close()

    print("SpeciesList created.")
    return species_list_non_protected

######## MASTER FUNCTION ########

# Returns the data for a single species from the SQL server
def get_single_species_data(connection, species):
    # Must add second single quote in order to manage apostrophes (e.g. Cooper's Hawk -> Cooper''s Hawk)
    species_apo_fixed = species.replace("'", "''")

    qSingleSpecies = """
        SELECT * FROM birds 
        INNER JOIN effort ON birds.effort = effort.checklistID 
        INNER JOIN species ON birds.species = species.species_name 
        WHERE birds.species = \'""" + species_apo_fixed + """\';"""

    # Get the data from the SQL server for this species
    results = read_query(connection, qSingleSpecies)

    # Cleanly add data to a list
    single_species_data = []
    for entry in results:
        entry = list(entry)
        single_species_data.append(entry)

    return single_species_data

# Returns a list of GPS coordinates based on the selected species
def heatmap_layer_maker(single_species_data):
    heatmap_list = []
    for entry in single_species_data:
        current_gps_coord = (entry[3], entry[4])
        heatmap_list.append(current_gps_coord)
    return heatmap_list

# Creates a MarkerLayer for the batch of coordinates
def marker_layer_maker(single_species_data):
    marker_list = []
    for entry in single_species_data:
        pop_up_html = HTML()
        pop_up_html.description = entry[7]
        pop_up_html.value = "<b>" + entry[5] + "</b>"
        marker_list.append(Marker(location=(entry[3], entry[4]),
                                  draggable=False,
                                  title=entry[1] + ', ' + entry[7],
                                  popup=pop_up_html))
    return marker_list

# Create a single map for the selected species
def create_map(species, single_species_data):
    # Create the map object and set some options
    m = Map(center=(43.64632654828124, -79.46253966380962),
            zoom=14,
            scroll_wheel_zoom=True)
    m.layout.width = '100%'
    m.layout.height = '500px'
    m.add_control(FullScreenControl())
    m.add_control(LayersControl(position='topright'))

    # Create the heatmap layer
    heatmap = Heatmap(name="Heatmap",
                             locations=heatmap_layer_maker(single_species_data),
                             min_opacity=0.01,
                             max=1.5,
                             radius=15)

    # Create the marker cluster for each represented bird
    marker_cluster = MarkerCluster(name="Markers", markers=marker_layer_maker(single_species_data))

    # Add all the layers to the map
    m.add_layer(heatmap)
    m.add_layer(marker_cluster)

    m.save(config.web_path + 'maps\\species\\' + species + '.html', title=species + ' Map')

# Create a map for each of the species
def map_all_species():
    # Create a connection to the SQL server
    connection = create_db_connection(config.my_host, config.my_user, config.my_pwd, config.my_db)
    # Create the species list
    species_list = create_species_list(connection)

    # Start a timer - not necessary, but just to know how long this takes
    maps_start_time = timeit.default_timer()

    print("Starting species maps.")
    # Loop through each species, get data from SQL, and make a map
    for species in species_list:
        # Get data from SQL server
        singleSpeciesData = get_single_species_data(connection, species)
        # Create and save the map
        create_map(species, singleSpeciesData)

    # Stop timer and alert that all maps are made
    maps_stop_time = timeit.default_timer()
    total_time = round(maps_stop_time - maps_start_time, 4)
    print("--- All species maps created! Total time elapsed: " + str(total_time) + "seconds ---")


# map_all_species()