/*jslint browser: true, devel: true*/
/*eslint-env browser*/
/*global $, jQuery, alert*/

var weatherAPIkey = "169a3303c8d5deae771b019a6c78f890";

// Define a starting hour for the table
var startHour = 8;

// Define all of the IDs for the table
var T_WIND_SPEED_IDS = ["t_ws8", "t_ws9", "t_ws10", "t_ws11", "t_ws12", "t_ws1", "t_ws2", "t_ws3", "t_ws4", "t_ws5"],
	T_WIND_DIRECTION_IDS = ["t_wd8", "t_wd9", "t_wd10", "t_wd11", "t_wd12", "t_wd1", "t_wd2", "t_wd3", "t_wd4", "t_wd5"],
	T_TEMP_IDS = ["t_t8", "t_t9", "t_t10", "t_t11", "t_t12", "t_t1", "t_t2", "t_t3", "t_t4", "t_t5"],
	T_HUMIDITY_IDS = ["t_h8", "t_h9", "t_h10", "t_h11", "t_h12", "t_h1", "t_h2", "t_h3", "t_h4", "t_h5"],
	T_PRES_IDS = ["t_pres8", "t_pres9", "t_pres10", "t_pres11", "t_pres12", "t_pres1", "t_pres2", "t_pres3", "t_pres4", "t_pres5"],
	T_CLOUD_COVER_IDS = ["t_c8", "t_c9", "t_c10", "t_c11", "t_c12", "t_c1", "t_c2", "t_c3", "t_c4", "t_c5"],
	T_VISIBILITY_IDS = ["t_v8", "t_v9", "t_v10", "t_v11", "t_v12", "t_v1", "t_v2", "t_v3", "t_v4", "t_v5"],
	T_PREC_IDS = ["t_prec8", "t_prec9", "t_prec10", "t_prec11", "t_prec12", "t_prec1", "t_prec2", "t_prec3", "t_prec4", "t_prec5"],
	Y_WIND_SPEED_IDS = ["y_ws8", "y_ws9", "y_ws10", "y_ws11", "y_ws12", "y_ws1", "y_ws2", "y_ws3", "y_ws4", "y_ws5"],
	Y_WIND_DIRECTION_IDS = ["y_wd8", "y_wd9", "y_wd10", "y_wd11", "y_wd12", "y_wd1", "y_wd2", "y_wd3", "y_wd4", "y_wd5"],
	Y_TEMP_IDS = ["y_t8", "y_t9", "y_t10", "y_t11", "y_t12", "y_t1", "y_t2", "y_t3", "y_t4", "y_t5"],
	Y_HUMIDITY_IDS = ["y_h8", "y_h9", "y_h10", "y_h11", "y_h12", "y_h1", "y_h2", "y_h3", "y_h4", "y_h5"],
	Y_PRES_IDS = ["y_pres8", "y_pres9", "y_pres10", "y_pres11", "y_pres12", "y_pres1", "y_pres2", "y_pres3", "y_pres4", "y_pres5"],
	Y_CLOUD_COVER_IDS = ["y_c8", "y_c9", "y_c10", "y_c11", "y_c12", "y_c1", "y_c2", "y_c3", "y_c4", "y_c5"],
	Y_VISIBILITY_IDS = ["y_v8", "y_v9", "y_v10", "y_v11", "y_v12", "y_v1", "y_v2", "y_v3", "y_v4", "y_v5"],
	Y_PREC_IDS = ["y_prec8", "y_prec9", "y_prec10", "y_prec11", "y_prec12", "y_prec1", "y_prec2", "y_prec3", "y_prec4", "y_prec5"];
	


// Get today's weather data from OpenWeather API
function getWeatherData(){
	console.log("Getting weather data...");
	
	// Get the current UTC time
	var todayMS = Math.floor(Date.now() / 1000) - 100;
	var today = new Date(0);
	today.setUTCSeconds(todayMS);
	var yesterdayMS = todayMS - 86400;
	var yesterday = new Date(0);
	yesterday.setUTCSeconds(yesterdayMS);
	
	console.log(today.toDateString());
	console.log(yesterday.toDateString());

	
	$.ajaxSetup({
    	async: false
	});
	
	var urlWithAPIkey = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=43.646372&lon=-79.465778&dt=" + todayMS + "&appid=" + weatherAPIkey;
	$.getJSON(urlWithAPIkey, function(data) {
		// Log data to display for production
		console.log(data);
		applyTodaysData(data);
		document.getElementById("t_weather").innerHTML = "Weather for today (" + today.toDateString() + "):";
	});
	
	var urlWithAPIkey = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=43.646372&lon=-79.465778&dt=" + yesterdayMS + "&appid=" + weatherAPIkey;
	$.getJSON(urlWithAPIkey, function(data) {
		// Log data to display for production
		console.log(data);
		applyYesterdaysData(data);
		document.getElementById("y_weather").innerHTML = "Weather for yesterday (" + yesterday.toDateString() + "):";
	});
	
}

