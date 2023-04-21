# Import the necessary packages
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from VizualiseFlight.utm import utmconv
from VizualiseFlight.exportkml import kmlclass

def EriksFunction(fileName:str):
    ## Variables for plotting ##
    showPlot = False
    longitudeData:list = []
    latitudeData:list = []
    altitudeData:list = []

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
        if (csv[2] == "Stop"):
            break
        elif (csv[2] != "Recording" ):
            continue
                
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

    return list(e), list(n), altitudeData



# Create a 3d plot of the flight path
def plot_flight_path(utm_eastings:list, utm_northings:list, utm_altitudes:list) -> None:
    """Plot the flight path of the drone in 3d space.

    Args:
        utm_eastings (list): List of UTM eastings.
        utm_northings (list): List of UTM northings.
        utm_altitudes (list): List of UTM altitudes.
    """
    assert type(utm_eastings) == list and type(utm_northings) == list and type(utm_altitudes) == list
    assert len(utm_eastings) > 0 and len(utm_northings) > 0 and len(utm_altitudes) > 0
    assert len(utm_eastings) == len(utm_northings) == len(utm_altitudes)

    fig = plt.figure()    
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(utm_eastings, utm_northings, utm_altitudes)
    ax.axis('equal')
    ax.set_xlabel('UTM Eastings [m]')
    ax.set_ylabel('UTM Northings [m]')
    ax.set_zlabel('UTM Altitudes [m]')
    ax.set_title('Flight Path')
    plt.savefig('output/flight_path_3d.svg', format='svg')

    fig = plt.figure()
    ax = fig.add_subplot(1, 1 ,1)
    ax.plot(utm_eastings, utm_northings)
    ax.axis('equal')
    ax.set_xlabel('UTM Eastings [m]')
    ax.set_ylabel('UTM Northings [m]')
    ax.set_title('Flight Path')
    plt.savefig('output/flight_path_2d.svg', format='svg')

# Call the main function
if __name__ == '__main__':
    """
    Task
        Investigate the contents of the logfile, please pay at-
        tention to what values are present in the logfile. Ex-
        tract the GPS coordinates of the UAV during record-
        ing of the first video. Convert the GPS coordinates
        to UTM and visualize the flight path.
    """
    
    # Read the logfile
    utm_eastings, utm_northings, utm_altitudes =  EriksFunction("dataset/DJIFlightRecord_2021-03-18_[13-04-51]-TxtLogToCsv.csv")

    # Plot the flight path
    plot_flight_path(utm_eastings, utm_northings, utm_altitudes)


    """
    Task
        Make a python program that goes through all frames
        in the video one by one and saves every 50th frame
        to disc. Ensure that they are named in a consistent
        way that maintains their order from the video. Ex-
        clude the first 1200 frames of the video. These saved
        frames will be used in the rest of the project.
    """

    # TODO code here 
    pass


# pipenv run python3 1\ -\ flight\ path.py 