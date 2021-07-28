var mapPath = 'https://theseanfraser.github.io/HighParkBirdLocations/maps/species/';
var chartPath = 'https://theseanfraser.github.io/HighParkBirdLocations/charts/species/';
var selectSpeciesButton = document.getElementById("selectSpeciesButton");


selectSpeciesButton.onclick = function() {
	console.log("Button clicked");
	// Get species name from selector
	var speciesName = document.getElementById("speciesSelector").value;
	// Set path variables based on species name
	var mapSource = mapPath + speciesName + '.html';
	var barChartSource = chartPath + speciesName + ' Bar Graph.html'
	var pieChartSource = chartPath + speciesName + ' Pie Graph.html'
	
	// Get page elements
	var mapTitle = document.getElementById("mapTitle");
	var speciesMapiFrame = document.getElementById("species_map");
	var barChartiFrame = document.getElementById("bar_chart");
	var pieChartiFrame = document.getElementById("pie_chart");

	// Set page elements to reflect selected species
	mapTitle.innerHTML = "Map of " + speciesName +  " observations since July 2021:";
    speciesMapiFrame.setAttribute('src', mapSource);
	barChartiFrame.setAttribute('src', barChartSource);
	pieChartiFrame.setAttribute('src', pieChartSource);
};


// Checks and deals with hashtag fragment in link
function fragmentSpeciesMap(){
	if(window.location.hash) {
		console.log("HASH FOUND");
		var hashSpeciesName = decodeURI(window.location.hash.split("#")[1]);
		var speciesMapiFrame = document.getElementById("species_map");
		var mapTitle = document.getElementById("mapTitle");
		var source = mapPath + hashSpeciesName + '.html';
		
		console.log(source);
		mapTitle.innerHTML = "Map of " + hashSpeciesName +  " observations since July 2021:";
		document.getElementById("speciesSelector").value = hashSpeciesName;
		speciesMapiFrame.setAttribute('src', source);
		
	} else {
		console.log("NO HASH");
	}
}

fragmentSpeciesMap();
