var dateListResponse;

fetch('https://theseanfraser.github.io/HighParkBirdLocations/maps/checklists/checklistList.txt')
	.then(response => response.text())
    .then(text=> dateListResponse = text)
    .then((response) => {
        this.updateSelectorList();
 		})
    .then(text => console.log(text));


function updateSelectorList()
{
    var selector = document.getElementById("dateSelector");

	var dateList = dateListResponse.split("\n");

     for(var i = 0; i < dateList.length - 1; i++) {
         var opt = dateList[i];
         var el = document.createElement("option");
         el.textContent = opt;
         el.value = opt;
         selector.appendChild(el);
     }
}



