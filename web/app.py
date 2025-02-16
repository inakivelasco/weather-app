from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template
import os, requests


load_dotenv()

app = Flask(__name__, template_folder='templates')

AEMET_URL = os.getenv('AEMET_URL')
API_KEY = os.getenv('AEMET_APIKEY')

def get_hourly_predictions_url():
    url = f"{AEMET_URL}/api/prediccion/especifica/municipio/horaria/31201?api_key={API_KEY}"
    payload={}
    headers = {
        'accept': 'application/json'
    }

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()['datos']

    return None

def get_temperatures():
    response = requests.get(get_hourly_predictions_url())
    if response.status_code == 200:
        temperatures = []
        dates = []

        for day in response.json()[0]['prediccion']['dia']:    
            for temperature in day['temperatura']:
                dates.append(datetime.strptime(day['fecha'], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=int(temperature['periodo'])))
                temperatures.append(int(temperature['value']))
        
        return temperatures, dates
    return [None], [None]

def plot_temperature():
    import plotly.express as px
    temperatures, dates = get_temperatures()
    
    if temperatures[0] is None:
        return '<p>Error fetching data.</p>'
    
    fig = px.line(
        x=dates, 
        y=temperatures, 
        labels={'x': '', 'y': 'Temperature (°C)'}
    )
    fig.update_layout(
        yaxis_title="Temperature (°C)",
        xaxis=dict(tickangle=-45),
        hovermode="x unified"
    )
    
    return fig.to_html(full_html=False)

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
    plot_html = plot_temperature()
    return render_template("index.html", plot_html=plot_html)

@app.route("/legal_note")
def legal_note():
    return render_template("legal_note.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)