#!/usr/bin/python


#############################################
# PYTHON SCRIPT TO WEBSCRAPE SOLAR SYSTEM
# IMAGE AND DATA FROM HEAVENS-ABOVE.COM
#############################################


#############################################
# Import necessary modules:
#############################################

# Current system times:
from datetime import datetime

# Julian dates:
from astropy.time import Time

# RA and Dec coordinate conversion:
from astropy import units as u
from astropy.coordinates import SkyCoord

# Parsing information and images from HTML websites:
from bs4 import BeautifulSoup
import urllib
import requests

# Manipulating (crop, resize, save etc.) images:
from PIL import Image

# Manipulating strings:
import string

# Setting environment variables and/or deleting files:
import os

import ephem as e
import datetime

darkStyleSheet = ""
lightStyleSheet = ""
styleSheet = ""

kobs = e.Observer()
kobs.lon, kobs.lat = '-2.5881', '55.2330'
kobs.date = datetime.datetime.now()

#Compute Sun Altitude
sol = e.Sun()
sol.compute(kobs)

# Return First digit of Sun's altitude
alt = int(str(sol.alt).split(':')[0])

if (alt < -6):
    #read the contents of the dark style sheet for night time
    styleSheet = open("Planets_Style_Dark.css", "r").read()
else:
    #read the contents of the light for day time style sheet
    styleSheet = open("Planets_Style_Light.css", "r").read()


#############################################
# Determine the current Modified Julian Date:
#############################################

currentTime = datetime.datetime.now()
currentTime = Time(currentTime)
mjd = currentTime.mjd


#############################################
# Set longitude, latitude and altitude for
# Kielder observatory location:
#############################################

latitude = 55.2305486
longitude = -2.6054411
altitude = 370


#############################################
# Get live planetary position image from
# Heavens Above website (Kielder specific
# coordinates):
#############################################

# Only needs to be done daily upon startup

# Create URL for planetary position image
# (with correct current Modified Julian Date and at desired size):
planetsUrl = "http://www.heavens-above.com/SolarSystemPic.aspx?Epoch=" + str(mjd) + "&Width=500&Height=500&cul=en"

# Get solar system planetary positions image:
planetsImage = urllib.request.urlretrieve(planetsUrl, "Planets_Position.png")
planetsImage = Image.open("Planets_Position.png")

# Change blue background colour in image to pure black:
# Convert image to RGB colour space:
planetsImage = planetsImage.convert("RGBA")
# Read in pixel colours:
pixels = planetsImage.getdata()
newPixels = []
# Loop over pixels:
for pixel in pixels:
# Heavens Above background colour is 0,0,32 in RGB space
  if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 32:
    newPixels.append((0, 0, 0, 0))
  else:
    newPixels.append(pixel)
# Set new pixel array:
planetsImage.putdata(newPixels)

# Mask out 'Heavens Above' text in lower right corner:
# Set size of mask:
creditsMaskSize = 127, 9
# Create new RGBA image for mask given size:
planetsCreditsMask = Image.new("RGBA", creditsMaskSize)
planetsCreditsMask.save("Planets_Credits_Mask.png")
# Set top left corner of mask position in pixels:
creditsMaskPosition = 370, 487
# Paste mask over text region in planets image:
planetsImage.paste(planetsCreditsMask, creditsMaskPosition)

# Mask out 'Outer Planets' text in lower right corner:
# Set size of mask:
outerMaskSize = 73, 11
# Create new RGBA image for mask given size:
planetsOuterMask = Image.new("RGBA", outerMaskSize)
planetsOuterMask.save("Planets_Outer_Mask.png")
# Set top left corner of mask position in pixels:
outerMaskPosition = 424, 5
# Paste mask over text region in planets image:
planetsImage.paste(planetsOuterMask, outerMaskPosition)

