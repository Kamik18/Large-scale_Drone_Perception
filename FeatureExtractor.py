import cv2
import numpy as np

class FeatureExtractor():
    def __init__(self,input_path_1,input_path_2,camera_matrix):

        self.img1 = cv2.imread(input_path_1)
        self.img2 = cv2.imread(input_path_2)

        self.gray1 = cv2.cvtColor(self.img1,cv2.COLOR_BGR2GRAY)
        self.gray2 = cv2.cvtColor(self.img2,cv2.COLOR_BGR2GRAY)

        self.camera_matrix = camera_matrix
        
        print(self.camera_matrix)


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

    def extract_features(self): # possibly rename to get3DPoints

        # create sift
        sift = cv2.SIFT_create()

        # detect keypoints and compute descriptors
        kp1,des1 = sift.detectAndCompute(self.gray1,mask=None)
        kp2,des2 = sift.detectAndCompute(self.gray2,mask=None)

        # create BruteForce Matcher
        bf = cv2.BFMatcher_create(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(des1,des2)

        # draw all matches
        matched_image_total = cv2.drawMatches(self.img1,kp1,self.img2,kp2,matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        # get corresponding points 
        pts1,pts2,match_indices = self.getPointsFromMatches(matches,kp1,kp2)

        # remove outlier matched with fundamental matrix
        F,goodF = self.rmOutliersFundamentalMatrix(pts1,pts2,matches,match_indices)

        # draw good matches F
        matched_image_goodF = cv2.drawMatches(self.img1,kp1,self.img2,kp2,goodF ,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        ''' NOTE what camera matrix are we supposed to use? '''

        pts1E,pts2E,E,goodE = self.rmOutliersEssentialMatrix(self.camera_matrix,pts1,pts2,matches,match_indices)

        # draw good matches E
        matched_image_goodE = cv2.drawMatches(self.img1,kp1,self.img2,kp2,goodE ,None,flags=2)

        # save images
        cv2.imwrite("./output/rmOutliersE.png", matched_image_goodE)
        cv2.imwrite("./output/rmOutliersF.png", matched_image_goodF)
        cv2.imwrite("./output/matched.png", matched_image_total)
        
        R1,R2,t1,t2 = self.decompose_essential_matrix(E)
        
        _,R,t,mask=cv2.recoverPose(E,pts1,pts2,self.camera_matrix)

        projectionMatrix = self.camera_matrix @ np.hstack((R,t))
        nullProjectionMatrix = self.camera_matrix @ np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])

        points3D = cv2.triangulatePoints(projectionMatrix,nullProjectionMatrix,pts1.T,pts2.T)

        print(points3D)

        return points3D
        #plt.figure()
        #plt.scatter(points3D)
        #plt.show()

