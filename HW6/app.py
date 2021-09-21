import requests, json
from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET','POST'])
def index():
    return app.send_static_file("weatherHomePage.html")
    # elif request.method == "POST":
    #     timeData = request.get_json()
    #     time = timeData[0]['timeSelected']
    #     date = timeData[0]['timeSelected'][0:10]
        
    #     coordinates = request.get_json()[0]['location']
    #     print(coordinates)
        
    #     # params = {
    #     #         'address':add,
    #     #         'key':'AIzaSyBmMjGCQFNUjjLfT649-N2e0-JCK-M5n_I'
    #     # }
    #     # base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    #     # tempResponse = requests.get(base_url, params=params).json()
    #     # print(tempResponse)
    #     # location = tempResponse['results'][0]['geometry']['location']
    #     # print(location)
    #     # lati = location['lat']
    #     # longi = location['lng']
    #     # location_name = tempResponse['results'][0]['formatted_address']
    #     # coordinates = str(lati) + "," + str(longi)

    #     url = "https://api.tomorrow.io/v4/timelines"
    #     querystring = {"location":coordinates, "fields":["temperature","temperatureApparent","temperatureMin","temperatureMax","windSpeed","windDirection","humidity","pressureSeaLevel","uvIndex","weatherCode","precipitationProbability","precipitationType","sunriseTime","sunsetTime","visibility","moonPhase","cloudCover"],"units":"metric","timesteps":["1d"],"timezone":"America/Los_Angeles","apikey":"RtxToEPf66DWW8NrohEt9H0lnpR8xtCA"}
    #     headers = {"Accept": "application/json"}
    #     response = requests.request("GET", url, headers=headers, params=querystring).json()

    #     print(response)
    #     print(time)
    #     print(date)

    #     weather_data_3 = []

    #     for interval in response['data']['timelines']:
    #         for singleEvent in interval['intervals']:
    #             if singleEvent['startTime'][0:10] == date:
    #                 print("HERE!!!!!!")
    #                 weather = {
    #                     'date' : singleEvent['startTime'],
    #                     'weatherCode' : singleEvent['values']['weatherCode'],
    #                     'tempMin' : singleEvent['values']['temperatureMin'],
    #                     'tempMax' : singleEvent['values']['temperatureMax'],
    #                     'precipitationType' : singleEvent['values']['precipitationType'],
    #                     'precipitationProbability' : singleEvent['values']['precipitationProbability'],
    #                     'windSpeed' : singleEvent['values']['windSpeed'],
    #                     'humidity' : singleEvent['values']['humidity'],
    #                     'visibility' : singleEvent['values']['visibility'],
    #                     'sunriseTime' : singleEvent['values']['sunriseTime'],
    #                     'sunsetTime' : singleEvent['values']['sunsetTime'],
    #                 }
    #                 weather_data_3.append(weather)
    #         break

    #     return jsonify({'data': render_template('weatherChart.html', weather_data_3=weather_data_3)})


    # return render_template('weatherHomePage.html')

@app.route("/findWeather", methods=["GET"])
def formSubmit():
    street = request.args.get('address-street')
    city = request.args.get('address-city')
    state = request.args.get('address-state')
    loc = request.args.get('address-coords')
    country = request.args.get('address-country')

    print(loc)

    if(street != None):
        submittedAddress = street + city + state
        params = {
                'address':submittedAddress,
                'key':'AIzaSyBmMjGCQFNUjjLfT649-N2e0-JCK-M5n_I'
        }
        base_url_geolocationAPI = 'https://maps.googleapis.com/maps/api/geocode/json?'
        locationAPIResponse = requests.get(base_url_geolocationAPI, params=params).json()
        locationCoordinates = locationAPIResponse['results'][0]['geometry']['location']
        lati = locationCoordinates['lat']
        longi = locationCoordinates['lng']
        location_name = locationAPIResponse['results'][0]['formatted_address']
        coordinates = str(lati) + "," + str(longi)
    else:
        coordinates = loc
        location_name = city + ", " + state + ", " + country

    base_url_weatherAPI = "https://api.tomorrow.io/v4/timelines"
    querystring = {"location":coordinates, "fields":["temperature","temperatureApparent","temperatureMin","temperatureMax","windSpeed","windDirection","humidity","pressureSeaLevel","uvIndex","weatherCode","precipitationProbability","precipitationType","sunriseTime","sunsetTime","visibility","moonPhase","cloudCover"],"units":"metric","timesteps":["current","1d"],"timezone":"America/Los_Angeles","apikey":"RtxToEPf66DWW8NrohEt9H0lnpR8xtCA"}
    headers = {"Accept": "application/json"}
    weatherAPIResponse = requests.request("GET", base_url_weatherAPI, headers=headers, params=querystring).json()

    weather_data_1 = []
    weather_data_2 = []
    weather_data_3 = []
    count = 0

    for interval in weatherAPIResponse['data']['timelines']:
        count = count+1
        for singleEvent in interval['intervals']:
            if count == 1:
                weather = {
                    'location_name': location_name,
                    'weatherCode' : singleEvent['values']['weatherCode'],
                    'temperature': singleEvent['values']['temperature'],
                    'humidity' : singleEvent['values']['humidity'],
                    'pressureSeaLevel' : singleEvent['values']['pressureSeaLevel'],
                    'windSpeed' : singleEvent['values']['windSpeed'],
                    'visibility' : singleEvent['values']['visibility'],
                    'cloudCover' : singleEvent['values']['cloudCover'],
                    'uvIndex' : singleEvent['values']['uvIndex'],
                }
                weather_data_1.append(weather)
            else:
                weather = {
                    'coordinates' : coordinates,
                    'date' : singleEvent['startTime'],
                    'weatherCode' : singleEvent['values']['weatherCode'],
                    'tempMin' : singleEvent['values']['temperatureMin'],
                    'tempMax' : singleEvent['values']['temperatureMax'],
                    'windSpeed' : singleEvent['values']['windSpeed'],
                }
                weather_data_2.append(weather)

                weather_2 = {
                    'date' : singleEvent['startTime'],
                    'weatherCode' : singleEvent['values']['weatherCode'],
                    'tempMin' : singleEvent['values']['temperatureMin'],
                    'tempMax' : singleEvent['values']['temperatureMax'],
                    'precipitationType' : singleEvent['values']['precipitationType'],
                    'precipitationProbability' : singleEvent['values']['precipitationProbability'],
                    'windSpeed' : singleEvent['values']['windSpeed'],
                    'humidity' : singleEvent['values']['humidity'],
                    'visibility' : singleEvent['values']['visibility'],
                    'sunriseTime' : singleEvent['values']['sunriseTime'],
                    'sunsetTime' : singleEvent['values']['sunsetTime'],
                }
                weather_data_3.append(weather_2)

    final_response = {}
    final_response['current'] = weather_data_1
    final_response['oneday'] = weather_data_2
    final_response['oneday_2'] = weather_data_3
    print(final_response)   
    res = jsonify(final_response)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res


if __name__ == "__main__":
    app.run()




    # R2cChkU3mSRBSiseul2jBg1H3sRmImRt
    # RtxToEPf66DWW8NrohEt9H0lnpR8xtCA

    # 7c350f6f9be9c0 - https://ipinfo.io/?token=7c350f6f9be9c0