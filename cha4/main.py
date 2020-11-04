
import sys
ros_cv2_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
if ros_cv2_path in sys.path:
    sys.path.remove(ros_cv2_path)
import numpy as np
from matplotlib import pyplot as plt
import argparse
import cv2



parser = argparse.ArgumentParser(description='CAMERA IMAGE PROCESSING')
parser.add_argument("--solution", type=int, default=1)
parser.add_argument("--result", default="result")

'''
Step1 Generate Laplacian pyramid Lo of orange image. Generate the Laplacian pyramid La of apple image. 
Step 2&3 Generate Laplacian pyramid Lc by 
– copying left half of the nodes at each level from apple and 
– right half of nodes from orange pyramids. 
Step 4 Reconstruct a combined image from Lc.
'''


def main():

    A = cv2.imread('cha4/orange.jpg')
    B = cv2.imread('cha4/apple.jpg')
    #print(B.shape[1])
    B = cv2.resize(B, (A.shape[1], int(A.shape[1]/B.shape[1]*B.shape[0])))

    #print(A.shape)
    #print(B.shape)
    # generate Gaussian pyramid for A
    G = A.copy()
    gpA = [G]
    for i in range(6):
        G = cv2.pyrDown(G)
        gpA.append(G)

    # generate Gaussian pyramid for B
    G = B.copy()
    gpB = [G]
    for i in range(6):
        G = cv2.pyrDown(G)
        gpB.append(G)

    # generate Laplacian Pyramid for A
    lpA = [gpA[5]]
    for i in range(5, 0, -1):
        GE = cv2.pyrUp(gpA[i])
        GE = cv2.resize(GE, (int(gpA[i-1].shape[1]), int(gpA[i-1].shape[0])))
        L = cv2.subtract(gpA[i-1], GE)
        lpA.append(L)

    # generate Laplacian Pyramid for B
    lpB = [gpB[5]]
    for i in range(5, 0, -1):
        GE = cv2.pyrUp(gpB[i])
        GE = cv2.resize(GE, (int(gpB[i-1].shape[1]), int(gpB[i-1].shape[0])))
        L = cv2.subtract(GE, gpB[i-1])
        lpB.append(L)

    # 把金字塔的每一层图像都上下拼接
    # Take a sequence of arrays and stack them horizontally
    # to make a single array.
    LS = []
    for la, lb in zip(lpA, lpB):
        rows= la.shape[0]
        #print(la.shape)
        #print(lb.shape)
        ls = np.vstack((la[0:round(rows/2)], lb[round(rows/2):]))
        LS.append(ls)

    # now reconstruct
    ls_ = LS[0]
    for i in range(1, 6):
        ls_ = cv2.pyrUp(ls_)
        ls_ = cv2.resize(ls_, (int(LS[i].shape[1]), int(LS[i].shape[0])))
        #print(ls_.shape)
        #print(LS[i].shape)
        ls_ = cv2.add(ls_, LS[i])

    # image with direct connecting each half
    real = np.vstack((A[:round(rows/2), :], B[round(rows/2):, :]))

    cv2.imwrite('Pyramid_blending2.jpg', ls_)
    cv2.imwrite('Direct_blending.jpg', real)


if __name__ == '__main__':
    main()
