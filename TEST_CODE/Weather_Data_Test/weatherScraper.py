import json, requests

def testValues():
    #print the whole JSON array
    #print(weather)
    print("Feels Like: "+ feelLikeTemp +"°C")
    print("Actual Temp: "+ temp +"°C")
    print("Precipitation Probablity: "+ precip + "%")
    print("Observation: " + observation)
    print("Location: "+location)


#What the temperature feels like (Units: °C)
feelLikeTemp = ""
#What the temperature actually is (Units: °C)
temp = ""
#percipitation probablity  (Units: %)
precip = ""
#Location of where the requested data is for
location = ""
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
location = (weather['SiteRep']['DV']['Location']['name']).title() #.title() will change the first letter to upper case and the rest to lower
#print("Location: "+location)

htmlFile = open("Weather_Display.html", "w+")

htmlFile.write('''<!DOCTYPE html>
<html>
  <head>
    <title>KIELDER WEATHER DISPLAY</title>
    <link rel="stylesheet" type="text/css" href="CSS/weatherStyle.css">
  </head>

  <body>
    <h1>Weather - '''+location+'''</h1>

    <div class="weatherData">
      <div id="feelsLikeTemp">
        Feels like: <b>'''+feelLikeTemp+'''˚C</b>
      </div>

      <div id="temp">
        Actual Temp: <b>'''+temp+'''°C</b>
      </div>

      <div id="precip">
        Precipitation Probablity: <b>'''+precip+'''%</b>
      </div>

      <div id="observation">
        Current Observation: <b>'''+observation+'''</b>
      </div>
    </div>
  </body>
</html>

''')

htmlFile.close()

testValues()
