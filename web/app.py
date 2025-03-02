from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from PIL import Image
import base64, io, os, requests, logging
import plotly.express as px
import mysql.connector
from mysql.connector import Error


load_dotenv()

app = Flask(__name__, template_folder='templates')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

AEMET_URL = os.getenv('AEMET_URL')
API_KEY = os.getenv('AEMET_APIKEY')

def get_hourly_predictions_url():
    """Fetch and return the AEMET API URL for hourly predictions."""
    url = f"{AEMET_URL}/api/prediccion/especifica/municipio/horaria/31201?api_key={API_KEY}"
    headers = {'accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers, data={})
        response.raise_for_status()
        return response.json()['datos']
    except requests.RequestException as e:
        logger.error(f"Error fetching predictions URL: {e}")
        return None

def get_temperatures():
    """Fetch temperature data and corresponding dates from AEMET."""
    predictions_url = get_hourly_predictions_url()
    if not predictions_url:
        return [None], [None]
    
    try:
        response = requests.get(predictions_url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching temperature data: {e}")
        return [None], [None]
    
    temperatures = []
    dates = []
    try:
        for day in response.json()[0]['prediccion']['dia']:
            base_date = datetime.strptime(day['fecha'], "%Y-%m-%dT%H:%M:%S")
            for temperature in day['temperatura']:
                hour_offset = int(temperature['periodo'])
                dates.append(base_date + timedelta(hours=hour_offset))
                temperatures.append(int(temperature['value']))
        return temperatures, dates
    except (KeyError, ValueError) as e:
        logger.error(f"Error processing temperature data: {e}")
        return [None], [None]

def plot_temperature():
    """Generate an interactive Plotly line graph for temperature forecast."""
    temperatures, dates = get_temperatures()
    if temperatures[0] is None:
        return '<p>Error fetching data.</p>'
    
    fig = px.line(
        x=dates, 
        y=temperatures, 
        labels={'x': '', 'y': 'Temperature (°C)'},
    )
    fig.update_layout(
        yaxis_title="Temperature (°C)",
        xaxis=dict(tickangle=-45),
        hovermode="x unified",
        template="plotly_white"
    )
    
    return fig.to_html(full_html=False)

def get_analysis_map():
    """Fetch and rotate the analysis map from AEMET, returning it as a Base64 string."""
    url = f"{AEMET_URL}/api/mapasygraficos/analisis?api_key={API_KEY}"
    headers = {'accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers, data={})
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching analysis map URL: {e}")
        return None

    try:
        map_url = response.json()['datos']
        map_response = requests.get(map_url)
        map_response.raise_for_status()
        image = Image.open(io.BytesIO(map_response.content))
        rotated_image = image.rotate(-90, expand=True)
        buffer = io.BytesIO()
        rotated_image.save(buffer, format="PNG")
        buffer.seek(0)
        analysis_map = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return analysis_map
    except Exception as e:
        logger.error(f"Error processing analysis map: {e}")
        return None

def get_db_connection():
    """Return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host='db',
            user='root',
            password='root',
            database='weather_db'
        )
        return connection
    except Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def get_feedbacks():
    """Retrieve feedback entries from the database."""
    connection = get_db_connection()
    if connection is None:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT rating, comment, timestamp FROM feedback ORDER BY timestamp DESC")
            feedbacks = cursor.fetchall()
        return feedbacks
    except Error as e:
        logger.error(f"Error fetching feedbacks: {e}")
        return []
    finally:
        connection.close()

@app.route("/")
def home():
    """Render the homepage with temperature plot, analysis map, and feedbacks."""
    plot_html = plot_temperature()
    analysis_map = get_analysis_map()
    feedbacks = get_feedbacks()
    return render_template("index.html", plot_html=plot_html, analysis_map=analysis_map, feedbacks=feedbacks)

@app.route("/legal_note")
def legal_note():
    """Render the legal note page."""
    return render_template("legal_note.html")

@app.route("/feedback", methods=['POST'])
def submit_feedback():
    """Insert feedback data into the database and return the new entry as JSON."""
    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment')
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed."}), 500
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO feedback (rating, comment) VALUES (%s, %s)"
            cursor.execute(sql, (rating, comment))
            connection.commit()
    except Error as e:
        logger.error(f"Error inserting feedback: {e}")
        return jsonify({"error": "Failed to insert feedback."}), 500
    finally:
        connection.close()
    
    feedback_entry = {
        'rating': rating,
        'comment': comment,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return jsonify(feedback_entry), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)