// Master function to apply data to today's table
function applyTodaysData(data){
	applyTWindSpeed(data);
	applyTWindDirection(data);
	applyTTemp(data);
	applyTHumidity(data);
	applyTPressure(data);
	applyTCloudCover(data);
	applyTVisibility(data);
	applyTPrecipitation(data);
}

// Master function to apply data to yesterday's table
function applyYesterdaysData(data){
	applyYWindSpeed(data);
	applyYWindDirection(data);
	applyYTemp(data);
	applyYHumidity(data);
	applyYPressure(data);
	applyYCloudCover(data);
	applyYVisibility(data);
	applyYPrecipitation(data);
}

// Applies the wind speed for today to the table
// Must convert m/S to Beaufort Scale first
function applyTWindSpeed(data) {
	for (let i = startHour; i < startHour + 10; i++) {
		if (data.hourly[i] !== undefined){
			var tableRowIndex = i - startHour;
			var curWindSpeed = data.hourly[i].wind_speed;
			var BeaufortWindSpeed = 0;
			
			// Converts the wind speed in metres per second to Beaufort Scale
			if (curWindSpeed < 0.3){
				BeaufortWindSpeed = 0;
			} else if (curWindSpeed < 1.5) {
				BeaufortWindSpeed = 1;
			} else if (curWindSpeed < 3.3) {
				BeaufortWindSpeed = 2;
			} else if (curWindSpeed < 5.4) {
				BeaufortWindSpeed = 3;
			} else if (curWindSpeed < 7.9) {
				BeaufortWindSpeed = 4;
			} else if (curWindSpeed < 10.7) {
				BeaufortWindSpeed = 5;
			} else if (curWindSpeed < 13.8) {
				BeaufortWindSpeed = 6;
			} else if (curWindSpeed < 17.1) {
				BeaufortWindSpeed = 7;
			} else {
				BeaufortWindSpeed = 8;
			}
			
			document.getElementById(T_WIND_SPEED_IDS[tableRowIndex]).innerHTML = BeaufortWindSpeed;
		}	
	}
}

// Applies the wind direction to today's table
// Converts degrees to cardinal directions
function applyTWindDirection(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		if (data.hourly[i] !== undefined) {
			var curWindDeg = data.hourly[i].wind_deg;
			var WindDirStr = "NW";
			
			if ( (348.75 <= curWindDeg && curWindDeg <= 360) || (0 <= curWindDeg && curWindDeg <= 11.25)) {
				WindDirStr = "N";
			} else if ( 11.25 <= curWindDeg && curWindDeg < 33.75 ) {
				WindDirStr = "NNE";
			} else if ( 33.75 <= curWindDeg && curWindDeg < 56.25 ) {
				WindDirStr = "NE";
			} else if ( 56.25 <= curWindDeg && curWindDeg < 78.75 ) {
				WindDirStr = "ENE";
			} else if ( 78.75 <= curWindDeg && curWindDeg < 101.25 ) {
				WindDirStr = "E";
			} else if ( 101.25 <= curWindDeg && curWindDeg < 123.75 ) {
				WindDirStr = "ESE";
			} else if ( 123.75 <= curWindDeg && curWindDeg < 146.25 ) {
				WindDirStr = "SE";
			} else if ( 146.25 <= curWindDeg && curWindDeg < 168.75 ) {
				WindDirStr = "SSE";
			} else if ( 168.75 <= curWindDeg && curWindDeg < 191.25 ) {
				WindDirStr = "S";
			} else if ( 191.25 <= curWindDeg && curWindDeg < 213.75 ) {
				WindDirStr = "SSW";
			} else if ( 213.75 <= curWindDeg && curWindDeg < 236.25 ) {
				WindDirStr = "SW";
			} else if ( 236.25 <= curWindDeg && curWindDeg < 258.75 ) {
				WindDirStr = "WSW";
			} else if ( 258.75 <= curWindDeg && curWindDeg < 281.25 ) {
				WindDirStr = "W";
			} else if ( 281.25 <= curWindDeg && curWindDeg < 303.75 ) {
				WindDirStr = "WNW";
			} else if ( 303.75 <= curWindDeg && curWindDeg < 326.25 ) {
				WindDirStr = "NW";
			} else {
				WindDirStr = "NNW";
			}
					
			document.getElementById(T_WIND_DIRECTION_IDS[tableRowIndex]).innerHTML = WindDirStr;
		}
	}
}

