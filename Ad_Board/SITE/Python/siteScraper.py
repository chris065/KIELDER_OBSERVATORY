import ephem as e
import datetime
import pytz
import json, requests

date = ""
month = ""
nextMonth = ""
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
year = ""
day = ""
nextDay = ""

date = datetime.datetime.now()
day = date.day
nextDay = day+1
month = months[date.month-1] #-1 becuase it will start at 0
year = date.year

if(day < 10):
    day = "0"+str(day)
if(nextDay < 10):
    nextDay = "0"+str(nextDay)

if(int(nextDay) > 31):
    nextDay = "0"+str(1)
    nextMonth = months[date.month]
    nextDay = str(nextDay)+"("+nextMonth+")"


date = "Tonight: " + str(day)+" - "+str(nextDay)+" "+str(month)+" "+str(year)
#print(date)


#What the temperature feels like (Units: °C)
feelLikeTemp = ""
#What the temperature actually is (Units: °C)
temp = ""
#percipitation probablity  (Units: %)
precip = ""
#The condition code that will corespond to the correct description
weatherCode = ""
#The condition code will map to one of these values
weatherCodeDescs = ["Clear night", "Sunny day", "Partly cloudy (night)", "Partly cloudy (day)", "Not used", "Mist", "Fog", "Cloudy", "Overcast", "Light rain shower (night)",
                    "Light rain shower (day)", "Drizzle", "Light rain", "Heavy rain shower (night)", "Heavy rain shower (day)", "Heavy rain", "Sleet shower (night)", "Sleet shower (day)",
                    "Sleet", "Hail shower (night)", "Hail shower (day)", "Hail", "Light snow shower (night)", "Light snow shower (day)", "Light snow", "Heavy snow shower (night)", "Heavy snow shower (day)",
                    "Heavy snow", "Thunder shower (night)", "Thunder shower (day)", "Thunder"]
#once the condition code has been mapped to the description it
#will be stored in this variable
observation = ""

#making the BST timezone object
bst = pytz.timezone('Europe/London')

obsLat = '55.232302'
obsLon = '-2.616033'

#Setting the OBSERVATORY as the Observer
obs = e.Observer()

obs.lat, obs.lon = obsLat, obsLon
obs.date = datetime.datetime.now()

#Sun values
sunrise = obs.next_rising(e.Sun())
sunset = obs.next_setting(e.Sun())

#Moon values
moonrise = obs.next_rising(e.Moon())
moonset = obs.next_setting(e.Moon())



#dt = datetime.datetime.strptime(str(sunrise), "%Y/%m/%d %H:%M:%S")
#print(dt.time().isoformat())

#Increment all the times by +1 hour to deal with BST
#
#This will eventally change, but this bodge will just have
#to do for now
sunrise = e.Date(sunrise + e.hour)
sunset = e.Date(sunset + e.hour)
moonrise = e.Date(moonrise + e.hour)
moonset = e.Date(moonset + e.hour)

#print("Sunrise: " + str(sunrise))
#print("Sunset: " + str(sunset))
#print("Moonrise: " + str(moonrise))
#print("Moonset: " + str(moonset))

#Take out the date (Y/m/d) element of each value calculated. Leaving just the time
sunrise = datetime.datetime.strptime(str(sunrise), "%Y/%m/%d %H:%M:%S")
sunrise = sunrise.time().isoformat()

sunset = datetime.datetime.strptime(str(sunset), "%Y/%m/%d %H:%M:%S")
sunset = sunset.time().isoformat()

moonrise = datetime.datetime.strptime(str(moonrise), "%Y/%m/%d %H:%M:%S")
moonrise = moonrise.time().isoformat()

moonset = datetime.datetime.strptime(str(moonset), "%Y/%m/%d %H:%M:%S")
moonset = moonset.time().isoformat()

#Code to pull back the weather
def testValues():
    #print the whole JSON array
    #print(weather)
    print("Feels Like: "+ feelLikeTemp +"°C")
    print("Actual Temp: "+ temp +"°C")
    print("Precipitation Probablity: "+ precip + "%")
    print("Observation: " + observation)


