#!/usr/bin/python


#############################################
# PYTHON SCRIPT TO WEBSCRAPE SOLAR IMAGES
# LIVE FROM NASA SOLAR DYNAMICS OBSERVATORY
#############################################


#############################################
# Import necessary modules:
#############################################


# Parsing information and images from HTML websites:
import urllib
import requests

# Manipulating (crop, resize, save etc.) images:
from PIL import Image

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
    darkStyleSheet = open("Sun_Style_Dark.css", "r").read()
    styleSheet = darkStyleSheet
else:
    #read the contents of the light for day time style sheet
    lightStyleSheet = open("Sun_Style_Light.css", "r").read()
    styleSheet = lightStyleSheet


#############################################
# Get live SDO images from NASA SDO website:
#############################################

# Needs updating every 15 minutes

# Create URL for sun X-ray image:
xRayUrl = "http://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0094.jpg"

# Get SDO soft X-ray image:
sdoImage1 = urllib.request.urlretrieve(xRayUrl, "XRay_Sun.jpg")
xRayImage = Image.open("XRay_Sun.jpg")

# Crop X-ray image from 1024x1024 to size and to remove ugly timestamps:
xRayLeft = 40
xRayTop = 40
xRayRight = 984
xRayBottom = 984
xRaySize = 586, 586
xRayImage = xRayImage.crop((xRayLeft, xRayTop, xRayRight, xRayBottom))
xRayImage = xRayImage.resize(xRaySize, Image.ANTIALIAS)

# Save revised image:
xRayImage.save("IMG/XRay_Sun.jpg")

# Create URL for sun visible light intensitygram image:
visibleUrl = "http://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIC.jpg"

# Get SDO visible light composite image:
sdoImage2 = urllib.request.urlretrieve(visibleUrl, "Visible_Sun.jpg")
sunImage = Image.open("Visible_Sun.jpg")

# Crop visible light image from 1024x1024 to size and remove ugly timestamps:
visLeft = 37
visTop = 37
visRight = 987
visBottom = 987
visSize = 586, 586
sunImage = sunImage.crop((visLeft, visTop, visRight, visBottom))
sunImage = sunImage.resize(visSize, Image.ANTIALIAS)

# Save revised image:
sunImage.save("IMG/Visible_Sun.jpg")

# Create URL for sun magnetogram image:
magnetoUrl = "http://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIB.jpg"

# Get SDO magnetogram image:
sdoImage3 = urllib.request.urlretrieve(magnetoUrl, "IMG/Magnetic_Sun.jpg")
magnetoImage = Image.open("IMG/Magnetic_Sun.jpg")

# Crop magnetic image from 1024x1024 to size and remove ugly timestamps:
magneticLeft = 37
magneticTop = 37
magneticRight = 987
magneticBottom = 987
magneticSize = 586, 586
magnetoImage = magnetoImage.crop((magneticLeft, magneticTop, magneticRight, magneticBottom))
magnetoImage = magnetoImage.resize(magneticSize, Image.ANTIALIAS)

# Save revised image:
magnetoImage.save("IMG/Magnetic_Sun.jpg")

f = open("../Screen3.html", "w+")

sunHTML = '''<!DOCTYPE html>
<html>
<title>
The Sun Now
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
