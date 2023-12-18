# Christian Amundsen

# Logging data from Arduino to CSV file through serial communication

import serial
import csv
import keyboard
import datetime

arduino = serial.Serial(port='COM5', baudrate=9600)  # Port name 

csv_file = 'raw_data.csv'  
csv_header = ['data', 'time']
with open(csv_file, 'w', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(csv_header)

while True:
    data = arduino.readline()
    time = datetime.datetime.now().strftime("%H:%M:%S")

    with open(csv_file, 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([data, time])

    print(data)

    if keyboard.is_pressed('q'):
        break