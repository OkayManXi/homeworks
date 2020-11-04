import numpy as np
import sys
ros_cv2_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
if ros_cv2_path in sys.path: sys.path.remove(ros_cv2_path)
import cv2 as cv
from matplotlib import pyplot as plt
import argparse


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

#demosaic
def Demosaic(img):
    imgRGB=cv.cvtColor(img,cv.COLOR_BayerRG2BGR)
    return imgRGB

def main():

    args = parser.parse_args()
    solution=args.solution
    showpic=args.result
    imgpath='data/raw-data-BayerpatternEncodedImage.tif'
    img=cv.imread(imgpath,cv.IMREAD_UNCHANGED)
    rows, cows=img.shape

      
if __name__ == '__main__':
    main()