// Applies the temperature for today to the table
// Must convert Kelvin to Celcius first
function applyTTemp(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		if (data.hourly[i] !== undefined){
			var curTemp = data.hourly[i].temp;
			var CelciusTemp = Math.floor(data.hourly[i].temp - 273.15);

			document.getElementById(T_TEMP_IDS[tableRowIndex]).innerHTML = CelciusTemp;
		}
	}
}

// Applies the humidity to today's table
function applyTHumidity(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		if (data.hourly[i] !== undefined){
			var curHumidity = data.hourly[i].humidity;

			document.getElementById(T_HUMIDITY_IDS[tableRowIndex]).innerHTML = curHumidity;
		}
	}
}

// Applies the pressure to today's table
function applyTPressure(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		if (data.hourly[i] !== undefined){
			var curPressure = data.hourly[i].pressure;

			document.getElementById(T_PRES_IDS[tableRowIndex]).innerHTML = curPressure;
		}
	}
}

// Applies the cloud cover to today's table
function applyTCloudCover(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		if (data.hourly[i] !== undefined){
			var curClouds = data.hourly[i].clouds;

			document.getElementById(T_CLOUD_COVER_IDS[tableRowIndex]).innerHTML = curClouds;
		}
	}
}

// Applies the visibility to today's table
// Coverts m to km
function applyTVisibility(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		if (data.hourly[i] !== undefined){
			var curVisibility = data.hourly[i].visibility;
			var convertedVisibility = curVisibility / 1000;

			document.getElementById(T_VISIBILITY_IDS[tableRowIndex]).innerHTML = convertedVisibility;
		}
	}
}

// Applies the precipitation to today's table
// Must convert type to numerical value
function applyTPrecipitation(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		if (data.hourly[i] !== undefined){
			var curPrec = data.hourly[i].weather[0].main;
			var convertedPrec = 0;
			
			if (curPrec == "Haze" || curPrec == "Fog") {
				convertedPrec = 1;
			} else if (curPrec == "Drizzle") {
				convertedPrec = 2;
			} else if (curPrec == "Rain") {
				convertedPrec = 3;
			} else if (curPrec == "Thunderstorm") {
				convertedPrec = 4;
			} else if (curPrec == "Snow") {
				convertedPrec = 5;
			} else if (curPrec == "Dust" || curPrec == "Sand") {
				convertedPrec = 6;
			}

			document.getElementById(T_PREC_IDS[tableRowIndex]).innerHTML = convertedPrec;
		}
	}
}

// Applies the wind speed for yesterday to the table
// Must convert m/S to Beaufort Scale first
function applyYWindSpeed(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		var curWindSpeed = data.hourly[i].wind_speed;
		var BeaufortWindSpeed = 0;
		
		if (curWindSpeed < 0.3){
			BeaufortWindSpeed = 0;
		} else if (curWindSpeed < 1.5) {
			BeaufortWindSpeed = 1;
		} else if (curWindSpeed < 3.3) {
			BeaufortWindSpeed = 2;
		} else if (curWindSpeed < 5.4) {
			BeaufortWindSpeed = 3;
		} else if (curWindSpeed < 7.9) {
			BeaufortWindSpeed = 4;
		} else if (curWindSpeed < 10.7) {
			BeaufortWindSpeed = 5;
		} else if (curWindSpeed < 13.8) {
			BeaufortWindSpeed = 6;
		} else if (curWindSpeed < 17.1) {
			BeaufortWindSpeed = 7;
		} else {
			BeaufortWindSpeed = 8;
		}
		
		document.getElementById(Y_WIND_SPEED_IDS[tableRowIndex]).innerHTML = BeaufortWindSpeed;
	}
}

