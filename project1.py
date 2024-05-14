import cv2
import numpy as np
import time
import os
import mediapipe as mp

class handi():
    def __init__(self, mode=False, maxhq=2,compl=1, deCon=0.5, tCon = 0.5):
        self.mode = mode
        self.maxhq = maxhq
        self.compl = compl
        self.deCon = deCon
        self.tCon = tCon

        self.mph1 = mp.solutions.hands
        self.hands = self.mph1.Hands(self.mode, self.maxhq,self.compl, self.deCon, self.tCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]

    def findh(self, img, draw=True):
        img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(img1)
        # print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for i in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,i, self.mph1.HAND_CONNECTIONS)

        return img

    def findpos1(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, f in enumerate(myHand.landmark):
                h, w, c = img.shape
                c1, c2 = int(f.x * w), int(f.y * h)
                self.lmList.append([id, c1, c2])

                if draw:
                    cv2.circle(img, (c1, c2), 10, (255, 255, 255), cv2.FILLED)

        return self.lmList
    def finup(self):
        fin = []
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fin.append(1)
        else:
            fin.append(0)
        
        for i in range(1, 5):
            if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2]:
                fin.append(1)
            else:
                fin.append(0)
                
        return fin
def main():


    ###########################

    brusht=25
    erasert=80
    ###########################
    f1="C:/Users/DELL/OneDrive/Desktop/project_folde"
    l1=os.listdir(f1)
    print(l1)
    l2=[]
    for imPath in l1:
        image=cv2.imread(f'{f1}/{imPath}')
        l2.append(image)
    print(len(l2))
    header=l2[0]
    drawing=(0,0,255)
    
    cap=cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    detector=handi(deCon=0.85)
    xm,ym=0,0
    dupimg=np.zeros((720,1280,3),np.uint8)
    while True:
        success,img=cap.read()
        img=cv2.flip(img,1)

        
        img=detector.findh(img)
        lmList=detector.findpos1(img,draw=False)

        if len(lmList)!=0:
            #print(lmList)
            

   
            x1,y1=lmList[8][1:]
            x2,y2=lmList[12][1:]


            fingers=detector.finup()
            #print(fingers)

            #4
            if fingers[1] and fingers[2]:
                xm,ym=0,0
                print("selection mode")
                if y1<125:
                    if 250 < x1 < 450:
                        header=l2[0]
                        drawing=(0,0,255)
                    if 550 < x1 < 750:
                        header=l2[1]
                        drawing=(255,0,0)
                    if 800 < x1 < 950:
                        header=l2[2]
                        drawing=(0,255,0)
                    if 1050 < x1 < 1200:
                        header=l2[3]
                        drawing=(0,0,0)
                cv2.rectangle(img,(x1,y1-15),(x2,y2+15),drawing,cv2.FILLED)
                    
            #5
            if fingers[1] and fingers[2]==False:
                cv2.circle(img,(x1,y1),15,drawing,cv2.FILLED)
                print("Drawing mode")
                if xm==0 and ym==0:
                    xm,ym=x1,y1
                    
                if drawing==(0,0,0):
                    cv2.line(img,(xm,ym),(x1,y1),drawing,erasert)
                    cv2.line(dupimg,(xm,ym),(x1,y1),drawing,erasert)
                else:  
                    cv2.line(img,(xm,ym),(x1,y1),drawing,brusht)
                    cv2.line(dupimg,(xm,ym),(x1,y1),drawing,brusht)
                xm,ym=x1,y1


                
        imgg=cv2.cvtColor(dupimg,cv2.COLOR_BGR2GRAY)
        _, imgi= cv2.threshold(imgg,50,255,cv2.THRESH_BINARY_INV)
        imgi=cv2.cvtColor(imgi,cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img,imgi)
        img = cv2.bitwise_or(img,dupimg)
            
        img[0:125,0:1280]=header
        #img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
        cv2.imshow("image",img)
        cv2.imshow("canvas",dupimg)
        cv2.imshow("Inv",imgi)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            cap.release()

if __name__ == "__main__":
    main()

