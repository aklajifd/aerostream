from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_db_data():
    conn = sqlite3.connect('satellite_data.db')
    cursor = conn.cursor()
    # Get the 10 most recent telemetry entries
    cursor.execute("SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    # Main HTML page
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    # Send the raw JSON data to the dashboard
    rows = get_db_data()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, port=5000)