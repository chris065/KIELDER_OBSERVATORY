#!/usr/bin/python


#############################################
# PYTHON SCRIPT TO WEB SCRAPE AURORAL IMAGES
# AND SOLAR WIND DATA FROM VARIOUS WEBSITES
#############################################


#############################################
# Import necessary modules:
#############################################

# Current system times:
from datetime import datetime
import ephem as e

# Julian dates:
from astropy.time import Time

# Parsing information and images from HTML websites:
from bs4 import BeautifulSoup
import urllib
import requests

# Manipulating (crop, resize, save etc.) images:
from PIL import Image

# Manipulating strings:
import string

darkStyleSheet = ""
lightStyleSheet = ""
styleSheet = ""


#############################################
# Get live auroral oval from Space Weather
# website:
#############################################

#Checks whether the sun is below the horizon or not
kobs = e.Observer()
kobs.lon, kobs.lat = '-2.5881', '55.2330'
kobs.date = datetime.now()

#Compute Sun Altitude
sol = e.Sun()
sol.compute(kobs)

# Return First digit of Sun's altitude
alt = int(str(sol.alt).split(':')[0])

if (alt < -6):
    #read the contents of the dark style sheet for night time
    darkStyleSheet = open("Aurora_Style_Dark.css", "r").read()
    styleSheet = darkStyleSheet
else:
    #read the contents of the light for day time style sheet
    lightStyleSheet = open("Aurora_Style_Light.css", "r").read()
    styleSheet = lightStyleSheet
#End of checking whether or not the sun is below the horizon

# Needs updating every 5 minutes

# Create URL for auroral data (with Europe-centric loation):
auroraUrl = "http://services.swpc.noaa.gov/images/aurora-forecast-northern-hemisphere.jpg"

# Get auroral oval image:
spaceWeatherImage = urllib.request.urlretrieve(auroraUrl, "Aurora_Map.png")
spaceWeatherImage = Image.open("Aurora_Map.png")

# Resize image:
spaceWeatherSize = 750, 750
spaceWeatherImage = spaceWeatherImage.resize(spaceWeatherSize, Image.ANTIALIAS)

# Save revised image:
spaceWeatherImage.save("IMG/Aurora_Map.png")

# Create URL for space weather data:
spaceWeatherUrl = "http://www.spaceweather.com/"

# Get data from various Space Weather website tables:
soup = BeautifulSoup(urllib.request.urlopen(spaceWeatherUrl).read(), "html.parser")
ranProperly = True

# Get solar wind, sunspot and magnetic field data:
sunData = soup.findAll('b')

# Get solar wind data:
solarWindSpeed = str(sunData[1])
solarWindSpeed = ''.join([n for n in solarWindSpeed if n in '1234567890.'])
solarWindDensity = str(sunData[2])
solarWindDensity = ''.join([n for n in solarWindDensity if n in '1234567890.'])

# Get sunspot data:
sunSpotNumber = str(sunData[6])
sunSpotNumber = ''.join([n for n in sunSpotNumber if n in '1234567890.'])

# Get magnetic field data:
bTotal = str(sunData[11])
bTotal = ''.join([n for n in bTotal if n in '1234567890.'])
bZ = str(sunData[12])
bZ = ''.join([n for n in bZ if n in '1234567890.'])
bDirection = str(sunData[13])
bDirection.replace('<b>', '')
bDirection.replace('\n', '')
bDirection.replace('</b>', '')
# Ensure text has capital letters:
if 'north' in bDirection:
  bDirection = ' North'
  bColour = '<font color = "green">'
if 'south' in bDirection:
  bDirection = ' South'
  bColour = '<font color = "red">'

# Get Kp index data:
kIndexData = soup.findAll('strong')

# Get current planetary index data:
kNow = str(kIndexData[1])
kNow = ''.join([n for n in kNow if n in '1234567890.'])

# Get predicted 24hr maximum planetary index data:
kMax = str(kIndexData[2])
kMax = ''.join([n for n in kMax if n in '1234567890.'])

# Specify present conditions:
if kNow == '0' or '1' or '2':
  kNowDescription = ' (Quiet)'
  kNowColour = '<font color = "green">'
elif kNow == '3' or '4':
  kNowDescription = ' (Unsettled)'
  kNowColour = '<font color = "orange">'
else:
  kNowDescription = ' (Storm)'
  kNowColour = '<font color = "red">'

# Specify predicted conditions:
if kMax == '0' or '1' or '2':
  kMaxDescription = ' (Quiet)'
  kMaxColour = '<font color = "green">'
elif kMax == '3' or '4':
  kMaxDescription = ' (Unsettled)'
  kMaxColour = '<font color = "orange">'
else:
  kMaxDescription = ' (Storm)'
  kMaxColour = '<font color = "red">'


#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open("Aurora.html", 'w+')

# Write HTML href text to first line of new text HTML file:
auroraHtml = '''<!DOCTYPE html>
<html>
<title>
The Aurora Now
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
    }, 6*60000);
</script>

<div>
<b> The Aurora Now
</b>
</div>

<div class = "auroralOval">
	<img src = "IMG/Aurora_Map.png">
	<div class = "key">Current Auroral Oval</div>
</div>

<div class = "credits">Credit: National Oceanic and Atmospheric Administration</div>

<table class = "spaceWeatherTable">
	<tr>
		<th colspan = 2>Solar Wind and Magnetic Field<br></th>
	</tr>
	<tr>
		<td id="td01">Solar Wind Speed (kph)</td>
		<td id="td01"><i>''' + solarWindSpeed + '''</i></td>
	</tr>
	<tr>
		<td id="td02">Solar Wind Density (protons/cm<sup>3</sup>)</td>
		<td id="td02"><i>''' + solarWindDensity + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Number of Sunspots</td>
		<td id="td01"><i>''' + sunSpotNumber + '''</i></td>
	</tr>
	<tr>
		<td id="td02">B<sub>total</sub> (nano Tesla)</td>
		<td id="td02"><i>''' + bTotal + '''</i></td>
	</tr>
	<tr>
		<td id="td01">B<sub>z</sub> (nano Tesla)</td>
		<td id="td01"><i>''' + bZ + bColour + bDirection + '''</font></i></td>
	</tr>
	<tr>
		<td id="td02">K-Index Now (0-9)</td>
		<td id="td02"><i>''' + kNow + kNowColour + kNowDescription + '''</font></i></td>
	</tr>
	<tr>
		<td id="td01">24hr Maximum K-Index (0-9)</td>
		<td id="td01"><i>''' + kMax + kMaxColour + kMaxDescription + '''</font></i></td>
	</tr>
</table>

<div class = "kielderLogo">
	<img src = "IMG/Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(auroraHtml)

# Close text file:
f.close()
