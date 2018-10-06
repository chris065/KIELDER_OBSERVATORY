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
import ephem
import julian
import pytz

# Parsing information and images from HTML websites:
#from bs4 import BeautifulSoup
import urllib3, certifi
import requests
from bs4 import BeautifulSoup

# Manipulating (crop, resize, save etc.) images:
from io import BytesIO
from PIL import Image

# Setting environment variables and/or deleting files:
from os import remove

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

#############################################
# Set longitude, latitude and altitude for
# Kielder observatory location:
#############################################

latitude = 55.2305486
longitude = -2.6054411
altitude = 370


styleSheet = ""

kobs = ephem.Observer()
kobs.lon, kobs.lat = '-2.5881', '55.2330'
kobs.date = datetime.datetime.utcnow()

#Compute Sun Altitude
sol = ephem.Sun()
sol.compute(kobs)

# Return First digit of Sun's altitude
alt = int(str(sol.alt).split(':')[0])

if (alt < -6):
    #read the contents of the dark style sheet for night time
    styleSheet = open("Night_Sky_Style_Dark.css", "r").read()
else:
    #read the contents of the light for day time style sheet
    styleSheet = open("Night_Sky_Style_Light.css", "r").read()

# Current time and date, with Julian date conversion:
currentTime = datetime.datetime.utcnow()
mjd = julian.to_jd(currentTime, fmt='mjd')

# Time and date plus two hours:
timePlusHour  = datetime.datetime.utcnow() + datetime.timedelta(hours = 2)
mjdPlus = julian.to_jd(timePlusHour, fmt='mjd')

gb = pytz.timezone('Europe/London')

currentTime = currentTime.replace(tzinfo=pytz.utc)
currentTime = currentTime.astimezone(tz=gb).strftime("%H:%M (%Z)")
timePlusHour = timePlusHour.replace(tzinfo=pytz.utc)
timePlusHour = timePlusHour.astimezone(tz=gb).strftime("%H:%M (%Z)")

#############################################
# Get live night sky from Heavens Above
# website:
#############################################

# Needs updating every 5 minutes

# Create URL for Kielder specific night sky image at current modified Julian date:
nightSkyNowUrl = "http://www.heavens-above.com/wholeskychart.ashx?lat=" + str(latitude) + "&lng=" + str(longitude) + "&loc=Kielder&alt=" + str(altitude) + "&tz=GMT&size=700&SL=1&SN=1&BW=0&time=" + str(mjd) + "&ecl=1&cb=0"
nightSkyHourUrl = "http://www.heavens-above.com/wholeskychart.ashx?lat=" + str(latitude) + "&lng=" + str(longitude) + "&loc=Kielder&alt=" + str(altitude) + "&tz=GMT&size=700&SL=1&SN=1&BW=0&time=" + str(mjdPlus) + "&ecl=1&cb=0"
"https://www.heavens-above.com/wholeskychart.ashx?lat=55.2323&lng=-2.616&loc=Kielder&alt=378&tz=GMT&size=800&SL=1&SN=1&BW=0&time=58381.77784&ecl=0&cb=0"
# Create Mask to cover heavens-above logo
# Set size of mask:
nightSkyCreditsMaskSize = 113, 9
nightSkyCreditsColour = '#808080'
# Create new RGBA image for mask given size:
nightSkyCreditsMask = Image.new("RGBA", nightSkyCreditsMaskSize, nightSkyCreditsColour)
nightSkyCreditsMask.save("IMG/Night_Sky_Credits_Mask.png")
# Set top left corner of mask position in pixels:
nightSkyCreditsMaskPosition = 584, 687

for url in [nightSkyNowUrl, nightSkyHourUrl]:
    #print(url)
    i = http.request('GET', url)
    img = Image.open(BytesIO(i.data))
# Change blue background colour in image to pure black:
# Convert image to RGB colour space:
    img = img.convert("RGBA")
# Read in pixel colours:
    pixels = img.getdata()
    newPixels = []
# Loop over pixels:
    for pixel in pixels:
# Heavens Above background colour is 0,0,51 in RGB space
        if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 51:
            newPixels.append((0, 0, 0, 0))
        else:
            newPixels.append(pixel)
# Set new pixel array:
    img.putdata(newPixels)
# Paste mask over text region in planets image for both images:
    img.paste(nightSkyCreditsMask, nightSkyCreditsMaskPosition)

# Save new size and colour image:
    if url == nightSkyNowUrl:
        img.save("IMG/Night_Sky_Now.png")
    else:
        img.save("IMG/Night_Sky_Next.png")

# Delete inner/outer/credits mask images now no longer needed:
remove("IMG/Night_Sky_Credits_Mask.png")

# Get sun constellation data from Heavens Above table:
#soup = BeautifulSoup(urlopen(nightSkySunUrl).read())

