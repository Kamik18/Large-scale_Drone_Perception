from FeatureExtractor import *
import matplotlib.pyplot as plt

def main():
    # Define camera matrix
    camera_matrix = np.array([[2676, 0., 3840 / 2 - 35.24], 
            [0.000000000000e+00, 2676., 2160 / 2 - 279],
            [0.000000000000e+00, 0.000000000000e+00, 1.000000000000e+00]])
    
    featureExtractor = FeatureExtractor("./output/frame1.jpg","./output/frame2.jpg",camera_matrix)

    relative_pose_between_2_images = featureExtractor.get_relative_pose()

    #points_3D = featureExtractor.get_points3D()

    dL,dR = featureExtractor.get_distance_to_epipolars()

    '''
    Just a test below. 
    TODO    -   Statistical analysis of the epipolar distances
            -   Verify that right points need to be compared with left epipolar lines and vice versa
    '''

    plt.figure()
    plt.hist(dL, bins=100)
    plt.show()




if __name__ == '__main__':
    main()
