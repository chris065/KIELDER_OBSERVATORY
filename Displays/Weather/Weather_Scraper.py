#!/usr/bin/python


#############################################
# PYTHON SCRIPT TO WEB SCRAPE IMAGES AND
# DATA FROM VARIOUS WEBSITES
#############################################


#############################################
# Import necessary modules:
#############################################

# Current system times:
from datetime import datetime

# Parsing information and images from HTML websites:
import urllib
import requests
import json, requests
import ephem as e

# Manipulating (crop, resize, save etc.) images:
from PIL import Image

# Manipulating strings:
import string

# Getting weather data:
weatherUrl = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/352090?res=3hourly&key=c5e68363-c162-4e94-8661-bc92d217577a"
getWeather = requests.get(weatherUrl)
weather = json.loads(getWeather.text)


#Setting the style sheet depending on the time of the day
styleSheet = ""
darkStyleSheet = ""
lightStyleSheet = ""

obsLat = '55.232302'
obsLon = '-2.616033'

obs = e.Observer()
obs.lat, obs.lon = obsLat, obsLon
obs.date = datetime.now()

sun = e.Sun()
sun.compute(obs)

alt = int(str(sun.alt).split(':')[0])

if alt < -6:
	darkStyleSheet = open("displayStyleDark.css", "r").read()
	styleSheet = darkStyleSheet
else:
	lightStyleSheet = open("displayStyleLight.css", "r").read()
	styleSheet = lightStyleSheet



#############################################
# Get live satellite cloud IR map from
# Sat24 website (UK and time specific):
#############################################

# Needs updating every 5 minutes

# Create URL for infrared satellite weather image:
satUrl = "http://api.sat24.com/crop?type=infraPolair&lat=55.233&lon=-2.5881&width=800&height=800&zoom=0.60&continent=eu"

# Get satellite weather image:
satWeatherImage = urllib.request.urlretrieve(satUrl, "Sat_Weather.png")
satWeatherImage = Image.open("Sat_Weather.png")

# Crop satellite image from 800 x 800 to remove ugly timestamps:
left = 60
top = 80
right = 740
bottom = 760
satWeatherImage = satWeatherImage.crop((left, top, right, bottom))

# Save revised image:
satWeatherImage.save("Sat_Weather.png")


#############################################
# Get weather update:
#############################################

weatherTemp = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['T'])

weatherTempC = str(weatherTemp)

weatherTempF = (int(weatherTemp) * 9/5 + 32)
weatherTempF = str(round(weatherTempF))

weatherHumidity = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['H'])
weatherHumidity = str(weatherHumidity) + "%"

weatherWindSpeed = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['S'])
weatherWindSpeed = str(weatherWindSpeed) + "mph"

weatherWindDirection = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['D'])
weatherWindDirection = str(weatherWindDirection)

weatherPrecip = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['Pp'])
weatherPrecip = str(weatherPrecip) + "%"

weatherPressure = ""








#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open('Weather.html', 'w+')

# Write HTML href text to first line of new text HTML file:
weatherHtml = '''<!DOCTYPE html>
<html>
<title>
The Kielder Weather Now
</title>
<head>

<style>
'''+styleSheet+'''
</style>

</head>

<body>

	<script>
		setTimeout(function()
		{
			location.reload();
		}, 6*60000)
	</script>

<div>
<b>The Kielder Weather Now
</b>
</div>

<div class = "satCloud">
	<img src = "Sat_Weather.png">
	<div class = "key">Live Infra-red Cloud Map</div>
</div>

<div class = "credits">Credit: EUMETSAT & Met Office</div>

<table class = "weatherTable">
	<tr>
		<th>Kielder Live Weather</th>
	</tr>
	<tr>
		<td id="td01">Temperature (&#176C) / (&#176F)</td>
		<td id="td01"><i>''' + str(weatherTempC) + '''&deg;C / ''' + str(weatherTempF) + '''&deg;F</i></td>
	</tr>
    	<tr>
		<td id="td02">Humidity (%)</td>
		<td id="td02"><i>''' + str(weatherHumidity) + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Wind Speed/Direction (mph) / Compass</td>
		<td id="td01"><i>''' + str(weatherWindSpeed) + ''' / ''' + str(weatherWindDirection) + '''</i></td>
	</tr>
	<tr>
		<td id="td02">Precipitation Probablity (%)</td>
		<td id="td02"><i>''' + str(weatherPrecip) + '''</i></td>
	</tr>

</table>

<div class = "kielderLogo">
	<img src = "Kielder_Logo.png">
</div>

</body>
</html>'''

f.write(weatherHtml)

# Close text file:
f.close()
