# Christian Amundsen
# Finding thickness from raw data file

import keyboard
import csv
import time

zeroLevel = 0
windowSize = 10

dataStream = [0 for i in range(windowSize)]
list = [0, 0]
movingAvg = 0
state = 1

zMax = 350

raw_data = "Minera4.csv"
csv_file = 'data_height4.csv' 

csv_header = ['time','height']
with open(csv_file, 'w', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(csv_header)

file = open(raw_data)
csvreader = csv.reader(file)

header = []
header = next(csvreader)
header

rows = []
times = []
for row in csvreader:
    rows.append(row[0][2:5]) 
    times.append(row[1])

file.close()


for i in range(len(rows)):

    row = rows[i]
    time = times[i]

    try:
        data = float(row)
    except:
        data = movingAvg
        print("ups")

    dataStream.pop(0)
    dataStream.append(data)

    movingAvg = sum(dataStream)/windowSize
    
    if (zeroLevel == 0) and (0 not in dataStream):
        zeroLevel = movingAvg
        
    if zeroLevel-data < 5:
        zeroLevel = movingAvg

    if zeroLevel > zMax:
        zeroLevel = zMax

    height = zeroLevel - movingAvg
    list.append(height)

    if ((height > 5) and (abs(list[-1] - list[-2]) < 1) 
        and (abs(list[-1] - list[-3]) < 2) and (state == 1)):
        state = 0
        with open(csv_file, 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([round(height), time])


    if height < 5:
        state = 1

    #if movingAvg > 5

    print(height)
    #print(zeroLevel, height)

    if keyboard.is_pressed('q'):
        break
