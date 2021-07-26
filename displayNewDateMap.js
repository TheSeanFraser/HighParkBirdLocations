var path = 'https://theseanfraser.github.io/HighParkBirdLocations/maps/checklists/';
var selectDateButton = document.getElementById("selectDateButton");


selectDateButton.onclick = function() {
	console.log("Button clicked");
	var dateMapiFrame = document.getElementById("date_map");
	var dateAndChecklistID = document.getElementById("dateSelector").value;
	//var mapTitle = document.getElementById("mapTitle");
	var checklistID = dateAndChecklistID.split(" ")[1];
    var source = path + checklistID + '.html';
	console.log(source);
	//mapTitle.innerHTML("Map of " + speciesName +  " seen since July 2021:");
    dateMapiFrame.setAttribute('src', source);
};