# Mask out 'Inner Planets' text in lower right corner:
# Set size of mask:
innerMaskSize = 71, 11
# Create new RGBA image for mask given size:
planetsInnerMask = Image.new("RGBA", innerMaskSize)
planetsInnerMask.save("Planets_Inner_Mask.png")
# Set top left corner of mask position in pixels:
innerMaskPosition = 136, 25
# Paste mask over text region in planets image:
planetsImage.paste(planetsInnerMask, innerMaskPosition)

# Resize image:
planetsSize = 750, 750
planetsImage = planetsImage.resize(planetsSize, Image.ANTIALIAS)

# Save new size and colour image:
planetsImage.save("IMG/Planets_Position.png")

# Delete inner/outer/credits mask images now no longer needed:
os.remove("Planets_Credits_Mask.png")
os.remove("Planets_Outer_Mask.png")
os.remove("Planets_Inner_Mask.png")

# Create URL for planetary position tables
# (with correct long. lat. alt. and Modified Julian Date):
planetsTablesUrl = "http://www.heavens-above.com/planets.aspx?lat=" + str(latitude) + "&lng=" + str(longitude) + "&loc=Kielder+Observatory&alt=" + str(altitude) + "&tz=UCT"

# Get planetary distance and speed information from Heavens Above table:
soup = BeautifulSoup(urllib.request.urlopen(planetsTablesUrl).read(), "html.parser")

# Get Mercury data (in AU and kms):
mercurySolDistance = soup.find('span', {'id': 'ctl00_cph1_r1'})
mercurySolDistance = mercurySolDistance.text
mercuryEarthDistance = soup.find('span', {'id': 'ctl00_cph1_re1'})
mercuryEarthDistance = mercuryEarthDistance.text
mercurySpeed = soup.find('span', {'id': 'ctl00_cph1_v1'})
mercurySpeed = mercurySpeed.text
# Convert planet-Sol distance from AU to miles:
mercurySolDistanceMi = float(mercurySolDistance) * 92955807
mercurySolDistanceMi = int(round(mercurySolDistanceMi))
mercurySolDistanceMi = "{:,}".format(mercurySolDistanceMi)
# Convert planet-Earth distance from AU to miles:
mercuryEarthDistanceMi = float(mercuryEarthDistance) * 92955807
mercuryEarthDistanceMi = int(round(mercuryEarthDistanceMi))
mercuryEarthDistanceMi = "{:,}".format(mercuryEarthDistanceMi)
# Convert speed from kps to mph:
mercurySpeedMph = float(mercurySpeed) * 2236.9362920544
mercurySpeedMph = int(round(mercurySpeedMph))
mercurySpeedMph = "{:,}".format(mercurySpeedMph)

# Get Venus data (in AU and kms):
venusSolDistance = soup.find('span', {'id': 'ctl00_cph1_r2'})
venusSolDistance = venusSolDistance.text
venusEarthDistance = soup.find('span', {'id': 'ctl00_cph1_re2'})
venusEarthDistance = venusEarthDistance.text
venusSpeed = soup.find('span', {'id': 'ctl00_cph1_v2'})
venusSpeed = venusSpeed.text
# Convert planet-Sol distance from AU to miles:
venusSolDistanceMi = float(venusSolDistance) * 92955807
venusSolDistanceMi = int(round(venusSolDistanceMi))
venusSolDistanceMi = "{:,}".format(venusSolDistanceMi)
# Convert planet-Earth distance from AU to miles:
venusEarthDistanceMi = float(venusEarthDistance) * 92955807
venusEarthDistanceMi = int(round(venusEarthDistanceMi))
venusEarthDistanceMi = "{:,}".format(venusEarthDistanceMi)
# Convert speed from kps to mph:
venusSpeedMph = float(venusSpeed) * 2236.9362920544
venusSpeedMph = int(round(venusSpeedMph))
venusSpeedMph = "{:,}".format(venusSpeedMph)

