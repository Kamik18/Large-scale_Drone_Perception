from FeatureExtractor import *
import matplotlib.pyplot as plt

def main():
    # Define camera matrix
    camera_matrix = np.array([[2676, 0., 3840 / 2 - 35.24], 
            [0.000000000000e+00, 2676., 2160 / 2 - 279],
            [0.000000000000e+00, 0.000000000000e+00, 1.000000000000e+00]])
    
    featureExtractor = FeatureExtractor("./output/frame1.jpg","./output/frame2.jpg",camera_matrix)

    points_3D = featureExtractor.get_points3D()

    '''
    NOTE: This is how Hendrik processes the 3D points - Possibly attend to class function

        import collections

        Match3D = collections.namedtuple('Match3D', 
        ['featureid1', 'featureid2', 
            'keypoint1', 'keypoint2', 
            'descriptor1', 'descriptor2', 
            'distance', 'color', 
            'point'])  

        # in the function itself:
            self.matches_with_3d_information = [
                Match3D(match.featureid1, match.featureid2, 
                    match.keypoint1, match.keypoint2, 
                    match.descriptor1, match.descriptor2, 
                    match.distance, match.color,
                    (self.points3d_reconstr[0, idx],
                        self.points3d_reconstr[1, idx],
                        self.points3d_reconstr[2, idx]))
                for idx, match 
                in enumerate(matches)]
    
    
    '''






if __name__ == '__main__':
    main()