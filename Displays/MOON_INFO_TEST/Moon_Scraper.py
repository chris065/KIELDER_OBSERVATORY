#!/usr/bin/python


#############################################
# PYTHON SCRIPT TO WEBSCRAPE MOON POSITION
# IMAGE AND DATA FROM HEAVENS-ABOVE.COM
#############################################


#############################################
# Import necessary modules:
#############################################

# Current system times:
import datetime
import ephem
import pytz

# Julian dates:
import julian

# Parsing information and images from HTML websites:
from bs4 import BeautifulSoup
import urllib3, certifi
import requests

# Manipulating (crop, resize, save etc.) images:
from PIL import Image
from io import BytesIO

# Setting environmenopent variables and/or deleting files:
from os import remove


http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

#############################################
# Determine the current Modified Julian Date:
#############################################

currentTime = datetime.datetime.utcnow()
mjd = julian.to_jd(currentTime, fmt='mjd')


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
gb = pytz.timezone('Europe/London')

kielderObs.date = datetime.datetime.utcnow()

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
m.compute(kielderObs)
# Constellation:
moonConstellation = ephem.constellation(m)
moonConstellation = moonConstellation[1] # Comes as tuple, e.g. ('Tau', 'Taurus')

# Moon rise and moon set, change behaviour depending on if Moon is up or not
moonalt = int(str(m.alt).split(':')[0])
moonList = []
if moonalt > 0: # Moon is up
    moonList.append('Last rose')
    moonRise = kielderObs.previous_rising(ephem.Moon())
    moonRise = moonRise.datetime().replace(tzinfo=pytz.utc)
    moonRise = moonRise.astimezone(tz=gb)
    moonList.append(moonRise.strftime("%H:%M:%S %Z"))
    moonList.append('Next sets')
    moonSet = kielderObs.next_setting(ephem.Moon())
    moonSet = moonSet.datetime().replace(tzinfo=pytz.utc)
    moonSet = moonSet.astimezone(tz=gb)
    moonList.append(moonSet.strftime("%H:%M:%S %Z"))
else:
    moonList.append('Last set')
    moonSet = kielderObs.previous_setting(ephem.Moon())
    moonSet = moonSet.datetime().replace(tzinfo=pytz.utc)
    moonSet = moonSet.astimezone(tz=gb)
    moonList.append(moonSet.strftime("%H:%M:%S %Z"))
    moonList.append('Next rises')
    moonRise = kielderObs.next_rising(ephem.Moon())
    moonRise = moonRise.datetime().replace(tzinfo=pytz.utc)
    moonRise = moonRise.astimezone(tz=gb)
    moonList.append(moonRise.strftime("%H:%M:%S %Z"))

# Illumination (%):
moonPhase = m.moon_phase
moonPhase = moonPhase * 100.0
moonPhase = round(moonPhase, 1)
moonPhase = str(moonPhase)
# Distance to Moon in miles:
moonRange = m.earth_distance
moonRange = moonRange * 92955807.3
moonRange = round(moonRange)
moonRange = "{:,}".format(moonRange)
print(moonRange)


#############################################
# Get live moon position image from Heavens
# Above website (Kielder specific
# coordinates):
#############################################

# Needs updating every 5 minutes

# Create URL for moon data (with Kielder specific loation):
moonDataUrl = "https://www.heavens-above.com/moon.aspx?lat=55.2323&lng=-2.616&loc=Kielder&alt=378&tz=GMT"

# Get HTML on moon from Heavens Above:
HTMLMoon = http.request('GET', moonDataUrl)
soup = BeautifulSoup(HTMLMoon.data.decode('utf-8'), "html.parser")

# Create URL for moon position image (with Kielder specific location,
# correct current Modified Julian Date and at desired size):
moonSkychartUrl = str([moonImg['src'] for moonImg in soup.findAll('img', {'id': 'ctl00_cph1_imageSky'})])
moonSkychartUrl = moonSkychartUrl[3:-2]
# Set image size to 750 pixels:
moonSkychartUrl = moonSkychartUrl.replace('size=500', 'size=750')
# Create URL:
moonPositionUrl = "https://www.heavens-above.com/s" + str(moonSkychartUrl)

# Get moon position image:
i = http.request('GET', moonPositionUrl)
moonPositionImage = Image.open(BytesIO(i.data))

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
remove("Moon_Credits_Mask.png")


# Determine Lunation and pick out Phase Image from List
nnm = ephem.next_new_moon(kielderObs.date)
pnm = ephem.previous_new_moon(kielderObs.date)

lunation=(kielderObs.date-pnm)/(nnm-pnm)

if (lunation < 0.5):
	moonStatus = 'Waxing'
else:
	moonStatus = 'Waning'

fileno = int(lunation*713)

moonlist=open("frames/aa_filelist.txt", "r")

for c, line in enumerate(moonlist):
	#print(c, value)
	if (c ==fileno):
		phase = line
		break


#Compute Sun Altitude to select CSS Stylesheet
sol = ephem.Sun()
sol.compute(kielderObs)

styleSheet = ""

# Return First digit of Sun's altitude
alt = int(str(sol.alt).split(':')[0])
if (alt < -6):
    #read the contents of the dark style sheet for night time
    styleSheet = open("Moon_Style_Dark.css", "r").read()
else:
    #read the contents of the light for day time style sheet
    styleSheet = open("Moon_Style_Light.css", "r").read()

#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open("../Disp.html", 'w+')

# Write HTML href text to first line of new text HTML file:
moonHtml = '''<!DOCTYPE html>
<html>
<title>
The Moon Now
</title>
<head>
<link href="https://fonts.googleapis.com/css?family=Roboto:400,700" rel="stylesheet">
<style>
'''+styleSheet+'''
</style>
</head>

<body>

    <script>
        setTimeout(function()
        {
            location.reload();
        }, 3*60000);
    </script>

<div>
<b> The Moon Now
</b>
</div>

<div class = "moonPos">
	<img src = "MOON_INFO_TEST/Moon_Position.png">
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
		<td id="td01">Illumination</td>
		<td id="td01"><i>''' + moonPhase + ''' % (''' + moonStatus  +  ''')</i></td>
	</tr>
	<tr>
		<td id="td02">''' + moonList[0] + '''</td>
		<td id="td02"><i>''' + moonList[1] + '''</i></td>
	</tr>
	<tr>
		<td id="td01">''' + moonList[2] + '''</td>
		<td id="td01"><i>''' + moonList[3] + '''</i></td>
	</tr>
	<tr>
		<td id="td02" rowspan = 5>Phase</td>
		<td id="td03"rowspan = 5 align = "center" style = "background-color:#000000;"><img style = "width:60%;" src = MOON_INFO_TEST/frames/''' + phase + '''></td>	</tr>
</table>

<div class = "kielderLogo">
	<img src = "MOON_INFO_TEST/IMG/Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(moonHtml)

# Close text file:
f.close()
