#!/usr/bin/python


#############################################
# PYTHON SCRIPT TO WEBSCRAPE SOLAR SYSTEM
# IMAGE AND DATA FROM HEAVENS-ABOVE.COM
#############################################


#############################################
# Import necessary modules:
#############################################

# Current system times:
import datetime
import ephem as e
import julian

# RA and Dec coordinate conversion:
from astropy import units as u
from astropy.coordinates import SkyCoord

# Parsing information and images from HTML websites:
from bs4 import BeautifulSoup
import urllib3, certifi
import requests

# Manipulating (crop, resize, save etc.) images:
from PIL import Image
from io import BytesIO

# Setting environment variables and/or deleting files:
from os import remove


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

currentTime = datetime.datetime.utcnow()
mjd = julian.to_jd(currentTime, fmt='mjd')

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
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

planetsUrl = "http://www.heavens-above.com/SolarSystemPic.aspx?Epoch=" + str(mjd) + "&Width=500&Height=500&cul=en"

# Get solar system planetary positions image:
i = requests.get(planetsUrl)
planetsImage = Image.open(BytesIO(i.content))


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
remove("Planets_Credits_Mask.png")
remove("Planets_Outer_Mask.png")
remove("Planets_Inner_Mask.png")

# Create URL for planetary position tables
# (with correct long. lat. alt. and Modified Julian Date):
planetsTablesUrl = "http://www.heavens-above.com/planets.aspx?lat=" + str(latitude) + "&lng=" + str(longitude) + "&loc=Kielder+Observatory&alt=" + str(altitude) + "&tz=UCT"

# Get planetary distance and speed information from Heavens Above table:
planetPage = http.request('GET', planetsTablesUrl)
soup = BeautifulSoup(planetPage.data.decode('utf-8'), "html.parser")

listPlanets = [['Mercury', '1'], ['Venus', '2'], ['Earth', '3'], ['Mars', '4'], ['Jupiter', '5'], ['Saturn', '6'], ['Uranus', '7'], ['Neptune', '8'], ['(Pluto)', '9']]

for entry in listPlanets:
    tag = 'ctl00_cph1_r' + entry[1]
    solDistance = soup.find('span', {'id': tag})
    solDistance = solDistance.text
    solDistanceMi = float(solDistance) * 92955807
    solDistanceMi = round(solDistanceMi)
    solDistanceMi = "{:,}".format(solDistanceMi)
    entry.append(solDistanceMi)

    if entry[0] == 'Earth':
        earthDistanceMi = '-'
    else:
        tag = 'ctl00_cph1_re' + entry[1]
        earthDistance = soup.find('span', {'id': tag})
        earthDistance = earthDistance.text
        earthDistanceMi = float(earthDistance) * 92955807
        earthDistanceMi = round(earthDistanceMi)
        earthDistanceMi = "{:,}".format(earthDistanceMi)
    entry.append(earthDistanceMi)

    tag = 'ctl00_cph1_v' + entry[1]
    speed = soup.find('span', {'id': tag})
    speed = speed.text
    speedMph = float(speed) * 2236.9362920544
    speedMph = round(speedMph)
    speedMph = "{:,}".format(speedMph)
    entry.append(speedMph)
    print(entry)


planetTable = ""
for entry in listPlanets:
    planetTable = planetTable + '''
	<tr>
		<td id="td01">''' + entry[0] + '''</td>
		<td id="td01"><i>''' + entry[2] + '''</i></td>
		<td id="td01"><i>''' + entry[3] + '''</i></td>
		<td id="td01"><i>''' + entry[4] + '''</i></td>
	</tr>
    '''

#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open('../Disp.html', 'w+')

# Write HTML href text to first line of new text HTML file:
planetsHtml = '''<!DOCTYPE html>
<html>
<title>
The Solar System Now
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
<b> The Solar System Now
</b>
</div>

<div class = "solarSystem">
	<img src = "PLANETS_INFO_TEST/IMG/Planets_Position.png">
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
	''' + planetTable + '''
</table>

<div class = "kielderLogo">
	<img src = "IMG/Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(planetsHtml)

# Close text file:
f.close()
