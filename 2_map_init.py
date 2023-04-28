from FeatureExtractor import *
import matplotlib.pyplot as plt

def main():
    # Define camera matrix
    camera_matrix = np.array([[2676, 0., 3840 / 2 - 35.24], 
            [0.000000000000e+00, 2676., 2160 / 2 - 279],
            [0.000000000000e+00, 0.000000000000e+00, 1.000000000000e+00]])
    
    featureExtractor = FeatureExtractor("./output/frame1.jpg","./output/frame2.jpg",camera_matrix)
    points_3d = featureExtractor.extract_features()

    points_3d /= points_3d[3, :]
    print(points_3d)


    plt.figure()
    plt.scatter(points_3d)
    plt.show()

if __name__ == '__main__':
    main()
