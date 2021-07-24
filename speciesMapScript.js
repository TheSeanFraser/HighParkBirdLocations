// var path = "/maps/species/"
// // var speciesMap = $('#species_map');
// var speciesList = "test"
var speciesList;

fetch('https://theseanfraser.github.io/HighParkBirdLocations/maps/species/speciesList.txt')
    .then(response => response.text())
    .then(text=> speciesList = text)
    .then(text => console.log(text));

console.log(speciesList + "TET");


function loadNewMap(speciesName)
{
    var source = path + speciesName;
    speciesMap.attr('src', source);
}