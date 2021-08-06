# High Park Bird Locations

A Python application to record the GPS locations of birds in Toronto's High Park.

After importing the eBird checklist, a map of High Park is displayed with the list of species beside it.
Clicking the spot on the map where a bird of the selected species was observed records the location. 
Using *Affine Transformation*, a GPS coordinate is calculated from the pixel coordinates of the selected spot. 
Once the data collection is complete, the results get sent to an SQL server for storage.

A map is created for each checklist, to show where each bird was seen during that trip to the park.
The locations from each species are used to generate a map of total observations, as well as charts to analyze the patterns in the observations.


[The maps and charts can be viewed on the GitHub Pages site here.](theseanfraser.github.io/HighParkBirdLocations/)