# Get sunset time:
#sunData = soup.find('span', {'id': 'ctl00_cph1_lblDailyEvents'})
#sunSet = sunData.find_all('td')[25].text
#sunSet = sunSet.encode('ascii','ignore')
#print 'SUNSET: ' + sunSet

# Get civil twilight time:
#civilTwilightData = soup.find('span', {'id': 'ctl00_cph1_lblDailyEvents'})
#civilTwilight = civilTwilightData.find_all('td')[13].text
#civilTwilight = civilTwilight.encode('ascii','ignore')
# May be twilight start time, so if in early hours, try other civil twilight field in table:
#if civilTwilight[0] != '1' or '2':
#  civilTwilight = civilTwilightData.find_all('td')[29].text
#  civilTwilight = civilTwilight.encode('ascii','ignore')
#print 'CIVIL: ' + civilTwilight

# Get astronomical twilight time:
#astroTwilightData = soup.find('span', {'id': 'ctl00_cph1_lblDailyEvents'})
#astroTwilight = astroTwilightData.find_all('td')[5].text
#astroTwilight = astroTwilight.encode('ascii','ignore')
#print 'ASTRO: ' + astroTwilight
# May be twilight start time, so if in early hours, try other civil twilight field in table:
#if astroTwilight[0] != '1' or '2':
#  astroTwilight = astroTwilightData.find_all('td')[37].text
#  astroTwilight = astroTwilight.encode('ascii','ignore')

# Get current constellation of Sun in sky (zodiacal):
#sunConstellation = soup.find_all('a')[7]
#sunConstellation = sunConstellation.getText()


#############################################
# Create an observatory setup for PyEphem:
#############################################

kielderObs = ephem.Observer()

# PyEphem takes and returns only UTC times. Current noon
# is not always UTC noon in Kielder depending on daylight saving:
# Determine if GMT or BST:
now = datetime.datetime.utcnow()

kielderObs.date = now

# Set coordinates as strings for PyEphem:
kielderObs.lat = str(55.2305486)
kielderObs.lon = str(-2.6054411)
kielderObs.elev = 370

# To get U.S. Naval Astronomical Almanac values, use these settings
kielderObs.pressure= 0
kielderObs.horizon = '-0:34'
# (option to set temp./pressure of atmoshphere for refraction
# calculations, but NOAA/USNO ignore this so we will too)


#############################################
# Calculate sunset and various twilight times
# using PyEphem:
#############################################

# Calculature sunrise/noon/sunset times for today:
sunRise = kielderObs.previous_rising(ephem.Sun()) # Sunrise

kielderObs.date = sunRise

sunRise = sunRise.datetime().replace(tzinfo=pytz.utc)

solarNoon = kielderObs.next_transit(ephem.Sun()) # Solar noon
solarNoon = solarNoon.datetime().replace(tzinfo=pytz.utc)

sunSet = kielderObs.next_setting(ephem.Sun()) # Sunset
sunSet = sunSet.datetime().replace(tzinfo=pytz.utc)


# Calculate twilight (civil, nautical, astronomical):
# (relocate the horizon lower for various twilights)

# -6deg beneath horizon is civil twilight:
try:
  kielderObs.horizon = '-6'
  endCivilTwilight = kielderObs.next_setting(ephem.Sun(), use_center = True) # End civil twilight
  endCivilTwilight = endCivilTwilight.datetime().replace(tzinfo=pytz.utc)
except:
  endCivilTwilight = 'N/A'

# -12deg beneath horizon is nautical twilight:
try:
  kielderObs.horizon = '-12'
  endNauticalTwilight = kielderObs.next_setting(ephem.Sun(), use_center = True) # End nautical twilight
  endNauticalTwilight = endNauticalTwilight.datetime().replace(tzinfo=pytz.utc)
# In case it doesn't actually get this dark in summer time:
except:
  endNauticalTwilight = 'N/A'

# -18deg beneath horizon is nautical twilight:
try:
  kielderObs.horizon = '-18'
  endAstronomicalTwilight = kielderObs.next_setting(ephem.Sun(), use_center = True) # Begin astronomical twilight
  endAstronomicalTwilight = endAstronomicalTwilight.datetime().replace(tzinfo=pytz.utc)
except:
  endAstronomicalTwilight = 'N/A'

# Convert times to strings in correct time zone (GMT/BST)
for time in [sunRise, solarNoon, sunSet, endCivilTwilight, endNauticalTwilight, endAstronomicalTwilight]:
    if time == 'N/A':
        continue
    else:
        time = time.astimezone(tz=gb).strftime("%H:%M:%S %Z")

# Calculate current zodiacal constellation (current position of Sun):
s = ephem.Sun()
now = datetime.datetime.utcnow()
s.compute(now)
sunConstellation = ephem.constellation(s)
sunConstellation = sunConstellation[1] # Comes as tuple, e.g. ('Tau', 'Taurus')

