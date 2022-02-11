import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self, img, draw = True):
        #RGB画像に変換
        imgRGB = cv2.cvtColor( img, cv2.COLOR_BGR2RGB)

        #手の検出
        self.results = self.hands.process(imgRGB)

        #ランドマークが検出された場合
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

               
        return img

    def findPosition(self, img, handNo = 0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                #print(ix, gx, gy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle( img, ( cx, cy ) , 10, ( 0, 0, 255) , cv2.FILLED)
        
        return lmList

