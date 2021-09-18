import requests, json
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    # url = "https://api.tomorrow.io/v4/timelines"

    # querystring = {"location":"-73.98529171943665,40.75872069597532", "fields":["temperature","temperatureApparent","temperatureMin","temperatureMax","windSpeed","windDirection","humidity","pressureSeaLevel","uvIndex","weatherCode","precipitationProbability","precipitationType","visibility","cloudCover"],"units":"metric","timesteps":"1d","apikey":"RtxToEPf66DWW8NrohEt9H0lnpR8xtCA"}

    # headers = {"Accept": "application/json"}

    # response = requests.request("GET", url, headers=headers, params=querystring).json()

    weather_data = []
    
    # for interval in response['data']['timelines']:
    #     for singleEvent in interval['intervals']:
    #         weather = {
    #             'date' : singleEvent['startTime'],
    #             'weatherCode' : singleEvent['values']['weatherCode'],
    #             'tempMin' : singleEvent['values']['temperatureMin'],
    #             'tempMax' : singleEvent['values']['temperatureMax'],
    #             'windSpeed' : singleEvent['values']['windSpeed']
    #         }
    #         weather_data.append(weather)

    return render_template('weatherHomePage.html',weather_data=weather_data)

if __name__ == "__main__":
    app.run()