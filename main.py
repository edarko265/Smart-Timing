from flask import Flask, render_template, jsonify
import threading
import time
from datetime import datetime
from Usonic_test import measure_distance

app = Flask(__name__)
timestamps = []
running = False

def sensor_thread():
    global running, timestamps
    while running:
        # Replace this with your real sensor measurement function
        distance = measure_distance()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamps.append({"timestamp": timestamp, "distance": distance})
        time.sleep(1)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_sensor():
    global running
    if not running:
        running = True
        threading.Thread(target=sensor_thread).start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop_sensor():
    global running
    running = False
    return jsonify({"status": "stopped", "history": timestamps})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(timestamps)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
