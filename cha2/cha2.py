#在lena图片上进行（1）、添加高斯噪声、椒盐噪声、脉冲噪声得到噪声图（2）、用不同尺寸的box filter对三张噪声去噪
#（3）用不同sigma的高斯噪声对三张噪声图进行去噪

import numpy as np
import sys
ros_cv2_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
if ros_cv2_path in sys.path: sys.path.remove(ros_cv2_path)
import cv2 as cv
import random
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='IMAGE NOISING AND DENOISING')
parser.add_argument("--prob", type=float, default=0.01)
parser.add_argument("--sigma", type=float, default=0.0)
parser.add_argument("--result", default="img")

#椒盐噪声
def sp_noise(image,prob):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output
#高斯噪声
def gasuss_noise(image, mean=0, var=0.001):
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    return out
#脉冲噪声
def pl_noise(image,prob):
    output = np.zeros(image.shape,np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def main() :

    args = parser.parse_args()
    prob = args.prob
    sigma=args.sigma
    result=args.result
    imgpath='/home/zty/myGit/homeworks/cha2/lena.jpg'
    img=cv.imread(imgpath,cv.IMREAD_UNCHANGED)
    #print(img.shape)
    rows, cows=img.shape[0:2]

    #添加噪声
    imgSP = sp_noise(img, prob)
    imgGN = gasuss_noise(img, 0, 0.001)
    imgPL = pl_noise(img, prob)
    #box滤波
    imgSPDN = cv.boxFilter(imgSP,-1, (3, 3), normalize=True)
    imgGNDN = cv.boxFilter(imgGN,-1, (5, 5), normalize=True)
    imgPLDN = cv.boxFilter(imgPL,-1, (7, 7), normalize=True)
    #高斯滤波
    blurSP=cv.GaussianBlur(imgSP,(3,3),sigma)
    blurGN=cv.GaussianBlur(imgGN,(3,3),sigma)
    blurPL=cv.GaussianBlur(imgPL,(3,3),sigma)

    cv.imwrite("/home/zty/myGit/homeworks/cha2/results/SP.png", imgSP)
    cv.imwrite("/home/zty/myGit/homeworks/cha2/results/GN.png", imgGN)
    cv.imwrite("/home/zty/myGit/homeworks/cha2/results/PL.png", imgPL)
    cv.imwrite("/home/zty/myGit/homeworks/cha2/results/SPDN.png", imgSPDN)
    cv.imwrite("/home/zty/myGit/homeworks/cha2/results/GNDN.png", imgGNDN)
    cv.imwrite("/home/zty/myGit/homeworks/cha2/results/PLDN.png", imgPLDN)
    cv.imwrite("/home/zty/myGit/homeworks/cha2/results/PLGS.png", blurSP)
    cv.imwrite("/home/zty/myGit/homeworks/cha2/results/SPGS.png", blurPL)
    cv.imwrite("/home/zty/myGit/homeworks/cha2/results/GNDS.png", blurGN)

    cv.namedWindow("Result", cv.WINDOW_NORMAL)
    cv.resizeWindow("Result", int(cows*2), int(rows*2))
    cv.imshow("Result", eval(result))
    cv.waitKey(0)
    cv.destroyAllWindows()

    

if __name__ == '__main__':
    main()