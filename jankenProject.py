import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps  # 画像データ用
import cv2
import time
import os
import numpy as np
import HandTrackingModel as htm
import random
from natsort import natsorted

folderPath = "img"
jankenfolderPath = "janken"

myjankenList = os.listdir(jankenfolderPath)
myjankenList = sorted(myjankenList)

overlayList = []
for imPath in myjankenList:
    jankenimg = cv2.imread(f'{jankenfolderPath}/{imPath}')
    print(f'{folderPath}/{imPath}')
    overlayList.append(jankenimg)

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
PCHands = ["グー","チョキ","パー"]

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()

        self.master.title("OpenCVの動画表示")       # ウィンドウタイトル
        self.master.geometry("400x300")     # ウィンドウサイズ(幅x高さ)
        
        # Canvasの作成
        self.canvas = tk.Canvas(self.master)
        # Canvasを配置
        self.canvas.pack(expand = True, fill = tk.BOTH)

        self.start_button = tk.Button(self.master, text = "START", command = self.start)
        self.start_button.pack(side = "bottom")

        self.label = tk.Label(self.master,text="",font=("", 30, "bold"),)
        self.label.pack(side = "bottom")

        self.label1 = tk.Label(self.master,text="",font=("", 20, "bold"),)
        self.label1.pack(side = "bottom")

        # カメラをオープンする
        self.capture = cv2.VideoCapture(0)

        self.disp_id = None

    def start(self):
        # 動画を表示
        if self.disp_id == None:
            self.disp_image()

        self.totalFingers = 10
        self.PCHand = random.randint(0, 2)
        self.saisyoha()


    def saisyoha(self):
        self.label.configure(text = "最初は")
        
        self.after_id = self.master.after(1000,self.gu)

    def gu(self):
        self.label.configure(text = "グー")
        self.after_id = self.master.after(1000,self.janken)

    def janken(self):
        self.label.configure(text = "じゃんけん")
        self.after_id = self.master.after(700,self.pon)
    
    def pon(self):
        self.label.configure(text = "ぽん")

        self.myHand = self.totalFingers
        self.after_id = self.master.after(1000,self.judge)
        print(self.totalFingers)

    def disp_image(self):
        # フレーム画像の取得
        success, img = self.capture.read()
        img = detector.findHand(img)
        lmList = detector.findPosition(img, draw = False)
        if len(lmList) != 0:
            fingers = []
            #指が開いているか閉じているかの判断
            #親指
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            #それ以外
            for id in range(1 , 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            self.totalFingers = fingers.count(1)
        
            h, w, c = overlayList[0].shape
            if self.totalFingers == 0:
                img[0:h, 0:w] = overlayList[0]
            elif self.totalFingers == 2:
                img[0:h, 0:w] = overlayList[1]
            elif self.totalFingers == 5:
                img[0:h, 0:w] = overlayList[2]

        cv_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(cv_image)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height))

        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        self.canvas.create_image(canvas_width / 2, canvas_height / 2,image=self.photo_image)

        self.disp_id = self.after(2, self.disp_image)
    
    def judge(self):
        print(self.PCHand)
        PCHandText = PCHands[self.PCHand]

        
        if (self.PCHand == 0 and self.totalFingers == 2) or (self.PCHand == 1 and self.totalFingers == 5) or (self.PCHand == 2 and self.totalFingers == 0):
            print(PCHandText)
            
            self.label.configure(text = "あなたの負けです")
            self.label1.configure(text = f'PC:{PCHandText}')

        elif (self.PCHand == 0 and self.totalFingers == 5) or (self.PCHand == 1 and self.totalFingers == 0) or (self.PCHand == 3 and self.totalFingers == 2):
            print(PCHandText)
            print(self.totalFingers)
            self.label.configure(text = "あなたの勝ちです")
            self.label1.configure(text = f'PC:{PCHandText}')

        elif (self.PCHand == 0 and self.totalFingers == 0) or (self.PCHand == 1 and self.totalFingers == 2) or (self.PCHand == 3 and self.totalFingers == 5):
            print(PCHandText)
            print(self.totalFingers)
            self.label.configure(text = "あいこです")
            self.label1.configure(text = f'PC:{PCHandText}')

        else:
            print(PCHandText)
            print(self.totalFingers)
            self.label.configure(text = "手を認識できませんでした")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()