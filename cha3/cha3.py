#（1）一阶sobel、prewitt（2）log（3）canny算法，single threshold和double threshold
import numpy as np
import sys
ros_cv2_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
if ros_cv2_path in sys.path: sys.path.remove(ros_cv2_path)
import cv2 as cv
import random
from matplotlib import pyplot as plt
from scipy import signal
import math
import argparse

parser = argparse.ArgumentParser(description='IMAGE NOISING AND DENOISING')
parser.add_argument("--CannyS", type=int, default=50)
parser.add_argument("--CannyD", type=int, default=150)
parser.add_argument("--result", default="img")

def pascalSmooth(n):
    pascalSmooth = np.zeros([1, n], np.float32)
    for i in  range(n):
        pascalSmooth[0][i] = math.factorial(n - 1) / (math.factorial(i) * math.factorial(n-1-i))
    return pascalSmooth
 
def pascalDiff(n):      
    pascalDiff = np.zeros([1, n], np.float32)
    pascalSmooth_previous = pascalSmooth(n - 1)
    for i in range(n):
        if i == 0:
            pascalDiff[0][i] = pascalSmooth_previous[0][i]
        elif i == n-1:
            pascalDiff[0][i] = pascalSmooth_previous[0][i-1]
        else:
            pascalDiff[0][i] = pascalSmooth_previous[0][i] - pascalSmooth_previous[0][i-1]
    return pascalDiff
 
def getSmoothKernel(n):
    pascalSmoothKernel = pascalSmooth(n)
    pascalDiffKernel = pascalDiff(n)
    sobelKernel_x = signal.convolve2d(pascalSmoothKernel.transpose(), pascalDiffKernel, mode='full')
    sobelKernel_y = signal.convolve2d(pascalSmoothKernel, pascalDiffKernel.transpose(), mode='full')
    return (sobelKernel_x, sobelKernel_y)
 
def sobel(image, n):
 
    rows, cols = image.shape
    pascalSmoothKernel = pascalSmooth(n)
    pascalDiffKernel = pascalDiff(n)
 
    image_sobel_x = signal.convolve2d(image, pascalSmoothKernel.transpose(), mode='same')
    image_sobel_x = signal.convolve2d(image_sobel_x, pascalDiffKernel, mode='same')
    image_sobel_y = signal.convolve2d(image, pascalSmoothKernel, mode='same')
    image_sobel_y = signal.convolve2d(image_sobel_y, pascalDiffKernel.transpose(), mode='same')
 
    return (image_sobel_x, image_sobel_y)

def prewitt(I, _boundary = 'symm', ):
    ones_y = np.array([[1], [1], [1]], np.float32)
    i_conv_pre_x = signal.convolve2d(I, ones_y, mode='same', boundary=_boundary)
    diff_x = np.array([[1, 0, -1]], np.float32)
    i_conv_pre_x = signal.convolve2d(i_conv_pre_x, diff_x, mode='same', boundary=_boundary)
 
    ones_x = np.array([[1, 1, 1]], np.float32)
    i_conv_pre_y = signal.convolve2d(I, ones_x, mode='same', boundary=_boundary)
    diff_y = np.array([[1], [0], [-1]], np.float32)
    i_conv_pre_y = signal.convolve2d(i_conv_pre_y, diff_y, mode='same', boundary=_boundary)
 
    return (i_conv_pre_x, i_conv_pre_y)


def main() :

    args = parser.parse_args()
    CannyS=args.CannyS
    CannyD=args.CannyD
    result=args.result
    imgpath='/home/zty/myGit/homeworks/cha3/lena.jpg'
    img=cv.imread(imgpath,cv.IMREAD_UNCHANGED)
    rows, cows=img.shape[0:2]
    #cv.imwrite("/home/zty/myGit/homeworks/cha2/results/SP.png", imgSP)
    #Sobel
    image_sobel_x, image_sobel_y = sobel(img, 7)
    edge = np.sqrt(np.power(image_sobel_x, 2.0) + np.power(image_sobel_y, 2.0))
    edge = edge / np.max(edge)
    edge = np.power(edge, 1)
    edge = edge * 255
    edgeSB = edge.astype(np.uint8)
    cv.imwrite("/home/zty/myGit/homeworks/cha3/results/Sobel.png", edgeSB)
    #Prewitt
    i_conv_pre_x, i_conv_pre_y = prewitt(img)
    abs_i_conv_pre_x = np.abs(i_conv_pre_x)
    abs_i_conv_pre_y = np.abs(i_conv_pre_y)
    edge_x = abs_i_conv_pre_x.copy()
    edge_y = abs_i_conv_pre_y.copy()
    edge_x[edge_x > 255] = 255
    edge_y[edge_y > 255] = 255
    edge_x = edge_x.astype(np.uint8)
    edge_y = edge_y.astype(np.uint8)
    edgePR = 0.5 * abs_i_conv_pre_x + 0.5 * abs_i_conv_pre_y
    edgePR[edgePR > 255] = 255
    edgePR = edgePR.astype(np.uint8)
    cv.imwrite("/home/zty/myGit/homeworks/cha3/results/Prewitt.png", edgePR)
    #LoG
    imgGS = cv.GaussianBlur(img, (3,3), 0)
    imgLAP = cv.Laplacian(imgGS, cv.CV_16S, ksize = 3) #再通过拉普拉斯算子做边缘检测
    edgeLOG = cv.convertScaleAbs(imgLAP)
    cv.imwrite("/home/zty/myGit/homeworks/cha3/results/LoG.png", edgeLOG)
    #Canny
    edgeCAS = cv.Canny(imgGS, CannyS, CannyS)
    edgeCAD = cv.Canny(imgGS, CannyS, CannyD)
    cv.imwrite("/home/zty/myGit/homeworks/cha3/results/CAS.png", edgeCAS)
    cv.imwrite("/home/zty/myGit/homeworks/cha3/results/CAD.png", edgeCAD)

    cv.namedWindow("Result", cv.WINDOW_NORMAL)
    cv.resizeWindow("Result", int(cows*2), int(rows*2))
    cv.imshow("Result", eval(result))
    cv.waitKey(0)
    cv.destroyAllWindows()

    

if __name__ == '__main__':
    main()