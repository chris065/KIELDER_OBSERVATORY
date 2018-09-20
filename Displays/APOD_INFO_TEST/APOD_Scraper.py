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

# Parsing information and images from HTML websites:
from bs4 import BeautifulSoup
import urllib3, certifi, requests, json

# NASA APOD API and enviromental variable for API key:
from nasa import apod as nasaApod

# Manipulating (crop, resize, save etc.) images:
from PIL import Image
from io import BytesIO

# Setting environment variables and/or deleting files:
from subprocess import run

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

apodDay = datetime.datetime.now()

if (apodDay.hour < 9):
    apodDay = apodDay - datetime.timedelta(days=1) # Pull yesterday's APOD if before 9am
# Convert date to YYYY-MM-DD format:
apodDate = apodDay.strftime("%Y-%m-%d")

# Get image source for NASA APOD website:
astroPod = nasaApod.apod(apodDate)
apodUrl = str(astroPod.url)
apodUrl2 = "https://api.nasa.gov/planetary/apod?api_key=" + "VSeA2cMgNPtUslwyxj1cSGztgo8ZLJhUkGyA2IZ1"
apodUrl3 = "https://apod.nasa.gov/apod/ap"+apodDay.strftime('%y%m%d')+".html"

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

# NASA API returns a JSON object, read contents into memory
jApod = requests.get(apodUrl2)
aPod = json.loads(jApod.text)

apodPage = http.request('GET', apodUrl3)
soup = BeautifulSoup(apodPage.data.decode('utf-8'), "html.parser")
yturl = ""
iframe = ""

if (str(soup.iframe) != 'None'):
    #print(soup.iframe)
    if "youtube" in str(soup.iframe): # Youtube Video, prepare to download
        yturl = str(soup.iframe).split("youtube.com/embed/")[1].split("?rel")[0]
        run("youtube-dl -F https://youtube.com/watch?v="+yturl+" | grep mp4 | grep video | tail -n 1 > ytinfo.txt", shell=True)
        with open("ytinfo.txt", "r") as f:
            qual = f.read().split("mp4")[0].strip()
        run("youtube-dl -f "+qual+" https://youtube.com/watch?v="+yturl+"", shell=True)
        run("mv *.mp4 APODVideo.mp4", shell=True)
    else: # Other interactive frame. Embed directly.
        iframe = str(soup.iframe)
else: # APOD is image, fetch
    i = requests.get(aPod['hdurl'])
    apodImage = Image.open(BytesIO(i.content))
    #print(Image.format(apodImage))
    apodImage.save("NASA_APOD.jpg")


# Save Data for Future Use
with open("explanation.txt", "w+") as ex:
    ex.write(aPod['explanation'])

with open("title.txt", "w+") as ti:
    ti.write(apodTitle)

with open("credit.txt", "w+") as cr:
    cr.write(aPod['copyright'])

#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open('../Screen1.html', 'w+')

# Decide how to embed content
if yturl != "":
    frame = '''<video src="APOD_INFO_TEST/APODVideo.mp4" height="650" preload autoplay loop> </video>'''
elif iframe != "":
    frame = iframe
else:
    frame = '''<img style = "max-height: 650px; max-width: 1840px;" src = "APOD_INFO_TEST/NASA_APOD.jpg">'''

with open("frame.txt", "w") as fr:
    fr.write(frame)

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
	<div class = "key">''' + aPod['title'] + '''</div>
	<div class = "caption">''' + aPod['explanation'] + '''</div>
</div>

<div class = "credits">Image Credit: ''' + aPod['copyright'] + '''</div>

</body>
</html>'''
f.write(apodHtml)

# Close text file:
f.close()
