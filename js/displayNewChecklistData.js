var path = 'https://theseanfraser.github.io/HighParkBirdLocations/maps/checklists/';
var eBirdChecklistPath = 'https://ebird.org/checklist/'
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
	var eBirdChecklist = document.getElementById("eBirdChecklist");
	eBirdChecklist.setAttribute('href', eBirdChecklistPath + checklistID);
};


// Checks and deals with hashtag fragment in link
function fragmentChecklistMap(){
	if(window.location.hash) {
		console.log("HASH FOUND");
		var hashChecklistID = decodeURI(window.location.hash.split("#")[1]);
		var dateMapiFrame = document.getElementById("date_map");
		var mapTitle = document.getElementById("mapTitle");
		var source = path + hashChecklistID + '.html';
		
		console.log(source);
		mapTitle.innerHTML = "Map of checklist " + hashChecklistID +  " :";
		document.getElementById("dateSelector").value = hashChecklistID;
		dateMapiFrame.setAttribute('src', source);
		document.getElementById("eBirdChecklist").href = "https://ebird.org/checklist/" + hashChecklistID;
		
	} else {
		console.log("NO HASH");
	}
}

fragmentChecklistMap();
