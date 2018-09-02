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

# Julian dates:
from astropy.time import Time

# Parsing information and images from HTML websites:
from bs4 import BeautifulSoup
import urllib
import requests

# NASA APOD API and enviromental variable for API key:
from datetime import date
from nasa import apod as nasaApod

# Manipulating (crop, resize, save etc.) images:
from PIL import Image

# Manipulating strings:
import string

# Setting environment variables and/or deleting files:
import os
import sys

darkStyleSheet = ""
lightStyleSheet = ""
styleSheet = ""
apodTitle = ""

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
    styleSheet = open("APOD_Style_Dark.css", "r").read()
else:
    #read the contents of the light for day time style sheet
    styleSheet = open("APOD_Style_Light.css", "r").read()


#############################################
# Get today's NASA APOD image:
#############################################

# Only needs to be done daily

# Uses a Python NASA API (see brendanv github repository)
# Note that API was installed with pip installer, but API
# code was changed to reflect different NASA API website

# Set NASA API key as environment variable:
os.environ['NASA_API_KEY'] = 'VSeA2cMgNPtUslwyxj1cSGztgo8ZLJhUkGyA2IZ1'

# Create today's date in YYYY-MM-DD format:
apodDate = str(datetime.datetime.now())[0:10]

# Get image source for NASA APOD website:
astroPod = nasaApod.apod(apodDate)
apodUrl = str(astroPod.url)
apodUrl2 = "https://api.nasa.gov/planetary/apod?api_key=" + "VSeA2cMgNPtUslwyxj1cSGztgo8ZLJhUkGyA2IZ1"
apodUrl3 = "https://apod.nasa.gov/apod/astropix.html"

testsoup = BeautifulSoup(urllib.request.urlopen(apodUrl3).read(), "html.parser")
yturl = ""
iframe = ""

if (str(testsoup.iframe) != 'None'):
    #print(testsoup.iframe)
    if "youtube" in str(testsoup.iframe): # Youtube Video, prepare to download
        yturl = str(testsoup.iframe).split("youtube.com/embed/")[1].split("?rel")[0]
        run("youtube-dl -F https://youtube.com/watch?v="+yturl+" | grep mp4 | grep video | tail -n 1 > ytinfo.txt", shell=True)
        with open("ytinfo.txt", "r") as f:
            qual = f.read().split("mp4")[0].strip()
        print(qual)
        run("youtube-dl -f "+qual+" https://youtube.com/watch?v="+yturl+"", shell=True)
        run("mv *.mp4 APODVideo.mp4", shell=True)
    else: # Other interactive frame. Embed directly.
        iframe = str(testsoup.iframe)
else: # APOD is image, fetch
    apodImage = urllib.request.urlretrieve(apodUrl, "NASA_APOD.jpg")
    apodImage = Image.open("NASA_APOD.jpg")
    apodImage.save("NASA_APOD.jpg")

# Get explanatory text for NASA APOD website:
apodExplanation = str(astroPod.explanation)

# Get credits for NASA APOD website:
soup = BeautifulSoup(urllib.request.urlopen(apodUrl2).read(), "html.parser")
# Strip out HTML tags in source code:
apodText = str(soup.getText())
# Strip off preceding text before copywrite name:
apodText = apodText[18:]
index = apodText.find('"')
# Strip off following text after copywrite name:
apodCredit = apodText[:index]

# Save Data for Future Use
ex = open("explanation.txt", "w+")
ex.write(apodExplanation)
ex.close()

ti = open("title.txt", "w+")
ti.write(apodTitle)
ti.close()

cr = open("credit.txt", "w+")
cr.write(apodCredit)
#print(apodCredit)
cr.close()

#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open('APOD.html', 'w+')

# Decide how to embed content
if yturl != "":
    frame = '''<video src="APOD_INFO_TEST/APODVideo.mp4" height="650" preload autoplay loop> </video>'''
elif iframe != "":
    frame = iframe
else:
    frame = '''<img style = "max-height: 650px; max-width: 1840px;" src = "APOD_INFO_TEST/NASA_APOD.jpg">'''

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
<b> NASA Astronomy Picture of the Day -
<script language = "javascript">
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();
	if(dd<10) {
		dd='0'+dd
	}
	if(mm<10) {
		mm='0'+mm
	}
	today = dd+'/'+mm+'/'+yyyy;
	document.write(today);
</script>
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