# Get Earth data (in AU and kms):
earthSolDistance = soup.find('span', {'id': 'ctl00_cph1_r3'})
earthSolDistance = earthSolDistance.text
earthSpeed = soup.find('span', {'id': 'ctl00_cph1_v3'})
earthSpeed = earthSpeed.text
# Convert planet-Sol distance from AU to miles:
earthSolDistanceMi = float(earthSolDistance) * 92955807
earthSolDistanceMi = int(round(earthSolDistanceMi))
earthSolDistanceMi = "{:,}".format(earthSolDistanceMi)
# No Earth-Earth distance:
earthEarthDistanceMi = '-'
# Convert speed from kps to mph:
earthSpeedMph = float(earthSpeed) * 2236.9362920544
earthSpeedMph = int(round(earthSpeedMph))
earthSpeedMph = "{:,}".format(earthSpeedMph)

# Get Mars data (in AU and kms):
marsSolDistance = soup.find('span', {'id': 'ctl00_cph1_r4'})
marsSolDistance = marsSolDistance.text
marsEarthDistance = soup.find('span', {'id': 'ctl00_cph1_re4'})
marsEarthDistance = marsEarthDistance.text
marsSpeed = soup.find('span', {'id': 'ctl00_cph1_v4'})
marsSpeed = marsSpeed.text
# Convert planet-Sol distance from AU to miles:
marsSolDistanceMi = float(marsSolDistance) * 92955807
marsSolDistanceMi = int(round(marsSolDistanceMi))
marsSolDistanceMi = "{:,}".format(marsSolDistanceMi)
# Convert planet-Earth distance from AU to miles:
marsEarthDistanceMi = float(marsEarthDistance) * 92955807
marsEarthDistanceMi = int(round(marsEarthDistanceMi))
marsEarthDistanceMi = "{:,}".format(marsEarthDistanceMi)
# Convert speed from kps to mph:
marsSpeedMph = float(marsSpeed) * 2236.9362920544
marsSpeedMph = int(round(marsSpeedMph))
marsSpeedMph = "{:,}".format(marsSpeedMph)

# Get Jupiter data (in AU and kms):
jupiterSolDistance = soup.find('span', {'id': 'ctl00_cph1_r5'})
jupiterSolDistance = jupiterSolDistance.text
jupiterEarthDistance = soup.find('span', {'id': 'ctl00_cph1_re5'})
jupiterEarthDistance = jupiterEarthDistance.text
jupiterSpeed = soup.find('span', {'id': 'ctl00_cph1_v5'})
jupiterSpeed = jupiterSpeed.text
# Convert planet-Sol distance from AU to miles:
jupiterSolDistanceMi = float(jupiterSolDistance) * 92955807
jupiterSolDistanceMi = int(round(jupiterSolDistanceMi))
jupiterSolDistanceMi = "{:,}".format(jupiterSolDistanceMi)
# Convert planet-Earth distance from AU to miles:
jupiterEarthDistanceMi = float(jupiterEarthDistance) * 92955807
jupiterEarthDistanceMi = int(round(jupiterEarthDistanceMi))
jupiterEarthDistanceMi = "{:,}".format(jupiterEarthDistanceMi)
# Convert speed from kps to mph:
jupiterSpeedMph = float(jupiterSpeed) * 2236.9362920544
jupiterSpeedMph = int(round(jupiterSpeedMph))
jupiterSpeedMph = "{:,}".format(jupiterSpeedMph)

# Get Saturn data (in AU and kms):
saturnSolDistance = soup.find('span', {'id': 'ctl00_cph1_r6'})
saturnSolDistance = saturnSolDistance.text
saturnEarthDistance = soup.find('span', {'id': 'ctl00_cph1_re6'})
saturnEarthDistance = saturnEarthDistance.text
saturnSpeed = soup.find('span', {'id': 'ctl00_cph1_v6'})
saturnSpeed = saturnSpeed.text
# Convert planet-Sol distance from AU to miles:
saturnSolDistanceMi = float(saturnSolDistance) * 92955807
saturnSolDistanceMi = int(round(saturnSolDistanceMi))
saturnSolDistanceMi = "{:,}".format(saturnSolDistanceMi)
# Convert planet-Earth distance from AU to miles:
saturnEarthDistanceMi = float(saturnEarthDistance) * 92955807
saturnEarthDistanceMi = int(round(saturnEarthDistanceMi))
saturnEarthDistanceMi = "{:,}".format(saturnEarthDistanceMi)
# Convert speed from kps to mph:
saturnSpeedMph = float(saturnSpeed) * 2236.9362920544
saturnSpeedMph = int(round(saturnSpeedMph))
saturnSpeedMph = "{:,}".format(saturnSpeedMph)

