# Christian Amundsen
# Sorting stones based on thickness, area and shape

import numpy as np
#import datetime 
import csv
import matplotlib.pyplot as plt

paths = ["data1.csv", "data2.csv", "data3.csv", "data4.csv"]
output = "sorted_data.csv"

zeroHeight = 0

##################################################################

##################################################################
# Function for sorting the stones

def sortStone(area, shape, shortside, height):
    if shape == "irregular":
        if (area >= 0.100) and (area < 0.200):
            if   (height >= 10) and (height < 20): product = "s1020"
            elif (height >= 20) and (height < 30): product = "s2030"
            elif (height >= 30) and (height < 40): product = "s3040"
            else:                                  product = "s"
        elif (area >= 0.200) and (area < 0.500):
            if   (height >= 10) and (height < 20): product = "m1020"
            elif (height >= 20) and (height < 30): product = "m2030"
            elif (height >= 30) and (height < 40): product = "m3040"
            elif (height >= 40) and (height < 60): product = "m4060"
            else:                                  product = "m"
        elif (area >= 0.500) and (area < 1.200):
            if   (height >= 10) and (height < 20): product = "l1020"
            elif (height >= 20) and (height < 30): product = "l2030"
            elif (height >= 30) and (height < 40): product = "l3040"
            else:                                  product = "l"
        else:                                      product = "irr"

    elif shape == "rectangular":
        if   (shortside >= 112) and (shortside < 137):
            if   (height >= 15) and (height < 25): product = "w125_h1525"
            else:                                  product = "w125"
        elif (shortside >= 137) and (shortside < 162):
            if   (height >= 15) and (height < 25): product = "w150_h1525"
            else:                                  product = "w150"
        elif (shortside >= 162) and (shortside < 187):
            if   (height >= 15) and (height < 25): product = "w175_h1525"
            else:                                  product = "w175"
        elif (shortside >= 187) and (shortside < 212):
            if   (height >= 15) and (height < 25): product = "w200_h1525"
            else:                                  product = "w200"
        elif (shortside >= 212) and (shortside < 237):
            if   (height >= 15) and (height < 25): product = "w225_h1525"
            else:                                  product = "w225"
        elif (shortside >= 237) and (shortside < 275):
            if   (height >= 15) and (height < 25): product = "w250_h1525"
            elif (height >= 25) and (height < 40): product = "w250_h2540"
            else:                                  product = "w250"

        elif (shortside >= 275) and (shortside < 312):
            if   (height >= 10) and (height < 20): product = "w300_h1020"
            elif (height >= 20) and (height < 30): product = "w300_h2030"
            elif (height >= 30) and (height < 40): product = "w300_h3040"
            else:                                  product = "w300"
        elif (shortside >= 312) and (shortside < 337):
            if   (height >= 20) and (height < 30): product = "w325_h2030"
            elif (height >= 30) and (height < 40): product = "w325_h3040"
            else:                                  product = "w325"
        elif (shortside >= 337) and (shortside < 375):
            if   (height >= 20) and (height < 30): product = "w350_h2030"
            elif (height >= 30) and (height < 40): product = "w350_h3040"
            else:                                  product = "w350"

        elif (shortside >= 375) and (shortside < 450):
            if   (height >= 10) and (height < 20): product = "w400_h1020"
            elif (height >= 20) and (height < 30): product = "w400_h2030"
            elif (height >= 30) and (height < 40): product = "w400_h3040"
            else:                                  product = "w400"
        elif (shortside >= 450) and (shortside < 550):
            if   (height >= 20) and (height < 30): product = "w500_h2030"
            elif (height >= 30) and (height < 40): product = "w500_h3040"
            else:                                  product = "w500"
        elif (shortside >= 550) and (shortside < 650):
            if   (height >= 20) and (height < 40): product = "w600_h2040"
            else:                                  product = "w600"
        else:                                      product = "rec"

    return product

