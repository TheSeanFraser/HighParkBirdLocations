from ipyleaflet import Map, Heatmap, FullScreenControl, Polygon
import config

locations = {
    "Howard and Ridout Pond": [(43.65316203180178, -79.46074683428375),
                               (43.65314699166003, -79.45994753599732),
                               (43.651455194256656, -79.46054298639862),
                               (43.65170409087088, -79.46135301352112)],
    "Bloor Street Savannah": [(43.65347132420393, -79.46514565706818),
                              (43.65240031666244, -79.46466822386353),
                              (43.65246266122634, -79.46129400492279),
                              (43.65410858282135, -79.46184653997986)],
    "Behind Nature Centre": [(43.65185012914491, -79.46288187265961),
                             (43.65155611152676, -79.46160514116852),
                             (43.649786638467255, -79.46155686140625),
                             (43.64986475450069, -79.46368653536408)],
    "All Star Cafe": [(43.649055, -79.464476),
                      (43.649746, -79.463709),
                      (43.649715, -79.461479),
                      (43.648610, -79.461347),
                      (43.647896, -79.463233),
                      (43.648005, -79.464348)],
    "Lower Duck Pond": [(43.640940917520425, -79.45739407301514),
                        (43.64117432930191, -79.45577938318817),
                        (43.63993252938227, -79.45504445791809),
                        (43.63997960081245, -79.45692736864655)],
    "Upper Duck Pond": [(43.64303285645221, -79.45881564379303),
                        (43.643189591230595, -79.45809144735901),
                        (43.64157515490247, -79.45647675753204),
                        (43.64137522769748, -79.45772130251495)],
    "Allotment Gardens": [(43.64754209338827, -79.4632949328479),
                          (43.648391, -79.461650),
                          (43.647938994839635, -79.46088094473451),
                          (43.646871, -79.461734),
                          (43.646778, -79.461863),
                          (43.646821307824176, -79.46209062100023)],
    "Grenadier Pond (South)": [(43.63797151053671, -79.46663696528041),
                               (43.63937009572973, -79.46177680254543),
                               (43.64132767209934, -79.46288187265957),
                               (43.64216716845231, -79.46604687929714),
                               (43.641050101938596, -79.46822483301723)],
    "Grenadier Pond Marsh (North)": [(43.648645, -79.471064),
                                     (43.648692, -79.470466),
                                     (43.646844, -79.469437),
                                     (43.646099, -79.469008),
                                     (43.646037, -79.470680),
                                     (43.648024, -79.471152)],
    "Hawk Hill": [(43.647822, -79.467078),
                  (43.648133, -79.465363),
                  (43.646176, -79.464848),
                  (43.645990, -79.466864)],
    "Behind Greenhouse": [(43.645093, -79.460829),
                          (43.644977, -79.459501),
                          (43.643160, -79.458836),
                          (43.642850, -79.460380)],

}

location_colors = {
    "Howard and Ridout Pond": "red",
    "Bloor Street Savannah": "orange",
    "Behind Nature Centre": "green",
    "All Star Cafe": "blue",
    "Lower Duck Pond": "black",
    "Upper Duck Pond": "purple",
    "Allotment Gardens": "gray",
    "Grenadier Pond (South)": "white",
    "Grenadier Pond Marsh (North)": "#33F204",
    "Hawk Hill": "#04D4F2",
    "Behind Greenhouse": "yellow"

}


# Create a map based on the selected species
def create_park_area_map():

    # Create the map object and set some options
    m = Map(
        center=(43.64632654828124, -79.46253966380962),
        zoom=14,
        scroll_wheel_zoom=True
    )

    m.layout.width = '100%'
    m.layout.height = '400px'
    m.add_control(FullScreenControl())

    for key in locations:
        polygon = Polygon(
            locations=[locations[key]],
            color=location_colors[key],
            fill_opacity=0.5
        )
        m.add_layer(polygon)

    # Save the map for the checklist
    m.layout.width = '100%'
    m.layout.height = '500px'
    m.save(config.dir_path + '\\maps\\park_areas_map.html',
           title='Park Areas Map')


create_park_area_map()
