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

#demosaic
def Demosaic(img):
    imgRGB=cv.cvtColor(img,cv.COLOR_BayerRG2BGR)
    return imgRGB

#白平衡
def Whitebalance(img,row,cow):
    imgtemp=img.copy()
    b, g, r = cv.split(imgtemp)
    sum_b =np.sum(b)
    sum_g =np.sum(g)
    sum_r =np.sum(r)
    time = row*cow
    avg_b = sum_b / time
    avg_g = sum_g / time
    avg_r = sum_r / time
    K=(avg_b + avg_g + avg_r)*(1/3.2)
    Kr=K/avg_r
    Kg=K/avg_g
    Kb=K/avg_b
    b=b*Kb
    g=g*Kg
    r=r*Kr
    imgWB = cv.merge([b, g, r])
    imgWB = imgWB.astype(np.uint8)
    return imgWB
    #cv.imwrite("/home/zty/myGit/homeworks/result/wb.png", imgWB)

#色彩矫正
def ColorCorrect(img):
    imgtemp=img.copy()
    b, g, r = cv.split(imgtemp)
    CCM=np.array([[1, 0.1, 0.1], [0.1, 1, 0.1], [0.1, 0.1, 1]])
    imgtemp[:,:,0:3]=np.matmul(imgtemp[:,:,0:3], CCM)
    imgtemp = imgtemp.astype(np.uint8)
    imgCC=imgtemp.copy()
    return imgCC
    #cv.imwrite("/home/zty/myGit/homeworks/result/cc.png", imgCC)



#gamma矫正
def gammaCorrect(img):
    gamma=1
    imgtemp=img.copy()
    b, g, r = cv.split(imgtemp)
    b=np.power(b/255, gamma)*255
    g=np.power(g/255, gamma)*255
    r=np.power(r/255, gamma)*255
    imgGC = cv.merge([b, g, r])
    imgGC = imgGC.astype(np.uint8)
    return imgGC
    #cv.imwrite("/home/zty/myGit/homeworks/result/gc.png", imgGC)

def denoising(img):
    imgtemp=img
    imgtemp = imgtemp.astype(np.uint8)
    imgDN = cv.fastNlMeansDenoisingColored(imgtemp,None,10,10,7,21)
    #cv.imwrite("/home/zty/myGit/homeworks/result/dn.png", imgDN)
    return imgDN

def main():

    args = parser.parse_args()
    solution=args.solution
    showpic=args.result
    imgpath='data/raw-data-BayerpatternEncodedImage.tif'
    img=cv.imread(imgpath,cv.IMREAD_UNCHANGED)
    rows, cows=img.shape

    if solution==1:
        imgRGB=Demosaic(img)
        imgWB=Whitebalance(imgRGB,rows,cows)
        imgCC=ColorCorrect(imgWB)
        imgGC=gammaCorrect(imgCC)
        imgDN=denoising(imgGC)
        result=imgDN.copy()
    else:
        imgRGB=Demosaic(img)
        imgDN=denoising(imgRGB)
        imgWB=Whitebalance(imgDN,rows,cows)
        imgCC=ColorCorrect(imgWB)
        imgGC=gammaCorrect(imgCC)
        result=imgGC.copy()

    cv.namedWindow("Result", cv.WINDOW_NORMAL)
    cv.resizeWindow("Result", int(cows/2), int(rows/2));
    cv.imshow("Result",eval(showpic))
    cv.waitKey(0)
    cv.destroyAllWindows()

        
if __name__ == '__main__':
    main()


'''
plt.subplot(231)
plt.imshow(img)
plt.subplot(232)
plt.imshow(imgRGB)
plt.subplot(233)
plt.imshow(imgWB/255)
plt.subplot(234)
plt.imshow(imgCC/255)
plt.subplot(235)
plt.imshow(imgGC/255)
#plt.subplot(236),plt.imshow(imgDN)
plt.show()

plt.savefig("/home/zty/myGit/homeworks/result/cha1.png")
'''






