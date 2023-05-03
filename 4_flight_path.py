# Import the necessary packages
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from VizualiseFlight.utm import utmconv
from VizualiseFlight.exportkml import kmlclass
from FrameIterator import *


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

    TOTAL_FRAMES:int = 3294
    DISCARD_FRAMES:int = 1200
    INTERSECTION:int = int(len(utm_northings) * (DISCARD_FRAMES / TOTAL_FRAMES))
    
    SIFT: np.ndarray = np.array([
    ( 0.000000,  0.000000,  0.000000),
    ( 0.020794,  0.440986, -0.897273),
    ( 0.036656,  0.834608, -1.853767),
    ( 0.027050,  1.268064, -2.788852),
    (-0.048445,  1.623116, -3.505401),
    (-0.119248,  1.676257, -3.573501),
    ( 1.712244,  1.650907, -3.643679),
    ( 2.937114,  1.736012, -3.588372),
    ( 4.018324,  1.696690, -3.493547),
    ( 5.088890,  1.582627, -3.239544),
    ( 6.196512,  1.186280, -2.409438),
    ( 6.803724,  0.912705, -1.811008),
    ( 6.994039,  0.870298, -1.851752),
    ( 7.551854, -0.195366,  0.589806),
    ( 7.168783, -0.871949,  1.958246),
    ( 5.776419, -1.859514,  4.109528),
    ( 2.927802, -2.573225,  5.784584)])

    ORB : np.ndarray = np.array([
    (  0.000000,  0.000000,  0.000000),
    (  0.020452,  0.355433,  -0.934478),
    (  0.061836,  0.743202,  -1.832796),
    (  0.109962,  1.127996,  -2.763329),
    (  0.282499,  1.348961,  -3.597656),
    (  0.486762,  1.267279,  -3.781944),
    (  2.023431,  1.248570,  -3.948995),
    (  3.021007,  0.964526,  -3.734636),
    (-17.376541, -0.485440,  17.084622),
    (-20.337491,  1.562764,  11.778244),
    (-21.983947,  4.732205,   5.193696),
    (-21.566606,  7.022344,  -0.260270),
    (-20.645872,  8.299657,  -4.138168),
    (-13.694112, 12.566813, -12.719841),
    ( -9.205659, 12.146941, -17.820362),
    (  2.703067, 13.623171, -19.611317),
    ( 15.836941, 11.535945, -15.032499)
    ])

    # Swap the y and z axis
    temp = SIFT[:, 1].copy()
    SIFT[:, 1] = SIFT[:, 2]
    SIFT[:, 2] = temp
    SIFT[:, 0] = -SIFT[:, 0]

    temp = ORB[:, 1].copy()
    ORB[:, 1] = ORB[:, 2]
    ORB[:, 2] = temp
    ORB[:, 0] = -ORB[:, 0]

    SIFT[:, 0] = SIFT[:, 0]
    SIFT[:, 1] = SIFT[:, 1]
    SIFT[:, 2] = SIFT[:, 2]

    ORB[:, 0] = ORB[:, 0]
    ORB[:, 1] = ORB[:, 1]
    ORB[:, 2] = ORB[:, 2]

    # Create a 3d plot
    fig = plt.figure()    
    ax = fig.add_subplot(111, projection='3d')
    # Plot the SIFT features
    ax.plot(SIFT[:, 0], SIFT[:, 1], SIFT[:, 2], color='green', label='SIFT')
    # Plot the ORB features
    ax.plot(ORB[:, 0], ORB[:, 1], ORB[:, 2], color='blue', label='ORB')
    ax.axis('equal')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')
    ax.set_title('Flight Path')
    ax.legend()
    #plt.savefig('output/flight_path_features/3d.png', format='png', bbox_inches='tight')
    plt.show()
  
    print(SIFT.shape)
    print(ORB.shape)

    # Create a 2d plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1 ,1)
    # Plot the SIFT features
    ax.plot(SIFT[:, 0], SIFT[:, 1], color='green', label='SIFT')
    # Plot the ORB features
    ax.plot(ORB[:, 0], ORB[:, 1], color='blue', label='ORB')
    ax.axis('equal')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_title('Flight Path')
    ax.legend()
    #plt.savefig('output/flight_path_features/2d.png', format='png', bbox_inches='tight')
    plt.show()


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

# pipenv run python3 1_flight_path.py 






