###############################################################################
# WORK IN PROGRESS - Currently doesn't contribute to anything
###############################################################################

import plotly.express as px
import pandas as pd
import config
import plotly.graph_objects as go
from sql_manager import create_db_connection, read_query


###############################################################################
# Helper functions
###############################################################################
# Clean up the species list to only include the name
def species_list_cleaner(species_list_input):
    cleanSpeciesList = []
    for species in species_list_input:
        cleanSpeciesList.append(species[0])

    return cleanSpeciesList


###############################################################################
# Main function
###############################################################################
def checklist_chart_maker(checklist_id="S92367052"):
    # Set SQL query to get the data for the selected species
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
    from_db = []
    for result in results:
        result = list(result)
        from_db.append(result)

    columns = ["id", "species", "effort", "latitude", "longitude", "surface",
               "checklistID", "date", "time", "location", "duration"]

    # Create pandas DataFrame of data
    df = pd.DataFrame(from_db, columns=columns)

    # Create series of sorted species and counts of species
    dfSpecies = df.sort_values("species")
    dfSpeciesSorted = dfSpecies["species"].unique()
    dfSpeciesCount = df.groupby("species").id.nunique()

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Species", "Total", "% Water", "% Ground", "% Structure",
                    "% Tree", "% Air"],
            fill_color='paleturquoise',
            align='left'),
        cells=dict(
            values=[dfSpeciesSorted, dfSpeciesCount, [1, 2, 3, 4, 5555, 4634]],
            fill_color='lavender',
            align='left'))
    ])

    fig.show()
    # fig.write_html(config.web_path + "charts\\checklists\\" + checklistID + "  Table.html")


# checklist_chart_maker()

def make_all_checklist_charts():
    checklists = []
    f = open(config.dir_path + "maps\\checklists\\checklistList.txt")
    for line in f:
        checklists.append(line.split(' ')[1].strip("\n"))
    f.close()
    for checklist in checklists:
        print("Making map for " + checklist)
        checklist_chart_maker(checklist)
    print("All charts created!")

# make_all_checklist_charts()