# Calculate horoscope constellation based on astrology dates given todays date:
month = int(now.month)
day = int(now.day)
if ((int(month) == 12 and int(day) >= 22) or (int(month) == 1 and int(day) <= 19)):
  zodiacalConstellation = ("Capricorn")
elif ((int(month) == 1 and int(day) >= 20) or (int(month) == 2 and int(day) <= 17)):
  zodiacalConstellation = ("Aquarius")
elif ((int(month) == 2 and int(day) >= 18) or (int(month) == 3 and int(day) <= 19)):
  zodiacalConstellation = ("\n Pisces")
elif ((int(month) == 3 and int(day) >= 20) or (int(month) == 4 and int(day) <= 19)):
  zodiacalConstellation = ("Aries")
elif ((int(month) == 4 and int(day) >= 20) or (int(month) == 5 and int(day) <= 20)):
  zodiacalConstellation = ("Taurus")
elif ((int(month) == 5 and int(day) >= 21) or (int(month) == 6 and int(day) <= 20)):
  zodiacalConstellation = ("Gemini")
elif ((int(month) == 6 and int(day) >= 21) or (int(month) == 7 and int(day) <= 22)):
  zodiacalConstellation = ("Cancer")
elif ((int(month) == 7 and int(day) >= 23) or (int(month) == 8 and int(day) <= 22)):
  zodiacalConstellation = ("Leo")
elif ((int(month) == 8 and int(day) >= 23) or (int(month) == 9 and int(day) <= 22)):
  zodiacalConstellation = ("Virgo")
elif ((int(month) == 9 and int(day) >= 23) or (int(month) ==10 and int(day) <= 22)):
  zodiacalConstellation = ("Libra")
elif ((int(month) == 10 and int(day) >= 23) or (int(month) == 11 and int(day) <= 21)):
  zodiacalConstellation = ("Scorpio")
elif ((int(month) == 11 and int(day) >= 22) or (int(month) == 12 and int(day) <= 21)):
  zodiacalConstellation = ("Sagittarius")

# Compare actual sun constellation with horoscope expectation:
if sunConstellation != zodiacalConstellation:
  zodiacalConstellation = ' (' + str(zodiacalConstellation) + ')*'
  noteColour = '<font color = "red">'
else:
  zodiacalConstellation = ''
  noteColour = '<font color = "black">'


#############################################
# Write data to HTML file:
#############################################

# Open text HTML file (as an overwrite rather than append):
f = open('../Disp.html', 'w+')

# Write HTML href text to first line of new text HTML file:
nightSkyHtml = '''<!DOCTYPE html>
<html>
<title>
The Kielder Night Sky Now
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
<b> The Night Sky Now -
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

<div class = "nightSkyNow">
	<img src = "NIGHT_SKY_INFO_TEST/IMG/Night_Sky_Now.png">
	<div class = "key">Night Sky (''' + currentTime + ''')</div>
</div>

<div class="nightSkyNext">
	<img src = "NIGHT_SKY_INFO_TEST/IMG/Night_Sky_Next.png">
	<div class = "key">Night Sky + 2 Hours (''' + timePlusHour + ''')</div>
</div>

<div class = "note">''' + str(noteColour) + '''*Note: The actual position of the sun is not the horoscope constellation (shown in red in parentheses) for today's date, making astrology complete nonsense!</div>

<div class = "credits">Credit: www.heavens-above.com</div>

<table class = "sunTable">
	<tr>
		<th>Observing<br></th>
	</tr>
	<tr>
		<td id="td01">Solar Noon</td>
	</tr>
	<tr>
		<td id="td02"><i>''' + solarNoon.strftime("%H:%M:%S %Z") + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Sunset</td>
	</tr>
	<tr>
		<td id="td02"><i>''' + sunSet.strftime("%H:%M:%S %Z") + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Civil Twilight</td>
	</tr>
	<tr>
		<td id="td02"><i>''' + endCivilTwilight.strftime("%H:%M:%S %Z") + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Nautical Twilight</td>
	</tr>
	<tr>
		<td id="td02"><i>''' + endNauticalTwilight.strftime("%H:%M:%S %Z") + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Astronomy Twilight</td>
	</tr>
	<tr>
		<td id="td02"><i>''' + endAstronomicalTwilight.strftime("%H:%M:%S %Z") + '''</i></td>
	</tr>
	<tr>
		<td id="td01">Zodiac Constellation</td>
	</tr>
	<tr>
		<td id="td02"><i>''' + str(sunConstellation) + str(noteColour) + str(zodiacalConstellation) + '''</i></td>
	</tr>
</table>

<div class = "kielderLogo">
	<img src = ""NIGHT_SKY_INFO_TEST/IMG/Kielder_Logo.png">
</div>

</body>
</html>'''
f.write(nightSkyHtml)

# Close text file:
f.close()
