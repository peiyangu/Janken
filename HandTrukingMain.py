import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands()

img_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
img_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


while True:
    res, img = cap.read()

    imgRGB = cv2.cvtColor( img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for ix, lm in enumerate(handLms.landmark):
                gx = int(lm.x * img_w)
                gy = int(lm.y * img_h)
                print(ix, gx, gy)
                cv2.circle( img, ( gx, gy ) , 10, ( 0, 0, 255) , cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow('hand', img)
    if cv2.waitKey( 1 ) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()