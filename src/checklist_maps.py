from ipywidgets import HTML
import config
from ipyleaflet import Map, Heatmap, FullScreenControl, Marker, LayersControl, MarkerCluster
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


# Returns a heatmap created from the results
def heatmap_layer_maker(checklist_data):
    heatmap_list = []
    for entry in checklist_data:
        current_gps_coord = (entry[3],entry[4])
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

    # Create the marker cluster for each represented bird
    marker_cluster = MarkerCluster(name="Markers",
                                   markers=marker_layer_maker(checklist_data))

    # Add all the layers to the map
    m.add_layer(heatmap)
    m.add_layer(marker_cluster)

    # Save the map for the checklist
    m.layout.width = '100%'
    m.layout.height = '500px'

    m.save(config.web_path + 'maps\\checklists\\'
           + checklist_id + '.html',
           title='Map for: ' + checklist_id)


# Creates a map for the selected checklist
def checklist_map_maker(checklist_id):
    print("Making map for " + checklist_id )
    # Select a group with specific checklistID
    qChecklist = """
    SELECT * 
    FROM birds
    INNER JOIN effort
    ON birds.effort = effort.checklistID
    WHERE effort = '""" + checklist_id + """';"""

    # Create a connection and store the results of the query
    connection = create_db_connection(config.my_host, config.my_user,
                                      config.my_pwd, config.my_db)
    results = read_query(connection, qChecklist)

    # Create a list from the database results
    checklist_data = []
    for result in results:
        result = list(result)
        checklist_data.append(result)

    create_map(checklist_id, checklist_data)
    print("Map for " + checklist_id + " created.")


# Remakes all available checklist maps
def remake_all_checklist_maps():
    checklists = []
    # Read list of checklists
    f = open(config.web_path + "maps\\checklists\\checklistList.txt")
    for line in f:
        checklists.append(line.split(' ')[1].strip("\n"))
    f.close()

    # Create the map for each checklist
    for checklist in checklists:
        print("Making map for " + checklist)
        checklist_map_maker(checklist)


# checklist_map_maker("S92746003")
# remake_all_checklist_maps()