weatherDataUrl = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/352090?res=3hourly&key=c5e68363-c162-4e94-8661-bc92d217577a"

jWeather = requests.get(weatherDataUrl)

weather = json.loads(jWeather.text)
#print(weather)

feelLikeTemp = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['F'])
#print("Feels Like: "+ feelLikeTemp +"°C")
temp = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['T'])
#print("Actual Temp: "+ temp +"°C")
precip = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['Pp'])
#print("Precipitation Probablity: "+ precip + "%")
weatherCode = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['W'])
observation = weatherCodeDescs[int(weatherCode)]
#print("Observation: " + observation)

#testValues()


htmlFile = open("../DISPLAY.html", "w+")

#writing the sunrise, moonrise, sunset and the moonset data to the html file
#overwrite the file rather than append to it

htmlFile.write(
'''<!DOCTYPE html>
<html>
  <head>
      <title>AD DISPLAY - KIELDER OBSERVATORY</title>
      <link type="text/css" rel="stylesheet" href="CSS/displayStyle.css"/>
  </head>

  <body>
      <p style="text-align: center;"><img class="logoIMG" src="IMG/logoNew.png"></p>

      <!--Start of code for automatic slide show
          The slide show will change the image every 3 seconds
          The slide show will be used to show light polution-->

          <div class="slideShowContainer">
            <div class="slides fade">
              <img src="IMG/LP_IMAGE.png" style="width: 100%;">
              <div class="text">Image taken in a light polluted enviroment</div>
            </div>

            <div class="slides fade">
              <img src="IMG/LPF_IMAGE.png" style="width: 100%;">
              <div class="text">Image taken in a light pollution free enviroment</div>
            </div>

          </div>

          <script>
          var slideIndex = 0;
          showSlides();

          function showSlides()
          {
            var i;
            var slides = document.getElementsByClassName("slides");
            for (i = 0; i < slides.length; i++)
            {
              slides[i].style.display = "none";
            }
            slideIndex++;
            if (slideIndex > slides.length)
            {
              slideIndex = 1
            }
            slides[slideIndex-1].style.display = "block";
            setTimeout(showSlides, 3000);
          }
          </script>

      <!--End of Code for automatic slide show-->

      <div class="date">
      '''+date+'''
      </div>

      <div class="weatherDataTableDiv">
        <table class="weatherDataTable">
          <tr>
            <th>Feels Like</th>
            <th>Actual Temperature</th>
            <th>Precipitation Probability</th>
            <th>Current Observation</th>
          </tr>
          <tr>
            <!--Insert Feels Like Temp here-->
            <td>'''+str(feelLikeTemp)+''' &deg;C</td>
            <!--Insert Actual Temp here-->
            <td>'''+str(temp)+''' &deg;C</td>
            <!--Insert Precipertaion Probability here-->
            <td>'''+str(precip)+'''&percnt;</td>
            <!--Insert Current Observation here-->
            <td>'''+str(observation)+'''</td>
          </tr>
        </table>
      </div>

        <div class="astroTableDiv">
          <table class="astroTable">
            <tr>
              <th>Sunset</th>
              <th>Moonrise</th>
              <th>Sunrise</th>
              <th>Moonset</th>
            </tr>
            <tr>
              <!--Input time for sunset-->
              <td>'''+str(sunset)+''' BST</td>
              <!--input time for moonrise-->
              <td>'''+str(moonrise)+''' BST</td>
              <!--Input time for sunrise-->
              <td>'''+str(sunrise)+''' BST</td>
              <!--Input time for moonset-->
              <td>'''+str(moonset)+''' BST</td>
            </tr>
          </table>
        </div>

        <div class="eventTableDiv">
          <table class="eventTable">
            <tr>
              <th>Date</th>
              <th>Event Name</th>
              <th>Spaces Available</th>
            </tr>

            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>
            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>
            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>

            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>

            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>

            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>
          </tabel>
        </div>
  </body>
</html>
'''
)
htmlFile.close()