##################################################################
# Creating a database for all stones

stones = []

for i in range(4):
    path = paths[i]

    file = open(path)
    csvreader = csv.reader(file)

    header = []
    header = next(csvreader)
    header

    for row in csvreader:
        area      = float(row[2])
        shape     = row[3]
        shortside = float(row[4])
        longside  = float(row[5]) / 1000
        height    = int(row[6])
        batch     = i + 1

        stone = [area, shape, shortside, longside, height, batch]
        stones.append(stone)

        if height == 0: zeroHeight += 1

    file.close()

##################################################################
# Sorting all stones

total  = {}
batch1 = {}
batch2 = {}
batch3 = {}
batch4 = {}

for stone in stones:

    area      = stone[0]
    shape     = stone[1]
    shortside = stone[2]
    longside  = stone[3]
    height    = stone[4]
    batch     = stone[5]
    product = sortStone(area, shape, shortside, height)

    #if shape == "irregular":
    if shape == "rectangular":
    #if True:
        if product not in total.keys(): total[product]  = 0

    
    #if shape == "irregular":   total[product] += area
    if shape == "rectangular": total[product] += area

    total = dict(sorted(total.items()))
##################################################################
# Real data from Minera

sold = {
     "s1020":40
    ,"s2030":30
    ,"s3040":20

    ,"m1020":120
    ,"m2030":120
    ,"m3040":10
    ,"m4060":10

    ,"l1020":0
    ,"l2030":105
    ,"l3040":0
}

##################################################################

total_measured = sum(total.values())
total_sold     = sum( sold.values())

print(total_measured)
print(total_sold)
print(zeroHeight)

##################################################################
# Simple plotting

# Creating the dataset
data = total
courses = list(data.keys())
values = list(data.values())

plt.rcParams['toolbar'] = 'None'

# Creating the figure
fig = plt.figure(figsize = (10, 6))

plt.bar(courses, values, width = 0.4)
plt.xticks(rotation=90)

plt.xlabel("Product category")
plt.ylabel("Area detected [m2]")
#plt.title("Production of flagstone")
plt.show()

##################################################################
# Plot by batch
"""
# Creating the dataset
products = total.keys()
values = {"batch1":list(batch1.values())
         ,"batch2":list(batch2.values())
         ,"batch3":list(batch3.values())
         ,"batch4":list(batch4.values())}

# Creating the figure
bar_width = 0.2
fig, ax = plt.subplots()
x_pos = np.arange(len(products)) 

for i, (group, values) in enumerate(values.items()):
   pos = x_pos + (i * bar_width)
   ax.bar(pos, values, width=bar_width, label=group)

ax.set_xticks(x_pos + ((len(values) - 1) / 2 - 4.5) * bar_width)
ax.set_xticklabels(products)

plt.xticks(rotation=90)
ax.legend()
plt.xlabel("Product category")
plt.ylabel("Area produced [m2]")
plt.title("Production of flagstone")
plt.show()
"""
##################################################################
# Ploting against data
"""
t = {}
s = {}

for key in total.keys():
    total1 = total[key]
    if key in sold.keys(): sold1 = sold[key]
    else: sold1 = 0
    t[key], s[key] = total1, sold1

products = t.keys()
values = {"total":list(t.values())
         ,"sold":list(s.values())}

# Creating the figure
bar_width = 0.2
fig, ax = plt.subplots()
x_pos = np.arange(len(products)) 

for i, (group, values) in enumerate(values.items()):
   pos = x_pos + (i * bar_width)
   ax.bar(pos, values, width=bar_width, label=group)

ax.set_xticks(x_pos + ((len(values) - 1) / 2 - 4.5) * bar_width)
ax.set_xticklabels(products)

plt.xticks(rotation=90)
ax.legend()
plt.xlabel("Product category")
plt.ylabel("Area produced [m2]")
plt.title("Production of flagstone")
plt.show()

"""
##################################################################

