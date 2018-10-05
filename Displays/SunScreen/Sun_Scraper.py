#!/usr/bin/python


#############################################
# PYTHON SCRIPT TO WEBSCRAPE SOLAR IMAGES
# LIVE FROM NASA SOLAR DYNAMICS OBSERVATORY
#############################################


#############################################
# Import necessary modules:
#############################################


# Parsing information and images from HTML websites:
import urllib3, certifi
import requests

# Manipulating (crop, resize, save etc.) images:
from PIL import Image
from io import BytesIO

import ephem as e
import datetime

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
    styleSheet = open("Sun_Style_Dark.css", "r").read()
else:
    #read the contents of the light for day time style sheet
    styleSheet = open("Sun_Style_Light.css", "r").read()


#############################################
# Get live SDO images from NASA SDO website:
#############################################

# Needs updating every 15 minutes


# Create URL for sun X-ray image:
xRayUrl = "http://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0094.jpg"
visibleUrl = "http://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIC.jpg"
magnetoUrl = "http://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIB.jpg"

imageList = [[xRayUrl, 'XRay_Sun'], [visibleUrl, 'Visible_Sun'], [magnetoUrl, 'Magnetic_Sun']]

for image in imageList:
    i = requests.get(image[0])
    sunImage = Image.open(BytesIO(i.content))

    # Crop X-ray image from 1024x1024 to size and to remove ugly timestamps:
    left = 40
    top = 40
    right = 984
    bottom = 984
    imageSize = 586, 586
    sunImage = sunImage.crop((left, top, right, bottom))
    sunImage = sunImage.resize(imageSize, Image.ANTIALIAS)

    # Save revised image:
    filename = "IMG/" + image[1] + ".jpg"
    sunImage.save(filename)


f = open("../Disp.html", "w+")

sunHTML = '''<!DOCTYPE html>
<html>
<title>
The Sun Now
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
    }, 6*60000);
  </script>

<div>
<b> The Sun Now
</b>
</div>

<div class = "sunVisible">
	<img src = "SUN_INFO_TEST/IMG/Visible_Sun.jpg">
	<div class = "key">Visible Light:</div>
	<div class = "caption">Intensitygram (~5700&#176C)<br>- sunspots appear darker</div>
</div>

<div class = "sunMagneto">
	<img src = "SUN_INFO_TEST/IMG/Magnetic_Sun.jpg">
	<div class = "key">Magnetogram (6173&Aring):</div>
	<div class = "caption">Magnetic fields in the photosphere<br>- black/white showing opposite poles</div>
</div>

<div class = "sunXray">
	<img src = "SUN_INFO_TEST/IMG/XRay_Sun.jpg">
	<div class = "key">Soft X-Rays (94&Aring):</div>
	<div class = "caption">Flares (~6million&#176C) in the corona<br>- hottest regions appear white</div>
</div>

<div class = "credits">Credit: NASA Solar Dynamics Observatory</div>

<div class = "kielderLogo">
	<img src = "IMG/Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(sunHTML)
f.close()
