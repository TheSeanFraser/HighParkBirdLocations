import plotly.express as px
import pandas as pd
import config
from sql_manager import create_db_connection, read_query


###############################################################################
# Main function
###############################################################################
def species_chart_maker(connection, species="Cooper''s Hawk"):
    # Create a cleaned species name for file name
    species_apo_fixed = species.replace("''", "'")
    species_slash_fixed = species_apo_fixed.replace('/', ' or ')

    # Set SQL query to get the data for the selected species
    q_species = """
    SELECT * 
    FROM birds
    INNER JOIN effort
    ON birds.effort = effort.checklistID
    WHERE birds.species = '""" + species + """';"""

    # Get results from SQL server
    results = read_query(connection, q_species)

    # Create a list from the database results
    from_db = []
    for result in results:
        result = list(result)
        from_db.append(result)
    columns = ["id", "species", "effort", "latitude", "longitude", "surface",
               "checklistID", "date", "time", "location", "duration"]
    # Create pandas DataFrame of data
    df = pd.DataFrame(from_db, columns=columns)

    fig = px.bar(df, x="date", color="surface",
                 color_discrete_map={'GROUND': 'sandybrown',
                                     'TREE': 'seagreen',
                                     'AIR': 'skyblue',
                                     'WATER': 'royalblue',
                                     'STRUCTURE': 'darkslategrey'},
                 category_orders={"surface":
                                      ["GROUND", "WATER", "STRUCTURE", "TREE",
                                       "AIR"]},
                 title=species + " surface observations")
    fig.write_html(config.dir_path + "charts\\species\\"
                   + species_slash_fixed + " Bar Graph.html")

    # Count the occurrences of each surface
    air_count = len(df[df["surface"] == "AIR"])
    water_count = len(df[df["surface"] == "WATER"])
    ground_count = len(df[df["surface"] == "GROUND"])
    tree_count = len(df[df["surface"] == "TREE"])
    structure_count = len(df[df["surface"] == "STRUCTURE"])

    # Create a pie chart
    labels = ["AIR", "WATER", "GROUND", "TREE", "STRUCTURE"]
    values = [air_count, water_count, ground_count, tree_count, structure_count]
    fig2 = px.pie(labels=labels, values=values, names=labels, color=labels,
                  color_discrete_map={
                      'GROUND': 'sandybrown',
                      'TREE': 'seagreen',
                      'AIR': 'skyblue',
                      'WATER': 'royalblue',
                      'STRUCTURE': 'darkslategrey'
                  }, title=species + " surface observations")
    fig2.write_html(
        config.dir_path + "charts\\species\\" + species_slash_fixed + " Pie Graph.html")


# Create the charts for every species in database
def make_all_species_charts(checklist_species=None):
    # Create a connection to the SQL server
    connection = create_db_connection(config.my_host, config.my_user,
                                      config.my_pwd, config.my_db)

    species_list = []
    f = open(config.dir_path + "maps\\species\\speciesList.txt")
    for line in f:
        species_list.append(line.strip("\n"))
    f.close()

    print("Started making charts.")
    if checklist_species:
        print("Checklist species provided - making charts")
        for species_in_checklist in checklist_species:
            species = species_in_checklist
            species = species.replace("'", "''")
            species = species.replace(' or ', '/')
            species_chart_maker(connection, species)
    else:
        for species in species_list:
            species = species.replace("'", "''")
            species = species.replace(' or ', '/')
            species_chart_maker(connection, species)
    print("All charts created!")


# make_all_species_charts()
