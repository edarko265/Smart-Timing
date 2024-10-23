import RPi.GPIO as GPIO
import time
from datetime import datetime

# Set up the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define the GPIO pins for the trigger and echo
TRIG_PIN = 18
ECHO_PIN = 16

# Set up the GPIO pins
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    # Ensure the trigger pin is low
    GPIO.output(TRIG_PIN, False)
    time.sleep(2)

    # Send a pulse to the sensor
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)  # Pulse duration of 10 microseconds
    GPIO.output(TRIG_PIN, False)

    # Measure the time it takes for the echo to be received
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate the distance based on the time difference
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is ~34300 cm/s, so half of that for round trip

    return round(distance, 2)

try:
    while True:
        dist = measure_distance()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Object Distance: {dist} cm | Timestamp: {timestamp}")
        time.sleep(10)  # Wait a bit before the next reading

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()  # Reset GPIO settings