# Get Uranus data (in AU and kms):
uranusSolDistance = soup.find('span', {'id': 'ctl00_cph1_r7'})
uranusSolDistance = uranusSolDistance.text
uranusEarthDistance = soup.find('span', {'id': 'ctl00_cph1_re7'})
uranusEarthDistance = uranusEarthDistance.text
uranusSpeed = soup.find('span', {'id': 'ctl00_cph1_v7'})
uranusSpeed = uranusSpeed.text
# Convert planet-Sol distance from AU to miles:
uranusSolDistanceMi = float(uranusSolDistance) * 92955807
uranusSolDistanceMi = int(round(uranusSolDistanceMi))
uranusSolDistanceMi = "{:,}".format(uranusSolDistanceMi)
# Convert planet-Earth distance from AU to miles:
uranusEarthDistanceMi = float(uranusEarthDistance) * 92955807
uranusEarthDistanceMi = int(round(uranusEarthDistanceMi))
uranusEarthDistanceMi = "{:,}".format(uranusEarthDistanceMi)
# Convert speed from kps to mph:
uranusSpeedMph = float(uranusSpeed) * 2236.9362920544
uranusSpeedMph = int(round(uranusSpeedMph))
uranusSpeedMph = "{:,}".format(uranusSpeedMph)

# Get Neptune data (in AU and kms):
neptuneSolDistance = soup.find('span', {'id': 'ctl00_cph1_r8'})
neptuneSolDistance = neptuneSolDistance.text
neptuneEarthDistance = soup.find('span', {'id': 'ctl00_cph1_re8'})
neptuneEarthDistance = neptuneEarthDistance.text
neptuneSpeed = soup.find('span', {'id': 'ctl00_cph1_v8'})
neptuneSpeed = neptuneSpeed.text
# Convert planet-Sol distance from AU to miles:
neptuneSolDistanceMi = float(neptuneSolDistance) * 92955807
neptuneSolDistanceMi = int(round(neptuneSolDistanceMi))
neptuneSolDistanceMi = "{:,}".format(neptuneSolDistanceMi)
# Convert planet-Earth distance from AU to miles:
neptuneEarthDistanceMi = float(neptuneEarthDistance) * 92955807
neptuneEarthDistanceMi = int(round(neptuneEarthDistanceMi))
neptuneEarthDistanceMi = "{:,}".format(neptuneEarthDistanceMi)
# Convert speed from kps to mph:
neptuneSpeedMph = float(neptuneSpeed) * 2236.9362920544
neptuneSpeedMph = int(round(neptuneSpeedMph))
neptuneSpeedMph = "{:,}".format(neptuneSpeedMph)

# Get Pluto data (in AU and kms):
plutoSolDistance = soup.find('span', {'id': 'ctl00_cph1_r9'})
plutoSolDistance = plutoSolDistance.text
plutoEarthDistance = soup.find('span', {'id': 'ctl00_cph1_re9'})
plutoEarthDistance = plutoEarthDistance.text
plutoSpeed = soup.find('span', {'id': 'ctl00_cph1_v9'})
plutoSpeed = plutoSpeed.text
# Convert planet-Sol distance from AU to miles:
plutoSolDistanceMi = float(plutoSolDistance) * 92955807
plutoSolDistanceMi = int(round(plutoSolDistanceMi))
plutoSolDistanceMi = "{:,}".format(plutoSolDistanceMi)
# Convert planet-Earth distance from AU to miles:
plutoEarthDistanceMi = float(plutoEarthDistance) * 92955807
plutoEarthDistanceMi = int(round(plutoEarthDistanceMi))
plutoEarthDistanceMi = "{:,}".format(plutoEarthDistanceMi)
# Convert speed from kps to mph:
plutoSpeedMph = float(plutoSpeed) * 2236.9362920544
plutoSpeedMph = int(round(plutoSpeedMph))
plutoSpeedMph = "{:,}".format(plutoSpeedMph)


