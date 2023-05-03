import cv2
import numpy as np


class FeatureExtractor():
    DETECTOR_TYPE: str = "SIFT" # SIFT, ORB
    
    def __init__(self,input_path_1,input_path_2,camera_matrix, save_images: bool = False):

        self.img1 = cv2.imread(input_path_1)
        self.img2 = cv2.imread(input_path_2)

        self.gray1 = cv2.cvtColor(self.img1,cv2.COLOR_BGR2GRAY)
        self.gray2 = cv2.cvtColor(self.img2,cv2.COLOR_BGR2GRAY)

        self.camera_matrix = camera_matrix
        self.save_images:bool = save_images
        
        self.__extract_features_and_estimate_pose()

        self.__calculate_epipolar_line()


    def rmOutliersFundamentalMatrix(self,pts1,pts2,matches,match_indices):
        # create mask from ransac    
        F,mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_RANSAC,1,0.99)

        #extract indices of good matches
        match_indices = np.int32(match_indices)
        match_indices = match_indices[mask.ravel()==1]
        good = []

        # get all good matches
        for i in match_indices:
            good.append(matches[i])

        pts1 = pts1[mask.ravel()==1]
        pts2 = pts2[mask.ravel()==1]

        return [F,good]

    def rmOutliersEssentialMatrix(self,cameraMatrix,pts1,pts2,matches,match_indices):

        # create mask from ransac    
        E,mask = cv2.findEssentialMat(pts1,pts2,cameraMatrix,method=cv2.RANSAC)

        #extract indices of good matches
        match_indices = np.int32(match_indices)
        match_indices = match_indices[mask.ravel()==1]
        good = []

        # get all good matches
        for i in match_indices:
            good.append(matches[i])

        pts1 = pts1[mask.ravel()==1]
        pts2 = pts2[mask.ravel()==1]

        return [pts1,pts2,E,good]


    def getPointsFromMatches(self,matches,kp1,kp2):
        pts1 = []
        pts2 = []
        match_indices = []

        for idx, m in enumerate(matches):
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)
            match_indices.append(idx)
        
        return [np.asarray(pts1).astype(np.float32),np.asarray(pts2).astype(np.float32),match_indices]

    def decompose_essential_matrix(self,E):    
        D = np.array([[0,1,0],[-1,0,0],[0,0,1]])

        U, S, Vt = np.linalg.svd(E, full_matrices=True)

        R1 = U @ D @ Vt
        R2 = U @ np.transpose(D) @ Vt

        t1 = U @ np.array([0,0,1])
        t2 = U @ np.array([0,0,-1])

        return [R1,R2,t1,t2]

    def __extract_features_and_estimate_pose(self): # possibly rename to get3DPoints
        # create sift
        if self.DETECTOR_TYPE == "SIFT":
            detector = cv2.SIFT_create()
        elif self.DETECTOR_TYPE == "ORB":
            detector = cv2.ORB_create()
        else:
            raise Exception("Invalid detector type")

        # detect keypoints and compute descriptors
        kp1,des1 = detector.detectAndCompute(self.gray1,mask=None)
        kp2,des2 = detector.detectAndCompute(self.gray2,mask=None)

        # create BruteForce Matcher
        bf = cv2.BFMatcher_create(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(des1,des2)

        if self.save_images:
            # draw all matches
            matched_image_total = cv2.drawMatches(self.img1,kp1,self.img2,kp2,matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            cv2.imwrite(f"./output/feature/{self.DETECTOR_TYPE}/matched.png", matched_image_total)
            print(f"Number of matches: {len(matches)}")

        # get corresponding points 
        self.pts1,self.pts2,match_indices = self.getPointsFromMatches(matches,kp1,kp2)

        # remove outlier matched with fundamental matrix
        self.F,self.goodF = self.rmOutliersFundamentalMatrix(self.pts1,self.pts2,matches,match_indices)

        if self.save_images:
            # draw good matches F
            matched_image_goodF = cv2.drawMatches(self.img1,kp1,self.img2,kp2,self.goodF ,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            cv2.imwrite(f"./output/feature/{self.DETECTOR_TYPE}/rmOutliersF.png", matched_image_goodF)
            print(f"Number of good matches F: {len(goodF)}")

        ''' NOTE what camera matrix are we supposed to use? '''

        self.pts1E,self.pts2E,E,self.goodE = self.rmOutliersEssentialMatrix(self.camera_matrix,self.pts1,self.pts2,matches,match_indices)

        if self.save_images:
            # draw good matches E
            matched_image_goodE = cv2.drawMatches(self.img1,kp1,self.img2,kp2,self.goodE ,None,flags=2)
            cv2.imwrite(f"./output/feature/{self.DETECTOR_TYPE}/rmOutliersE.png", matched_image_goodE)
            print(f"Number of good matches E: {len(goodE)}")
        
        
        R1,R2,t1,t2 = self.decompose_essential_matrix(E)
        
        _,R,t,mask=cv2.recoverPose(E,self.pts1E,self.pts2E,self.camera_matrix)

        projectionMatrix = self.camera_matrix @ np.hstack((R,t))
        nullProjectionMatrix = self.camera_matrix @ np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])

        self.points3D = cv2.triangulatePoints(projectionMatrix,nullProjectionMatrix,self.pts1.T,self.pts2.T)


        self.relative_pose = np.eye(4)
        self.relative_pose[:3, :3] = R
        self.relative_pose[:3, 3] = t.T[0]

    def get_points3D(self):
        return self.points3D
    
    def get_relative_pose(self):
        return self.relative_pose

    def __calculate_epipolar_line(self, point_type = 'None'):

        # get points depending on point type
        if point_type == 'E':
            self.ptsL = self.pts1E
            self.ptsR = self.pts2E
        else:
            self.ptsL = self.pts1
            self.ptsR = self.pts2

        # find epilines corresponding to points in right image
        self.epilinesR = cv2.computeCorrespondEpilines(self.ptsR.reshape(-1, 1, 2), 2, self.F)
        #epilinesR = epilinesR.reshape(-1, 3)

        # find epilines corresponding to points in left image
        self.epilinesL = cv2.computeCorrespondEpilines(self.ptsL.reshape(-1, 1, 2), 1, self.F)
        #epilinesL = epilinesL.reshape(-1, 3)

    def get_distance_to_epipolars(self):
            # create empty lists
            dL = []
            dR = []
            # calculate distance to epipolar lines for each point left and right
            for line in self.epilinesL:
                a, b, c = line[0]
                for pt in self.ptsR:
                    x, y = pt
                    dL.append(abs(a*x + b*y + c) / np.sqrt(a*a + b*b))

            for line in self.epilinesR:
                a, b, c = line[0]
                for pt in self.ptsL:
                    x, y = pt
                    dR.append(abs(a*x + b*y + c) / np.sqrt(a*a + b*b))

            return [dL,dR]


    def get_matches_E(self):
        return self.goodE

                

        
        

