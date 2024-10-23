from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import threading
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timestamps.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app)

# Database model for storing timestamps
class Timestamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Timestamp {self.timestamp} - {self.distance}>"

# Initialize the database
with app.app_context():
    db.create_all()

running = False
timestamps = []

def sensor_thread():
    global running, timestamps
    while running:
        # Simulate measuring distance (replace with actual sensor code)
        distance = measure_distance_simulated()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamps.append({"timestamp": timestamp, "distance": distance})

        # Emit the new timestamp to the frontend in real time
        socketio.emit('new_timestamp', {"timestamp": timestamp, "distance": distance})
        time.sleep(1)

def measure_distance_simulated():
    import random
    return round(random.uniform(5, 100), 2)

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
    # Save the timestamps to the database
    for ts in timestamps:
        new_timestamp = Timestamp(timestamp=ts["timestamp"], distance=ts["distance"])
        db.session.add(new_timestamp)
    db.session.commit()
    return jsonify({"status": "stopped"})

@app.route('/history', methods=['GET'])
def get_history():
    history = Timestamp.query.all()
    history_data = [{"timestamp": ts.timestamp, "distance": ts.distance} for ts in history]
    return jsonify(history_data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
