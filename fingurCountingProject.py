import cv2
import time
import os
import HandTrackingModel as htm
from natsort import natsorted


wCam = 640
hCam = 480
folderPath = "img"

cap = cv2.VideoCapture(0)

myList = os.listdir(folderPath)
myList = sorted(myList)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    print(f'{folderPath}/{imPath}')
    overlayList.append(image)

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
while True: 

    success, img = cap.read()
    img = detector.findHand(img)
    lmList = detector.findPosition(img, draw = False)
    #print(lmList)
    if len(lmList) != 0:
        fingers = []
        #指が開いているか閉じているかの判断

        #Thmb
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #4 Fingurs
        for id in range(1 , 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]

        #img[0 : 120, 0 : 120] = overlayList[0]

    cv2.imshow("image", img)
    cv2.waitKey(1) 