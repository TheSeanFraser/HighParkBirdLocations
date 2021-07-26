var path = 'https://theseanfraser.github.io/HighParkBirdLocations/maps/species/';
var selectSpeciesButton = document.getElementById("selectSpeciesButton");


selectSpeciesButton.onclick = function() {
	console.log("Button clicked");
	var speciesMapiFrame = document.getElementById("species_map");
	var speciesName = document.getElementById("speciesSelector").value;
	//var mapTitle = document.getElementById("mapTitle");
    var source = path + speciesName + '.html';
	console.log(source);
	//mapTitle.innerHTML("Map of " + speciesName +  " seen since July 2021:");
    speciesMapiFrame.setAttribute('src', source);
};


