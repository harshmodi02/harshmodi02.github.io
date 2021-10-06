import requests, json
from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET','POST'])
def index():
    return app.send_static_file("weatherHomePage.html")


@app.route("/findWeather", methods=["GET"])
def formSubmit():
    street = request.args.get('address-street')
    city = request.args.get('address-city')
    state = request.args.get('address-state')
    loc = request.args.get('address-coords')
    country = request.args.get('address-country')

    if(street != None):
        submittedAddress = street + city + state
        params = {
                'address':submittedAddress,
                'key':'AIzaSyBmMjGCQFNUjjLfT649-N2e0-JCK-M5n_I'
        }
        base_url_geolocationAPI = 'https://maps.googleapis.com/maps/api/geocode/json?'
        locationAPIResponse = requests.get(base_url_geolocationAPI, params=params).json()
        status = locationAPIResponse['status']
        if status == "OK":
            locationCoordinates = locationAPIResponse['results'][0]['geometry']['location']
            lati = locationCoordinates['lat']
            longi = locationCoordinates['lng']
            location_name = locationAPIResponse['results'][0]['formatted_address']
            coordinates = str(lati) + "," + str(longi)
        else:
            final_response = {}
            final_response['status'] = "Error"
            return final_response
    else:
        coordinates = loc
        location_name = city + ", " + state + ", " + country

    base_url_weatherAPI = "https://api.tomorrow.io/v4/timelines"
    querystring = {"location":coordinates, "fields":["temperature","temperatureApparent","temperatureMin","temperatureMax","windSpeed","windDirection","humidity","pressureSeaLevel","uvIndex","weatherCode","precipitationProbability","precipitationType","sunriseTime","sunsetTime","visibility","moonPhase","cloudCover"],"units":"imperial","timesteps":["current","1d","1h"],"timezone":"America/Los_Angeles","apikey":"R2cChkU3mSRBSiseul2jBg1H3sRmImRt"}
    headers = {"Accept": "application/json"}
    weatherAPIResponse = requests.request("GET", base_url_weatherAPI, headers=headers, params=querystring).json()
    if 'type' in weatherAPIResponse:
        if weatherAPIResponse['type'] == 429:
            final_response = {}
            final_response['status'] = "Error"
            return final_response

    weather_data_1 = []
    weather_data_2 = []
    weather_data_3 = []
    weather_data_4 = []
    weather_data_5 = []
    count = 0

    weatherCodeDescriptionImageMapping = {
        "4201": ('Heavy Rain','static/images/rain_heavy.svg'),
        "4001": ('Rain','static/images/rain.svg'),
        "4200": ('Ligh Rain','static/images/rain_light.svg'),
        "6201": ('Heavy Freezing Rain','static/images/freezing_rain_heavy.svg'),
        "6001": ('Freezing Rain','static/images/freezing_rain.svg'),
        "6200": ('Light Freezing Rain','static/images/freezing_rain_light.svg'),
        "6000": ('Freezing Drizzle','static/images/freezing_drizzle.svg'),
        "4000": ('Drizzle','static/images/drizzle.svg'),
        "7101": ('Heavy Ice Pellets','static/images/ice_pellets_heavy.svg'),
        "7000": ('Ice Pellets','static/images/ice_pellets.svg'),
        "7102": ('Light Ice Pellets','static/images/ice_pellets_light.svg'),
        "5101": ('Heavy Snow','static/images/snow_heavy.svg'),
        "5000": ('Snow','static/images/snow.svg'),
        "5100": ('Light Snow','static/images/snow_light.svg'),
        "5001": ('Flurries','static/images/flurries.svg'),
        "8000": ('Thunderstrom','static/images/tstorm.svg'),
        "2100": ('Light Fog','static/images/fog_light.svg'),
        "2000": ('Fog','static/images/fog.svg'),
        "1001": ('Cloudy','static/images/cloudy.svg'),
        "1102": ('Mostly Cloudy','static/images/mostly_cloudy.svg'),
        "1101": ('Partly Cloudy','static/images/partly_cloudy_day.svg'),
        "1100": ('Mostly Clear','static/images/mostly_clear_day.svg'),
        "1000": ('Clear','static/images/clear_day.svg'),
    }

    weatherPrecipitationTypeMapping = {
      "0": "N/A",
      "1": "Rain",
      "2": "Snow",
      "3": "Freezing Rain",
      "4": "Ice Pellets"
    }

    for interval in weatherAPIResponse['data']['timelines']:
        count = count+1
        for singleEvent in interval['intervals']:
            if count == 1:
                weather = {
                    'location_name': location_name,
                    'weatherCode' : weatherCodeDescriptionImageMapping[str(singleEvent['values']['weatherCode'])],
                    'temperature': singleEvent['values']['temperature'],
                    'humidity' : singleEvent['values']['humidity'],
                    'pressureSeaLevel' : singleEvent['values']['pressureSeaLevel'],
                    'windSpeed' : singleEvent['values']['windSpeed'],
                    'visibility' : singleEvent['values']['visibility'],
                    'cloudCover' : singleEvent['values']['cloudCover'],
                    'uvIndex' : singleEvent['values']['uvIndex'],
                }
                weather_data_1.append(weather)
            elif count == 2:
                weather = {
                    'coordinates' : coordinates,
                    'date' : singleEvent['startTime'],
                    'weatherCode' : weatherCodeDescriptionImageMapping[str(singleEvent['values']['weatherCode'])],
                    'tempMin' : singleEvent['values']['temperatureMin'],
                    'tempMax' : singleEvent['values']['temperatureMax'],
                    'windSpeed' : singleEvent['values']['windSpeed'],
                }
                weather_data_2.append(weather)

                weather_3 = {
                    'date' : singleEvent['startTime'],
                    'weatherCode' : weatherCodeDescriptionImageMapping[str(singleEvent['values']['weatherCode'])],
                    'tempMin' : singleEvent['values']['temperatureMin'],
                    'tempMax' : singleEvent['values']['temperatureMax'],
                    'precipitationType' : weatherPrecipitationTypeMapping[str(singleEvent['values']['precipitationType'])],
                    'precipitationProbability' : singleEvent['values']['precipitationProbability'],
                    'windSpeed' : singleEvent['values']['windSpeed'],
                    'humidity' : singleEvent['values']['humidity'],
                    'visibility' : singleEvent['values']['visibility'],
                    'sunriseTime' : singleEvent['values']['sunriseTime'],
                    'sunsetTime' : singleEvent['values']['sunsetTime'],
                }
                weather_data_3.append(weather_3)

                dateObj = datetime.strptime(singleEvent['startTime'],'%Y-%m-%dT%H:%M:%S%z')
                dateInMilliseconds = dateObj.timestamp() * 1000
                weather_4 = [dateInMilliseconds,singleEvent['values']['temperatureMin'],singleEvent['values']['temperatureMax']]
                weather_data_4.append(weather_4)
            else:
                weather_5 = {
                    'date' : singleEvent['startTime'],
                    'temperature' : singleEvent['values']['temperature'],
                    'humidity' : singleEvent['values']['humidity'],
                    'windSpeed' : singleEvent['values']['windSpeed'],
                    'windDirection' : singleEvent['values']['windDirection'],
                    'pressureSeaLevel' : singleEvent['values']['pressureSeaLevel'],
                }
                weather_data_5.append(weather_5)

    final_response = {}
    final_response['status'] = "OK"
    final_response['current'] = weather_data_1
    final_response['oneday'] = weather_data_2
    final_response['oneday_2'] = weather_data_3
    final_response['oneday_3'] = weather_data_4
    final_response['onehour'] = weather_data_5
    res = jsonify(final_response)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res


if __name__ == "__main__":
    app.run()




    # R2cChkU3mSRBSiseul2jBg1H3sRmImRt
    # RtxToEPf66DWW8NrohEt9H0lnpR8xtCA

    # 7c350f6f9be9c0 - https://ipinfo.io/?token=7c350f6f9be9c0