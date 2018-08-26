#!/usr/bin/python


#############################################
# PYTHON SCRIPT TO WEBSCRAPE MOON POSITION
# IMAGE AND DATA FROM HEAVENS-ABOVE.COM
#############################################


#############################################
# Import necessary modules:
#############################################

# Current system times:
from datetime import datetime, timedelta

# Julian dates:
from astropy.time import Time

# Functions for calculating if GMT or BST times:
import pytz

# RA and Dec coordinate conversion:
from astropy import units as u
from astropy.coordinates import SkyCoord

# Parsing information and images from HTML websites:
from bs4 import BeautifulSoup
import urllib
import requests

# Rounding off functions:
import decimal

# Manipulating (crop, resize, save etc.) images:
from PIL import Image

# Manipulating strings:
import string

# Setting environment variables and/or deleting files:
import os

# Ephemeris tools for calculating moon position:
import ephem

import datetime

darkStyleSheet = ""
lightStyleSheet = ""
styleSheet = ""

kobs = ephem.Observer()
kobs.lon, kobs.lat = '-2.5881', '55.2330'
kobs.date = datetime.datetime.now()

#Compute Sun Altitude
sol = ephem.Sun()
sol.compute(kobs)

# Return First digit of Sun's altitude
alt = int(str(sol.alt).split(':')[0])

if (alt < -6):
    #read the contents of the dark style sheet for night time
    darkStyleSheet = open("Moon_Style_Dark.css", "r").read()
    styleSheet = darkStyleSheet
else:
    #read the contents of the light for day time style sheet
    lightStyleSheet = open("Moon_Style_Light.css", "r").read()
    styleSheet = lightStyleSheet


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

latitude = 55.233
longitude = -2.5881
altitude = 210


#############################################
# Create an observatory setup for PyEphem:
#############################################

kielderObs = ephem.Observer()

#PyEphem takes and returns only UTC times. Current noon
#is not always UTC noon in Kielder depending on daylight saving:
# Determine if GMT or BST:
tz = pytz.timezone('Europe/London')
now = pytz.utc.localize(datetime.datetime.utcnow())
britishSummerTime = now.astimezone(tz).dst() != timedelta(0)
if britishSummerTime == True:
  utcOffset = '11:00:00'
elif britishSummerTime == False:
  utcOffset = '12:00:00'

currentDate = datetime.datetime.now()
currentDate = str(currentDate)
currentDate = currentDate[0:10]
kielderObsDate = currentDate + ' ' + utcOffset
kielderObsDate = kielderObsDate.replace('-','/')
kielderObs.date = kielderObsDate

# Set coordinates as strings for PyEphem:
kielderObs.lat = str(55.2305486)
kielderObs.lon = str(-2.6054411)
kielderObs.elev = 370

# To get U.S. Naval Astronomical Almanac values, use these settings
kielderObs.pressure = 0
kielderObs.horizon = '-0:34'
# (option to set temp./pressure of atmoshphere for refraction
# calculations, but NOAA/USNO ignore this so we will too)

# Calculate current moon parameters:
m = ephem.Moon()
m.compute(kielderObsDate)
# Constellation:
moonConstellation = ephem.constellation(m)
moonConstellation = moonConstellation[1] # Comes as tuple, e.g. ('Tau', 'Taurus')
moonConstellation = str(moonConstellation)
# Moon rise and moon set:
moonSet = kielderObs.next_setting(ephem.Moon()) # Sunset
moonSet = str(moonSet)
moonSet = moonSet[-8:]
moonRise = kielderObs.previous_rising(ephem.Moon()) # Sunset
moonRise = str(moonRise)
moonRise = moonRise[-8:]
# Illumination (%):
moonPhase = m.moon_phase
moonPhase = decimal.Decimal(moonPhase * 100.0)
moonPhase = round(moonPhase, 1)
moonPhase = str(moonPhase)
# Distance to Moon in miles:
moonRange = m.earth_distance
moonRange = moonRange * 92955807.3
moonRange = decimal.Decimal(moonRange)
moonRange = int(round(moonRange))
moonRange = "{:,}".format(moonRange)
moonRange = str(moonRange)


#############################################
# Get live moon position image from Heavens
# Above website (Kielder specific
# coordinates):
#############################################

# Needs updating every 5 minutes

# Create URL for moon data (with Kielder specific loation):
moonDataUrl = "https://www.heavens-above.com/moon.aspx?lat=55.2323&lng=-2.616&loc=Kielder&alt=378&tz=GMT"

# Get HTML on moon from Heavens Above:
soup = BeautifulSoup(urllib.request.urlopen(moonDataUrl).read(), "html.parser")

