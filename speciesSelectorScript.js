var speciesListResponse;

fetch('https://theseanfraser.github.io/HighParkBirdLocations/maps/species/speciesList.txt')
	.then(response => response.text())
    .then(text=> speciesListResponse = text)
    .then((response) => {
        this.updateSelectorList();
 		})
    .then(text => console.log(text));


function updateSelectorList()
{
    var selector = document.getElementById("speciesSelector");

	var speciesList = speciesListResponse.split("\n");

     for(var i = 0; i < speciesList.length; i++) {
         var opt = speciesList[i];
         var el = document.createElement("option");
         el.textContent = opt;
         el.value = opt;
         selector.appendChild(el);
     }
}



