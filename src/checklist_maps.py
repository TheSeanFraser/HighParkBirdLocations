from ipywidgets import HTML
import config
import resources
import gc
from ipyleaflet import Map, Heatmap, FullScreenControl, Marker, LayersControl, \
    MarkerCluster, AwesomeIcon
from sql_manager import create_db_connection, read_query


# Returns a list of Markers with gps locations and species titles
def marker_layer_maker(checklist_data):
    marker_list = []
    for entry in checklist_data:
        pop_up_html = HTML()
        pop_up_html.value = entry[1] + ": <b>" + entry[5] + "</b>"
        marker_list.append(Marker(location=(entry[3], entry[4]),
                                  draggable=False,
                                  title=entry[1] + ', ' + entry[7],
                                  popup=pop_up_html))
    return marker_list


# Creates a marker list for the given family of birds
def family_marker_layer_maker(current_family, checklist_data):
    marker_list = []
    for entry in checklist_data:
        # Check if species is protected, if so skip
        if entry[13] == 0:
            # Check if the current bird is in the current family
            if entry[12] == current_family:
                pop_up_html = HTML()
                pop_up_html.value = entry[1] + ": <b>" + entry[5] + "</b>"
                color = list(resources.family_colors[current_family])[0]

                color2 = 'black'
                if color == 'black' or color == 'darkgray':
                    color2 = 'lightgray'

                icon_choice = 'chevron-circle-down'
                if entry[5] == 'TREE':
                    icon_choice = 'tree'
                elif entry[5] == 'WATER':
                    icon_choice = 'tint'
                elif entry[5] == 'AIR':
                    icon_choice = 'plane'
                elif entry[5] == 'GROUND':
                    icon_choice = 'square'
                elif entry[5] == 'STRUCTURE':
                    icon_choice = 'building'

                icon = AwesomeIcon(name=icon_choice,
                                   marker_color=color,
                                   icon_color=color2,
                                   spin=False)

                marker_list.append(Marker(location=(entry[3], entry[4]),
                                          icon=icon,
                                          draggable=False,
                                          title=entry[1] + ', ' + entry[7],
                                          popup=pop_up_html))
    return marker_list


# Returns a heatmap created from the results
def heatmap_layer_maker(checklist_data):
    heatmap_list = []
    for entry in checklist_data:
        # Check if species is not protected
        if entry[13] == 0:
            current_gps_coord = (entry[3], entry[4])
            heatmap_list.append(current_gps_coord)
    return heatmap_list


# Create a map based on the selected species
def create_map(checklist_id, checklist_data):
    # Create the map object and set some options
    m = Map(center=(43.64632654828124, -79.46253966380962),
            zoom=14,
            scroll_wheel_zoom=True)
    m.layout.width = '100%'
    m.layout.height = '400px'
    m.add_control(FullScreenControl())
    m.add_control(LayersControl(position='topright'))

    # Create the heatmap layer
    heatmap = Heatmap(name="Heatmap",
                      locations=heatmap_layer_maker(checklist_data),
                      min_opacity=0.01,
                      max=1.5,
                      radius=15)

    # Add all the layers to the map
    m.add_layer(heatmap)

    # Create a list of bird families in the current checklist
    family_list = []
    for entry in checklist_data:
        if entry[12] not in family_list:
            family_list.append(entry[12])

    # Create a marker cluster for each family of bird
    for family in family_list:
        marker_cluster = MarkerCluster(name=family,
                                       markers=family_marker_layer_maker(family,
                                                                         checklist_data))
        m.add_layer(marker_cluster)

    # Save the map for the checklist
    m.layout.width = '100%'
    m.layout.height = '500px'

    m.save(config.dir_path + 'maps\\checklists\\'
           + checklist_id + '.html',
           title='Map for: ' + checklist_id)

    # Clear the map to prevent sizes increasing
    m.clear_controls()
    m.clear_layers()
    m.close_all()
    m.close()
    del m


# Creates a map for the selected checklist
def checklist_map_maker(checklist_id, remake_flag=False):
    print("Making map for " + checklist_id)
    # Select a group with specific checklistID
    q_checklist = """
    SELECT * 
    FROM birds
    INNER JOIN effort
    ON birds.effort = effort.checklistID
    INNER JOIN species
    ON birds.species = species.species_name
    WHERE effort = '""" + checklist_id + """';"""

    # Create a connection and store the results of the query
    connection = create_db_connection(config.my_host, config.my_user,
                                      config.my_pwd, config.my_db)
    results = read_query(connection, q_checklist)

    # Create a list from the database results
    checklist_data = []
    for result in results:
        result = list(result)
        checklist_data.append(result)

    create_map(checklist_id, checklist_data)
    if not remake_flag:
        with open(config.dir_path + "maps\\checklists\\checklistList.txt",
                  "a") as checklists_file:
            entry = checklist_data[0][7] + ": " + checklist_id + "\n"
            checklists_file.write(entry)

    print("Map for " + checklist_id + " created.")


# Remakes all available checklist maps
def remake_all_checklist_maps():
    connection = create_db_connection(config.my_host, config.my_user,
                                      config.my_pwd, config.my_db)
    q = """
    SELECT * FROM effort;
    """

    results = read_query(connection, q)
    # Cleanly add data to a list
    checklists_data = []
    for entry in results:
        entry = list(entry)
        checklists_data.append(entry)

    # Open and empty checklist list file
    checklist_file = open(config.dir_path
                          + "maps\\checklists\\checklistList.txt", "r+")
    checklist_file.truncate(0)
    checklist_file.close()

    # Iterate through all checklists, add to list file, and make map
    for checklist in checklists_data:
        cur_checklist_id = checklist[0]
        cur_checklist_date = checklist[1]

        # Add checklist to checklist list file
        with open(config.dir_path + "maps\\checklists\\checklistList.txt",
                  "a") as checklists_file:
            entry = cur_checklist_date + ": " + cur_checklist_id + "\n"
            checklists_file.write(entry)
            checklist_file.close()

        checklist_map_maker(cur_checklist_id, remake_flag=True)


# checklist_map_maker("S93979335")