#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open('Planets.html', 'w+')

# Write HTML href text to first line of new text HTML file:
planetsHtml = '''<!DOCTYPE html>
<html>
<title>
The Solar System Now
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
<b> The Solar System Now
</b>
</div>

<div class = "solarSystem">
	<img src = "IMG/Planets_Position.png">
	<div class = "key">Current Position of Planets</div>
</div>

<div class = "credits">Credit: www.heavens-above.com</div>

<table class = "solarSystemTable">
	<tr>
		<th>Planet<br></th>
		<th>Distance from<br>Sun (miles)</th>
		<th>Distance from<br>Earth (miles)</th>
		<th>Speed<br>(mph)</th>
	</tr>
	<tr>
		<td id="td01">Mercury</td>
		<td id="td01"><i>''' + mercurySolDistanceMi + '''</i></td>
		<td id="td01"><i>''' + mercuryEarthDistanceMi + '''</i></td>
		<td id="td01"><i>''' + mercurySpeedMph + '''</i></td>
	</tr>
	<tr>
		<td id="td02">Venus</td>
		<td id="td02"><i>''' + venusSolDistanceMi + '''</i></td>
		<td id="td02"><i>''' + venusEarthDistanceMi + '''</i></td>
		<td id="td02"><i>''' + venusSpeedMph + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Earth</td>
		<td id="td01"><i>''' + earthSolDistanceMi + '''</i></td>
		<td id="td01"><i>''' + earthEarthDistanceMi + '''</i></td>
		<td id="td01"><i>''' + earthSpeedMph + '''</i></td>
	</tr>
	<tr>
		<td id="td02">Mars</td>
		<td id="td02"><i>''' + marsSolDistanceMi + '''</i></td>
		<td id="td02"><i>''' + marsEarthDistanceMi + '''</i></td>
		<td id="td02"><i>''' + marsSpeedMph + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Jupiter</td>
		<td id="td01"><i>''' + jupiterSolDistanceMi + '''</i></td>
		<td id="td01"><i>''' + jupiterEarthDistanceMi + '''</i></td>
		<td id="td01"><i>''' + jupiterSpeedMph + '''</i></td>
	</tr>
	<tr>
		<td id="td02">Saturn</td>
		<td id="td02"><i>''' + saturnSolDistanceMi + '''</i></td>
		<td id="td02"><i>''' + saturnEarthDistanceMi + '''</i></td>
		<td id="td02"><i>''' + saturnSpeedMph + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Uranus</td>
		<td id="td01"><i>''' + uranusSolDistanceMi + '''</i></td>
		<td id="td01"><i>''' + uranusEarthDistanceMi + '''</i></td>
		<td id="td01"><i>''' + uranusSpeedMph + '''</i></td>
	</tr>
	<tr>
		<td id="td02">Neptune</td>
		<td id="td02"><i>''' + neptuneSolDistanceMi + '''</i></td>
		<td id="td02"><i>''' + neptuneEarthDistanceMi + '''</i></td>
		<td id="td02"><i>''' + neptuneSpeedMph + '''</i></td>
	</tr>
	<tr>
		<td id="td01">(Pluto)</td>
		<td id="td01"><i>''' + plutoSolDistanceMi + '''</i></td>
		<td id="td01"><i>''' + plutoEarthDistanceMi + '''</i></td>
		<td id="td01"><i>''' + plutoSpeedMph + '''</i></td>
	</tr>
</table>

<div class = "kielderLogo">
	<img src = "IMG/Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(planetsHtml)

# Close text file:
f.close()
