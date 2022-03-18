var speciesListResponse;

fetch('https://theseanfraser.github.io/HighParkBirdLocations/maps/species/species.json')
    .then(response => response.text())
    .then(text=> speciesJSONResponse = text)
    .then((response) => {
        this.updateSelectorList();
        })
    .then(text => console.log(text));

function updateSelectorList()
{
    var selector = document.getElementById("speciesSelector");
    var speciesJSON = JSON.parse(speciesJSONResponse);

    // For each family, create an optgroup for the selector menu
    for(var family in speciesJSON) {
        var optGroup = document.createElement("optgroup");
        optGroup.label = family;

        for(var i = 0; i < speciesJSON[family].length; i++){
            curSpecies = speciesJSON[family][i];
            var el = document.createElement("option");
            el.textContent = curSpecies;
            el.value = curSpecies;
            optGroup.appendChild(el);
        }

        selector.appendChild(optGroup);
    }
}



