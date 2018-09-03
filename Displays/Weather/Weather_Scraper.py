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
from urllib2 import urlopen
import urllib
import requests

# Manipulating (crop, resize, save etc.) images:
from PIL import Image

# Manipulating strings:
import string

# Getting weather data:
import pyowm


#############################################
# Get live satellite cloud IR map from
# Sat24 website (UK and time specific):
#############################################

# Needs updating every 5 minutes

# Create URL for infrared satellite weather image:
satUrl = "http://api.sat24.com/crop?type=infraPolair&lat=55.233&lon=-2.5881&width=800&height=800&zoom=0.60&continent=eu"

# Get satellite weather image:
satWeatherImage = urllib.urlretrieve(satUrl, "Sat_Weather.png")
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

# Set API key for OpenWeatherMap.com:
owm = pyowm.OWM('0733a9c5266d2113bb9c19114c0c9cd8')

# Set Kielder Observatory location:
latitude = 55.2305486
longitude = -2.6054411
altitude = 370

# Create forecast location:
obsWeather = owm.weather_at_coords(latitude, longitude)

# Get time of weather:
kielderWeather = obsWeather.get_weather()

# Get time of weather report:
weatherTimeStamp = kielderWeather.get_reference_time(timeformat = 'iso')
weatherTimeStamp = weatherTimeStamp[11:19]
# Get cloud coverage:
weatherClouds = kielderWeather.get_clouds()
weatherClouds = str(weatherClouds) + '%'
# Get wind direction and speed:
weatherWind = kielderWeather.get_wind()
weatherWindSpeed = str(weatherWind['speed']) + 'mph'
weatherWindDirection = str(weatherWind['deg'])
# Get humidity:
weatherHumidity = kielderWeather.get_humidity()
weatherHumidity = str(weatherHumidity) + '%'
# Get temperature in C:
weatherTempC = kielderWeather.get_temperature(unit = 'celsius')
weatherTempC = str(weatherTempC['temp'])
# Get temperature in F:
weatherTempF = kielderWeather.get_temperature(unit = 'fahrenheit')
weatherTempF = str(weatherTempF['temp'])
# Get air pressure in milliBars:
weatherPressure = kielderWeather.get_pressure()
weatherPressure = str(weatherPressure['press'])


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

body {
	background-color: #000000;
}

b {
	color: #FFFFFF;
	font-size: 60px;
	font-weight: bold;
	font-family: Calibri;
	position: absolute;
	left: 40px;
	top: 40px;
}

table.weatherTable {
	position: absolute;
	top: 140px;
	right: 40px;
	width: 1118px;
	height: 678px;
	border: 1px solid #FFFFFF;
	border-collapse: collapse;
}

th {
	color: #FFFFFF;
	background-color: #78BE20;
	padding: 10px;
	font-size: 40px;
	text-align: center;
	font-weight: bold;
	font-family: Calibri;
	border: 1px solid #FFFFFF;
	border-collapse: collapse;
}

td#td01 {
	color: #FFFFFF;
	padding: 10px;
	background-color: #777777;
	font-size: 40px;
	text-align: left;
	font-family: Calibri;
	border: 1px solid #FFFFFF;
	border-collapse: collapse;
}

td#td02 {
	color: #000000;
	padding: 10px;
	background-color: #FFFFFF;
	font-size: 40px;
	text-align: left;
	font-family: Calibri;
	border: 1px solid #777777;
	border-collapse: collapse;
}

div.satCloud {
	position: absolute;
	top: 140px;
	left: 40px;
}

div.kielderLogo {
	position: absolute;
	top: 890px;
	right: 40px;
}

div.key {
	color: #78BE20;
	text-align: center;
	font-size: 40px;
	font-weight: bold;
	font-family: Calibri;
	padding: 10px;
}

div.credits {
	position: relative;
	top: 990px;
	left: center;
	color: #FFFFFF;
	text-align: center;
	font-size: 20px;
	font-weight: bold;
	font-family: Calibri;
}

</style>
</head>

<body>

<div>
<b>The Kielder Weather Now
</b>
</div>

<div class = "satCloud">
	<img src = "C:\Users\Kielder Observatory\Desktop\Kielder_Displays\Weather\Sat_Weather.png">
	<div class = "key">Live Infra-red Cloud Map</div>
</div>

<div class = "credits">Credit: EUMETSAT &#38 Open Weather Map</div>

<table class = "weatherTable">
	<tr>
		<th>Kielder Live Weather</th>
	</tr>
	<tr>
		<td id="td01">Temperature (&#176C)/(&#176F)</td>
		<td id="td01"><i>''' + str(weatherTempC) + '''&#176C/''' + str(weatherTempF) + '''&#176F</i></td>
	</tr>
    	<tr>
		<td id="td02">Humidity (%)</td>
		<td id="td02"><i>''' + str(weatherHumidity) + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Wind Speed/Direction (mph)/(&#176)</td>
		<td id="td01"><i>''' + str(weatherWindSpeed) + '''/''' + str(weatherWindDirection) + '''&#176</i></td>
	</tr>
	<tr>
		<td id="td02">Cloud Cover (%)</td>
		<td id="td02"><i>''' + str(weatherClouds) + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Pressure (mBar)</td>
		<td id="td01"><i>''' + str(weatherPressure) + '''mBar</i></td>
	</tr>

</table>

<div class = "kielderLogo">
	<img src = "C:\Users\Kielder Observatory\Desktop\Kielder_Displays\Weather\Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(weatherHtml)

# Close text file:
f.close()
