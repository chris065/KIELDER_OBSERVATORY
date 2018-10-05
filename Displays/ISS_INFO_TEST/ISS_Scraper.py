#!/usr/bin/python3


#############################################
# PYTHON SCRIPT TO WEB SCRAPE IMAGES AND
# DATA FROM VARIOUS WEBSITES
#############################################


#############################################
# Import necessary modules:
#############################################

# Current system times:
import datetime
import ephem as e

# Parsing information and images from web:
import urllib3
import requests

# Manipulating (crop, resize, save etc.) images:
from io import BytesIO
from PIL import Image

# Setting environment variables and/or deleting files:
import os

styleSheet = ""

kobs = e.Observer()
kobs.lon, kobs.lat = '-2.5881', '55.2330'
kobs.date = datetime.datetime.now()

#Compute Sun Altitude
sol = e.Sun()
sol.compute(kobs)

# Return First digit of Sun's altitude
alt = int(str(sol.alt).split(':')[0])

if (alt <= -6):
    #read the contents of the dark style sheet for night time
    styleSheet = open("ISS_Style_Dark.css", "r").read()
else:
    #read the contents of the light for day time style sheet
    styleSheet = open("ISS_Style_Light.css", "r").read()

#############################################
# Get live ISS positions from Heavens Above
# website:
#############################################

# Needs updating every 5 minutes

# Create URL for ISS ground track image:
issGroundUrl = "http://www2.heavens-above.com/orbitdisplay.aspx?icon=iss&width=1500&height=750&mode=M&satid=25544"

# Get image of ISS track over ground:
i = requests.get(issGroundUrl)
issGroundImage = Image.open(BytesIO(i.content))

# Mask out 'Heavens Above' text in lower right corner:
# Set size of mask:
issGroundCreditsMaskSize = 107, 8
# Determine if it is winter or summer at south pole
# (mask needs to be dark green if night, bright green if light)
dayOfYear = datetime.datetime.today().timetuple().tm_yday
# "Day of year" ranges for the northern hemisphere:
spring = range(80, 172)
summer = range(172, 264)
autumn = range(264, 355)
# Determine season (flip for southern hemisphere)
if dayOfYear in spring:
  season = 'Autumn'
elif dayOfYear in summer:
  season = 'Winter'
elif doy in autumn:
  season = 'Spring'
else:
  season = 'Summer'
# Base mask colour on season:
if season == 'Autumn' or 'Winter':
  issGroundCreditsMaskColour = '#005000'
elif season == 'Spring' or 'Summer':
  issGroundCreditsMaskColour = '#008000'
# Create new RGBA image for mask given size and appropriate colour:
issGroundCreditsMask = Image.new("RGBA", issGroundCreditsMaskSize, color = issGroundCreditsMaskColour)
issGroundCreditsMask.save("ISS_Ground_Credits_Mask.png")
# Set top left corner of mask position in pixels:
issGroundCreditsMaskPosition = 1390, 740
# Paste mask over text region in planets image:
issGroundImage.paste(issGroundCreditsMask, issGroundCreditsMaskPosition)

# Save new size and colour image:
issGroundImage.save("IMG/ISS_Ground.png")

# Create URL for ISS orbital plane image:
issOrbitUrl = "http://www2.heavens-above.com/orbitdisplay.aspx?icon=iss&width=300&height=300&mode=N&satid=25544"

# Get image of ISS plane view image:
i = requests.get(issOrbitUrl)
issOrbitImage = Image.open(BytesIO(i.content))

# Mask out 'Heavens Above' text in lower right corner:
# Set size of mask:
issOrbitCreditsMaskSize = 107, 8
# Create new RGBA image for mask given size and appropriate colour:
issOrbitCreditsMask = Image.new("RGBA", issOrbitCreditsMaskSize)
issOrbitCreditsMask.save("ISS_Orbit_Credits_Mask.png")
# Set top left corner of mask position in pixels:
issOrbitCreditsMaskPosition = 190, 290
# Paste mask over text region in planets image:
issOrbitImage.paste(issOrbitCreditsMask, issOrbitCreditsMaskPosition)

# Save new size and colour image:
issOrbitImage.save("IMG/ISS_Orbit.png")

# Create URL for ISS orbital plane image:
issViewUrl = "http://www2.heavens-above.com/orbitdisplay.aspx?icon=iss&width=300&height=300&mode=A&satid=25544"

# Get image of ISS satellite view image:
i = requests.get(issViewUrl)
issViewImage = Image.open(BytesIO(i.content))

# Mask out 'Heavens Above' text in lower right corner:
# Set size of mask:
issViewCreditsMaskSize = 107, 8
# Create new RGBA image for mask given size and appropriate colour:
issViewCreditsMask = Image.new("RGBA", issViewCreditsMaskSize)
issViewCreditsMask.save("ISS_View_Credits_Mask.png")
# Set top left corner of mask position in pixels:
issViewCreditsMaskPosition = 190, 290
# Paste mask over text region in planets image:
issViewImage.paste(issViewCreditsMask, issViewCreditsMaskPosition)

# Save new size and colour image:
issViewImage.save("IMG/ISS_View.png")

# Delete credits mask images now no longer needed:
os.remove("ISS_Ground_Credits_Mask.png")
os.remove("ISS_Orbit_Credits_Mask.png")
os.remove("ISS_View_Credits_Mask.png")


#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open('../Disp.html', 'w+')

# Write HTML href text to first line of new text HTML file:
issHtml = '''<!DOCTYPE html>
<html>
<title>
The International Space Station Now
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
    }, 3*60000);//refresh every 6 minutes. The exta minute is for delay
  </script>

<div>
<b> The International Space Station Now
</b>
</div>

<div class = "issGround">
	<img src = "ISS_INFO_TEST/IMG/ISS_Ground.png">
	<div class = "key">Ground Track</div>
</div>

<div class="issOrbit">
    <img src = ""ISS_INFO_TEST/IMG/ISS_Orbit.png">
  <div class = "key">Orbital View</div>
</div>

<div class = "issView">
	<img src = ""ISS_INFO_TEST/IMG/ISS_View.png">
	<div class = "key">ISS View</div>
</div>

<div class = "credits">Credit: www.heavens-above.com</div>

<div class = "kielderLogo">
	<img src = ""ISS_INFO_TEST/IMG/Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(issHtml)

# Close text file:
f.close()
