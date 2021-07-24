// var path = "/maps/species/"
// // var speciesMap = $('#species_map');
// var speciesList = "test"

fetch('speciesList.txt')
    .then(response => response.text())
    .then(text => console.log(text));


function getText(){
    // read text from URL location
    var request = new XMLHttpRequest();
    request.open('GET', 'speciesList.txt', true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-Type');
            if (type.indexOf("text") !== 1) {
                return request.responseText;
            }
        }
    }
}

var speciesList = getText();
console.log(speciesList);







function loadNewMap(speciesName)
{
    var source = path + speciesName;
    speciesMap.attr('src', source);
}