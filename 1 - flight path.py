# Import the necessary packages
import matplotlib.pyplot as plt

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
    ax.set_xlabel('UTM Eastings')
    ax.set_ylabel('UTM Northings')
    ax.set_zlabel('UTM Altitudes')
    ax.set_title('Flight Path')
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
    # TODO code here 
    utm_eastings:list = []
    utm_northings:list = []
    utm_altitudes:list = []

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
