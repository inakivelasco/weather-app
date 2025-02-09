from flask import Flask, render_template, Response
import os, requests
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from io import BytesIO
import sys
from pathlib import Path



# load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__, template_folder='templates')

load_dotenv('../.env')

aemet_url = 'https://opendata.aemet.es/opendata'

API_KEY = os.getenv('AEMET_APIKEY')

print(os.environ)
print('asdf', file=sys.stderr)
print(API_KEY, file=sys.stderr)
API_KEY='' # TODO

def get_hourly_predictions_url():
    url = f"{aemet_url}/api/prediccion/especifica/municipio/horaria/31201?api_key={API_KEY}"

    payload={}
    headers = {
        'accept': 'application/json'
    }

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()['datos']

    return None

def get_temperature():
    response = requests.get(get_hourly_predictions_url())
    if response.status_code == 200:
        temperatures = []

        for day in response.json()[0]['prediccion']['dia']:

            for temperature in day['temperatura']:
                temperatures.append(temperature['value'])

    return [None]

def plot_temperature():
    temperatures = get_temperature()

    temperatures = [1,2,3,4,5]

    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.plot(temperatures, temperatures, marker='o', linestyle='-', color='b', label="Temperature (°C)")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Forecast for the Next 48 Hours")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    # Save the plot to a BytesIO object instead of a file
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Rewind the BytesIO object
    plt.close()
    
    return img

# def get_db_connection():
#  import mysql.connector
#     return mysql.connector.connect(
#         host='db',
#         user='root',
#         password='root',
#         database='weather_db'
#         )

# @app.route("/")
# def hello_world():
#     connection = get_db_connection()
#     cursor =  connection.cursor()

#     cursor.execute("SELECT * FROM weather")
#     result = cursor.fetchall()
#     connection.close()
#     return str(result)

@app.route("/")
def home():
    # return render_template("index.html")
    img = plot_temperature()
    return Response(img, mimetype='image/png')

@app.route("/legal_note")
def legal_note():
    return render_template("legal_note.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)