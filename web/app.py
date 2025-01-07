from flask import Flask
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user='root',
        password='root',
        database='weather_db'
        )

@app.route("/")
def hello_world():
    connection = get_db_connection()
    cursor =  connection.cursor()

    cursor.execute("SELECT * FROM weather")
    result = cursor.fetchall()
    connection.close()
    return str(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)