# Create URL for moon position image (with Kielder specific location,
# correct current Modified Julian Date and at desired size):
moonSkychartUrl = str([moonImg['src'] for moonImg in soup.findAll('img', {'id': 'ctl00_cph1_imageSky'})])
moonSkychartUrl = moonSkychartUrl[3:-2]
# Set image size to 750 pixels:
moonSkychartUrl = moonSkychartUrl.replace('size=500', 'size=750')
# Create URL:
moonPositionUrl = "http://www.heavens-above.com/s" + str(moonSkychartUrl)

# Get moon position image:
moonPositionImage = urllib.request.urlretrieve(moonPositionUrl, "Moon_Position.png")
moonPositionImage = Image.open("Moon_Position.png")

# Change blue background colour in image to pure black:
# Convert image to RGB colour space:
moonPositionImage = moonPositionImage.convert("RGBA")
# Read in pixel colours:
pixels = moonPositionImage.getdata()
newPixels = []
# Loop over pixels:
for pixel in pixels:
# Heavens Above background colour is 0,0,32 in RGB space
  if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 32:
    newPixels.append((0, 0, 0, 0))
  else:
    newPixels.append(pixel)
# Set new pixel array:
moonPositionImage.putdata(newPixels)

# Mask out 'Heavens Above' text in lower right corner:
# Set size of mask:
creditsMaskSize = 114, 10
# Create new RGBA image for mask given size:
moonCreditsMask = Image.new("RGBA", creditsMaskSize)
moonCreditsMask.save("Moon_Credits_Mask.png")
# Set top left corner of mask position in pixels:
creditsMaskPosition = 384, 487
# Paste mask over text region in planets image:
moonPositionImage.paste(moonCreditsMask, creditsMaskPosition)

# Save revised image:
moonPositionImage.save("Moon_Position.png")

# Create URL for moon phase with correct Modified Julian Date:
moonPhaseUrl = "http://www.heavens-above.com/moonchart.aspx?sz=220&mjd=" + str(mjd)

# Get moon phase image:
moonPhaseImage = urllib.request.urlretrieve(moonPhaseUrl, "Moon_Phase.png")
moonPhaseImage = Image.open("Moon_Phase.png")

# Change blue background colour in image to pure black:
# Convert image to RGB colour space:
moonPhaseImage = moonPhaseImage.convert("RGBA")
# Read in pixel colours:
pixels = moonPhaseImage.getdata()
newPixels = []
# Loop over pixels:
for pixel in pixels:
# Heavens Above background colour is 0,0,32 in RGB space
  if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 32:
    newPixels.append((0, 0, 0, 0))
  else:
    newPixels.append(pixel)
# Set new pixel array:
moonPhaseImage.putdata(newPixels)

# Crop moon phase image from 220x220 to size:
moonPhaseLeft = 10
moonPhaseTop = 1
moonPhaseRight = 210
moonPhaseBottom = 210
moonPhaseImage = moonPhaseImage.crop((moonPhaseLeft, moonPhaseTop, moonPhaseRight, moonPhaseBottom))

# Save revised image:
moonPhaseImage.save("Moon_Phase.png")

# Delete credits mask images now no longer needed:
os.remove("Moon_Credits_Mask.png")


#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open("Moon.html", 'w+')

# Write HTML href text to first line of new text HTML file:
moonHtml = '''<!DOCTYPE html>
<html>
<title>
The Moon Now
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
<b> The Moon Now
</b>
</div>

<div class = "moonPos">
	<img src = "Moon_Position.png">
	<div class = "key">Current Moon Position on Sky</div>
</div>

<div class = "credits">Credit: www.heavens-above.com</div>

<table class = "moonTable">
	<tr>
		<th colspan = 2>Moon Data<br></th>
	</tr>
	<tr>
		<td id="td01">Range (miles)</td>
		<td id="td01"><i>''' + moonRange + '''</i></td>
	</tr>
	<tr>
		<td id="td02">Constellation</td>
		<td id="td02"><i>''' + moonConstellation + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Illumination (%)</td>
		<td id="td01"><i>''' + moonPhase + '''%</i></td>
	</tr>
	<tr>
		<td id="td02">Set Time</td>
		<td id="td02"><i>''' + moonSet + ''' (GMT)</i></td>
	</tr>
	<tr>
		<td id="td01">Rise Time</td>
		<td id="td01"><i>''' + moonRise + ''' (GMT)</i></td>
	</tr>
	<tr>
		<td id="td02" rowspan = 5>Phase</td>
		<td id="td03"rowspan = 5 align = "center"><img src = "Moon_Phase.png"></td>
	</tr>
</table>

<div class = "kielderLogo">
	<img src = "IMG/Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(moonHtml)

# Close text file:
f.close()
