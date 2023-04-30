from FeatureExtractor import *
import matplotlib.pyplot as plt
import numpy as np

def statistics(data):
    # Statistical analysis of the epipolar distances. Mean, std, median, mode, etc.
    print(f"Mean of the epipolar distances for the left image: {np.mean(data)}")
    print(f"Standard deviation of the epipolar distances for the left image: {np.std(data)}")
    print(f"Median of the epipolar distances for the left image: {np.median(data)}")
    print(f"Min of the epipolar distances for the left image: {np.min(data)}")
    print(f"Max of the epipolar distances for the left image: {np.max(data)}")

def main():
    # Define camera matrix
    camera_matrix = np.array([[2676, 0., 3840 / 2 - 35.24], 
            [0.000000000000e+00, 2676., 2160 / 2 - 279],
            [0.000000000000e+00, 0.000000000000e+00, 1.000000000000e+00]])

    # Find the first two frames in the output folder
    import glob 
    files = glob.glob("output/disc/*.jpg")
    # Sort the files by name
    files.sort()

    featureExtractor = FeatureExtractor(files[0], files[1], camera_matrix, save_images=False)
    relative_pose_between_2_images = featureExtractor.get_relative_pose()
    print(f"Relative pose between the first two images: \n{relative_pose_between_2_images}")

    points_3D = featureExtractor.get_points3D()
    print(points_3D.shape)

    # Statistical analysis of the epipolar distances. Mean, std, median, mode, etc.
    dL,dR = featureExtractor.get_distance_to_epipolars()
    statistics(dL)
    statistics(dR)

    plt.figure(figsize=(20,10))
    plt.hist(dL, bins=100, label='Left', color='blue', edgecolor='black')
    plt.title("Epipolar distances for the left image")
    plt.savefig("output/feature/epipolar_distances_left.png")

    '''
    Just a test below. 
    TODO    -   Verify that right points need to be compared with left epipolar lines and vice versa
    '''



if __name__ == '__main__':
    main()

# pipenv run python3 2_map_init.py 