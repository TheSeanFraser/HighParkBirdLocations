var path = 'https://theseanfraser.github.io/HighParkBirdLocations/maps/species/';
var selectSpeciesButton = document.getElementById("selectSpeciesButton");


selectSpeciesButton.onclick = function() {
	console.log("Button clicked");
	var speciesMapiFrame = document.getElementById("species_map");
	var speciesName = document.getElementById("speciesSelector").value;
	
    var source = path + speciesName + '.html';
	console.log(source);
	var mapTitle = document.getElementById("mapTitle");
	mapTitle.innerHTML = "Map of " + speciesName +  " observations since July 2021:";
	
    speciesMapiFrame.setAttribute('src', source);
};


// Checks and deals with hashtag fragment in link
function fragmentSpeciesMap(){
	if(window.location.hash) {
		console.log("HASH FOUND");
		var hashSpeciesName = decodeURI(window.location.hash.split("#")[1]);
		var speciesMapiFrame = document.getElementById("species_map");
		var mapTitle = document.getElementById("mapTitle");
		var source = path + hashSpeciesName + '.html';
		
		console.log(source);
		mapTitle.innerHTML = "Map of " + hashSpeciesName +  " observations since July 2021:";
		document.getElementById("speciesSelector").value = hashSpeciesName;
		speciesMapiFrame.setAttribute('src', source);
		
	} else {
		console.log("NO HASH");
	}
}

fragmentSpeciesMap();
