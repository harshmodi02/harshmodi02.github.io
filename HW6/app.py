import requests, json
from flask import Flask, redirect, url_for, render_template, request, jsonify

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET','POST'])
def index():
    
    if request.method == "POST":
        location_coordinates = request.get_json()
        lati = location_coordinates[0]['location']['lat']
        longi = location_coordinates[0]['location']['lng']
        coordinates = str(lati) + "," + str(longi)
        print(type(coordinates))
        print(coordinates)
        url = "https://api.tomorrow.io/v4/timelines"

        querystring1 = {"location":coordinates, "fields":["temperature","temperatureApparent","temperatureMin","temperatureMax","windSpeed","windDirection","humidity","pressureSeaLevel","uvIndex","weatherCode","precipitationProbability","precipitationType","visibility","cloudCover"],"units":"metric","timesteps":"1d","apikey":"RtxToEPf66DWW8NrohEt9H0lnpR8xtCA"}
        querystring2 = {"location":coordinates, "fields":["temperature","temperatureApparent","temperatureMin","temperatureMax","windSpeed","windDirection","humidity","pressureSeaLevel","uvIndex","weatherCode","precipitationProbability","precipitationType","visibility","cloudCover"],"units":"metric","timesteps":"current","apikey":"RtxToEPf66DWW8NrohEt9H0lnpR8xtCA"}

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers, params=querystring1).json()
        response2 = requests.request("GET", url, headers=headers, params=querystring2).json()
        print(response2)
        weather_data_1 = []
        weather_data_2 = []
        for interval in response['data']['timelines']:
            for singleEvent in interval['intervals']:
                weather = {
                    'date' : singleEvent['startTime'],
                    'weatherCode' : singleEvent['values']['weatherCode'],
                    'tempMin' : singleEvent['values']['temperatureMin'],
                    'tempMax' : singleEvent['values']['temperatureMax'],
                    'windSpeed' : singleEvent['values']['windSpeed']
                }
                weather_data_1.append(weather)

        print(weather_data_1)

        for interval in response2['data']['timelines']:
            for singleEvent in interval['intervals']:
                weather = {
                    'temperature': singleEvent['values']['temperature'],
                    'weatherCode' : singleEvent['values']['weatherCode'],
                    'humidity' : singleEvent['values']['humidity'],
                    'pressureSeaLevel' : singleEvent['values']['pressureSeaLevel'],
                    'windSpeed' : singleEvent['values']['windSpeed'],
                    'visibility' : singleEvent['values']['visibility'],
                    'cloudCover' : singleEvent['values']['cloudCover'],
                    'uvIndex' : singleEvent['values']['uvIndex'],
                }
                weather_data_2.append(weather)

        print(weather_data_2)
        return jsonify({'data': render_template('weatherTable.html', weather_data_1=weather_data_1, weather_data_2=weather_data_2)})

    return render_template('weatherHomePage.html')

if __name__ == "__main__":
    app.run()