// Applies the wind direction to yesterday's table
// Converts degrees to cardinal directions
function applyYWindDirection(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		var curWindDeg = data.hourly[i].wind_deg;
		var WindDirStr = "NW";
		
		if ( (348.75 <= curWindDeg && curWindDeg <= 360) || (0 <= curWindDeg && curWindDeg <= 11.25)) {
			WindDirStr = "N";
		} else if ( 11.25 <= curWindDeg && curWindDeg < 33.75 ) {
			WindDirStr = "NNE";
		} else if ( 33.75 <= curWindDeg && curWindDeg < 56.25 ) {
			WindDirStr = "NE";
		} else if ( 56.25 <= curWindDeg && curWindDeg < 78.75 ) {
			WindDirStr = "ENE";
		} else if ( 78.75 <= curWindDeg && curWindDeg < 101.25 ) {
			WindDirStr = "E";
		} else if ( 101.25 <= curWindDeg && curWindDeg < 123.75 ) {
			WindDirStr = "ESE";
		} else if ( 123.75 <= curWindDeg && curWindDeg < 146.25 ) {
			WindDirStr = "SE";
		} else if ( 146.25 <= curWindDeg && curWindDeg < 168.75 ) {
			WindDirStr = "SSE";
		} else if ( 168.75 <= curWindDeg && curWindDeg < 191.25 ) {
			WindDirStr = "S";
		} else if ( 191.25 <= curWindDeg && curWindDeg < 213.75 ) {
			WindDirStr = "SSW";
		} else if ( 213.75 <= curWindDeg && curWindDeg < 236.25 ) {
			WindDirStr = "SW";
		} else if ( 236.25 <= curWindDeg && curWindDeg < 258.75 ) {
			WindDirStr = "WSW";
		} else if ( 258.75 <= curWindDeg && curWindDeg < 281.25 ) {
			WindDirStr = "W";
		} else if ( 281.25 <= curWindDeg && curWindDeg < 303.75 ) {
			WindDirStr = "WNW";
		} else if ( 303.75 <= curWindDeg && curWindDeg < 326.25 ) {
			WindDirStr = "NW";
		} else {
			WindDirStr = "NNW";
		}
				
		document.getElementById(Y_WIND_DIRECTION_IDS[tableRowIndex]).innerHTML = WindDirStr;
	}
}

// Applies the temperature for yesterday to the table
// Must convert Kelvin to Celcius first
function applyYTemp(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		var curTemp = data.hourly[i].temp;
		var CelciusTemp = Math.floor(data.hourly[i].temp - 273.15);

		document.getElementById(Y_TEMP_IDS[tableRowIndex]).innerHTML = CelciusTemp;
	}
}

// Applies the humidity to yesterday's table
function applyYHumidity(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		var curHumidity = data.hourly[i].humidity;

		document.getElementById(Y_HUMIDITY_IDS[tableRowIndex]).innerHTML = curHumidity;
	}
}

// Applies the pressure to yesterday's table
function applyYPressure(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		var curPressure = data.hourly[i].pressure;

		document.getElementById(Y_PRES_IDS[tableRowIndex]).innerHTML = curPressure;
	}
}

// Applies the cloud cover to yesterday's table
function applyYCloudCover(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		var curClouds = data.hourly[i].clouds;

		document.getElementById(Y_CLOUD_COVER_IDS[tableRowIndex]).innerHTML = curClouds;
	}
}

// Applies the visibility to yesterday's table
// Coverts m to km
function applyYVisibility(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		var curVisibility = data.hourly[i].visibility;
		var convertedVisibility = curVisibility / 1000;

		document.getElementById(Y_VISIBILITY_IDS[tableRowIndex]).innerHTML = convertedVisibility;
	}
}

// Applies the precipitation to yesterday's table
// Must convert type to numerical value
function applyYPrecipitation(data){
	for (let i = startHour; i < startHour + 10; i++) {
		var tableRowIndex = i - startHour;
		var curPrec = data.hourly[i].weather[0].main;
		var convertedPrec = 0;
		
		if (curPrec == "Haze" || curPrec == "Fog") {
			convertedPrec = 1;
		} else if (curPrec == "Drizzle") {
			convertedPrec = 2;
		} else if (curPrec == "Rain") {
			convertedPrec = 3;
		} else if (curPrec == "Thunderstorm") {
			convertedPrec = 4;
		} else if (curPrec == "Snow") {
			convertedPrec = 5;
		} else if (curPrec == "Dust" || curPrec == "Sand") {
			convertedPrec = 6;
		}

		document.getElementById(Y_PREC_IDS[tableRowIndex]).innerHTML = convertedPrec;
	}
}


getWeatherData();