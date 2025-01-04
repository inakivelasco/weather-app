from flask import Flask
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='notes_db'
        )

@app.route("/")
def hello_world():
    connection = get_db_connection()
    cursor =  connection.cursor()

    cursor.execute("SELECT 'Hello, World!'")
    result = cursor.fetchone()
    connection.close()
    return str(result[0])

if __name__ == "__main__":
    app.run(host='0.0.0.0')