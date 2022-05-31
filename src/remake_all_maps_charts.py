import checklist_charts
import checklist_maps
import species_charts
import species_maps
import all_birds_map
import species_season_maps


# Quick and easy way to remake all media
def remake_all():
    # Remake all checklist maps and charts
    print("Starting checklist media...")
    checklist_maps.remake_all_checklist_maps()
    print("Checklist maps complete, next are charts...")
    # Have not fully implemented species charts yet
    # checklist_charts.make_all_checklist_charts()
    print("==========================================================")
    print("Checklist media completed!")
    print("==========================================================")

    # Remake all species maps and charts
    print("Starting species media...")
    species_maps.map_all_species()
    print("Species maps complete, next are charts...")
    species_charts.make_all_species_charts()
    # Have not fully implemented season maps yet
    # species_season_maps.map_all_species()
    print("==========================================================")
    print("Species media completed!")
    print("==========================================================")

    # Remake full park heatmap
    print("Starting full map...")
    all_birds_map.createMap()
    print("==========================================================")
    print("Full map completed!")
    print("======== Done! ========")



remake_all()
