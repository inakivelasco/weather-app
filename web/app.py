from flask import Flask, render_template
import mysql.connector

app = Flask(__name__, template_folder='templates')

def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user='root',
        password='root',
        database='weather_db'
        )

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
    return render_template("index.html")

@app.route("/legal_note")
def legal_note():
    return render_template("legal_note.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)