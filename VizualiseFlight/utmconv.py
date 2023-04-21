# import libraries
import matplotlib.pyplot as plt
import numpy as np
from utm import utmconv
from exportkml import kmlclass

## Variables for plotting ##
showPlot = False
longitudeData = []
latitudeData = []
altitudeData = []

fileName = "../input/DJIFlightRecord_2021-03-18_[13-04-51]-TxtLogToCsv.csv"

# open the imu data file
f = open (fileName, "r",encoding="utf8", errors='ignore')

# initialize variables
count = 0

# looping through file


for line in f:
	count += 1

	# Skip the first iterataion with header
	if count == 1:
		continue

	

	# Split the line into CSV formatted data
	csv = line.split(',')
	print(csv[15])
	# Extract Latitude, Longitude and Altitude
	long = float(csv[13])
	lat = float(csv[12])
	alt = float(csv[15])
	
	# In order to show a plot use this function to append your value to a list:
	if(abs(lat) > 0.0001 and abs(long) > 0.0001):
		latitudeData.append(lat)
		longitudeData.append(long)
		altitudeData.append(alt)

	######################################################

# closing the file	
f.close()

n = np.zeros(len(latitudeData))
e = np.zeros(len(latitudeData))
uc = utmconv()

for i in range (len(latitudeData)):
	(hemisphere, zone, letter, e[i], n[i]) = uc.geodetic_to_utm (latitudeData[i],longitudeData[i])

kml = kmlclass()
kml.begin('FlightPath.kml', 'Test Flight for LSDP miniproject 2', 'Plot Positional Flight Data', 0.7)
# color: red,green,blue,cyan,yellow,grey,red_poly,yellow_poly,green_poly
# altitude: use 'absolute' or 'relativeToGround'
kml.trksegbegin ('', '', 'red', 'relative to ground') 
for i in range(len(latitudeData)):
	kml.pt(latitudeData[i], longitudeData[i], altitudeData[i])	
kml.trksegend()
kml.end()


plt.figure()

plt.plot(n,e)
plt.grid()
plt.xlabel('Samples')
plt.ylabel('Angle [°]')
#plt.axis([0,len(gyroData),10,-100])
plt.title('Roll Static')
#plt.savefig('looool.png')
plt.show()

