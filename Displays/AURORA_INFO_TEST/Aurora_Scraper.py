#!/usr/bin/python3


#############################################
# PYTHON SCRIPT TO WEB SCRAPE AURORAL IMAGES
# AND SOLAR WIND DATA FROM VARIOUS WEBSITES
#############################################


#############################################
# Import necessary modules:
#############################################

# Current system times:
import datetime
import ephem as e

# Parsing information and images from web:
from bs4 import BeautifulSoup
import urllib3, certifi
import requests
import json

# Manipulating (crop, resize, save etc.) images:
from io import BytesIO
from PIL import Image


#############################################
# Get live auroral oval from Space Weather
# website:
#############################################

#Checks whether the sun is below the horizon or not
kobs = e.Observer()
kobs.lon, kobs.lat = '-2.5881', '55.2330'
kobs.date = datetime.datetime.now()

#Compute Sun Altitude
sol = e.Sun()
sol.compute(kobs)

# Return First digit of Sun's altitude
alt = int(str(sol.alt).split(':')[0])

styleSheet = ""
if (alt <= -6):
    #read the contents of the dark style sheet for night time
    styleSheet = open("Aurora_Style_Dark.css", "r").read()
else:
    #read the contents of the light for day time style sheet
    styleSheet = open("Aurora_Style_Light.css", "r").read()
#End of checking whether or not the sun is below the horizon

# Needs updating every 5 minutes

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

# URLs to retrieve data from
auroraUrl = "https://services.swpc.noaa.gov/images/aurora-forecast-northern-hemisphere.jpg"
geoMagUrl = "https://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json"
plasmaUrl = "https://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json"
solIndicesUrl = "https://services.swpc.noaa.gov/text/daily-solar-indices.txt"
kIndexUrl = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"

# Get auroral oval image:
i = requests.get(auroraUrl)
spaceWeatherImage = Image.open(BytesIO(i.content))
#spaceWeatherImage = spaceWeatherImage.save("Aurora_Map.png")

# Resize image:
spaceWeatherSize = 750, 750
spaceWeatherImage = spaceWeatherImage.resize(spaceWeatherSize, Image.ANTIALIAS)

# Save revised image:
spaceWeatherImage.save("IMG/Aurora_Map.png")

# Parse JSON files from SWPC
geoMagJSON = json.loads(requests.get(geoMagUrl).text)
plasmaJSON = json.loads(requests.get(plasmaUrl).text)
kJSON = json.loads(requests.get(kIndexUrl).text)

with open("solardata.txt","w") as f:
    f.write(http.request('GET', solIndicesUrl).data.decode('utf-8'))

with open("solardata.txt", "r") as f:
    solIndText = f.readlines()[-1].split("    ")

# Get solar wind data:
solarWindSpeed = plasmaJSON[len(plasmaJSON)-1][2]
solarWindDensity = plasmaJSON[len(plasmaJSON)-1][1]

# Get sunspot data:
sunSpotNumber = solIndText[1].strip()

# Get magnetic field data:
bTotal = float(geoMagJSON[len(geoMagJSON)-1][6])
bZ = float(geoMagJSON[len(geoMagJSON)-1][3])
print(bTotal, bZ)
#bDirection = str(sunData[13])
if bZ == 0.0:
    bDirection = ""
    bColour = "green"
elif bZ > 0.0:
    bDirection = "North"
    bColour = "green"
else:
    bDirection = "South"
    bColour = "red"

# Get Kp index data:

# Get current planetary index data:
kNow = int(kJSON[len(kJSON)-1][1])
# Get Observed 24hr maximum planetary index data:
kMax = kNow
for i in range(1,8):
    histK = int(kJSON[len(kJSON) - i][1])
    if histK > kMax:
        kMax = histK

kColours = []

for i in [kNow, kMax]:
    if i >= 5:
        if i >=8:
            kColours.append('Severe')
        else:
            kColours.append('Storm')
        kColours.append('red')
    elif i >= 4:
        kColours.append('Unsettled')
        kColours.append('orange')
    else:
        kColours.append('Quiet')
        kColours.append('green')


#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open("Aurora.html", 'w+')

# Write HTML href text to first line of new text HTML file:
auroraHtml = '''<!DOCTYPE html>
<html>
<title>
The Aurora Now
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
<b> The Aurora Now
</b>
</div>

<div class = "auroralOval">
	<img src = "IMG/Aurora_Map.png">
	<div class = "key">Current Auroral Oval</div>
</div>

<div class = "credits">Credit: National Oceanic and Atmospheric Administration</div>

<table class = "spaceWeatherTable">
	<tr>
		<th colspan = 2>Solar Wind and Magnetic Field<br></th>
	</tr>
	<tr>
		<td id="td01">Solar Wind Speed (kph)</td>
		<td id="td01"><i>''' + solarWindSpeed + '''</i></td>
	</tr>
	<tr>
		<td id="td02">Solar Wind Density (protons/cm<sup>3</sup>)</td>
		<td id="td02"><i>''' + solarWindDensity + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Number of Sunspots</td>
		<td id="td01"><i>''' + sunSpotNumber + '''</i></td>
	</tr>
	<tr>
		<td id="td02">B<sub>total</sub> (nano Tesla)</td>
		<td id="td02"><i>''' + str(bTotal) + '''</i></td>
	</tr>
	<tr>
		<td id="td01">B<sub>z</sub> (nano Tesla)</td>
		<td id="td01"><i>''' + str(bZ) + ''' <font color = "'''+ bColour +'''"> ''' + bDirection + '''</font></i></td>
	</tr>
	<tr>
		<td id="td02">K-Index Now (0-9)</td>
		<td id="td02"><i>''' + str(kNow) + ''' <font color = "'''+ kColours[1] +'''"> ''' + kColours[0] + '''</font></i></td>
	</tr>
	<tr>
		<td id="td01">24hr Maximum K-Index (0-9)</td>
		<td id="td01"><i>''' + str(kMax) + ''' <font color = "'''+ kColours[3] +'''"> ''' + kColours[2] + '''</font></i></td>
	</tr>
</table>

<div class = "kielderLogo">
	<img src = "IMG/Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(auroraHtml)

# Close text file:
f.close()
