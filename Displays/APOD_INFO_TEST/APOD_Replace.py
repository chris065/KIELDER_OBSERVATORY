#!/usr/bin/python

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

# Manipulating (crop, resize, save etc.) images:
from PIL import Image
from io import BytesIO

# Manipulating strings:
import string


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
    # Set stylesheet to Night Shift mode
    styleSheet = open("APOD_Style_Dark.css", "r").read()
else:
    #Set Stylesheet to Night Shift mode
    styleSheet = open("APOD_Style_Light.css", "r").read()


with open("explanation.txt", "r") as ex:
    apodExplanation = ex.read()

with open("title.txt", "r") as ti:
    apodTitle = ti.read()

with open("credit.txt", "r") as cr:
    apodCredit = cr.read()

with open("frame.txt", "w") as fr:
    frame = fr.read()

#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open('../Screen1.html', 'w+')

# Write HTML href text to first line of new text HTML file:
apodHtml = '''<!DOCTYPE html>
<html>
<title>
NASA Astronomy Picture of the Day
</title>
<head>
<style>
'''+styleSheet+'''
</style>
</head>

<body>
<div>
<b> NASA Astronomy Picture of the Day - '''+apodDay.strftime("%d/%m/%Y")+'''

</b>
</div>

<div class = "apodPosition">
    '''+frame+'''
	<!--<img style = "max-height: 650px; max-width: 1840px;" src = "APOD_INFO_TEST/NASA_APOD.jpg">-->
	<div class = "key">''' + apodTitle + '''</div>
	<div class = "caption">''' + apodExplanation + '''</div>
</div>

<div class = "credits">Image Credit: ''' + apodCredit + '''</div>

</body>
</html>'''
f.write(apodHtml)

# Close text file:
f.close()
