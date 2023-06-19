import cv2 
import cvzone  
import time
from cvzone.HandTrackingModule import HandDetector
import random
def resize_image(img : cv2.imread,width_portion,height_portion) : 
    width,height,channel = img.shape 
    width *= width_portion 
    height *= height_portion 
    return cv2.resize(img,(int(width),int(height)))


cap = cv2.VideoCapture(0) 
# cap.set(4,855)
detector = HandDetector(maxHands=2) 
timer = 0 
stateResult = False
startGame = False 
score = [0,0] # 0 for bot 1 for player
while True :  
    imgBG = cv2.imread("Resource/BG.png")  
    imgBG = resize_image(imgBG,0.8,0.2)
    width,height,channel = imgBG.shape 
    # print(width,height,channel) 

    success, img = cap.read() 
    img = resize_image(img,0.55,0.4)
    hands ,img = detector.findHands(img) 
    imgBG[110:366,510:774] = img
    if startGame : 

        if stateResult is False :  
            timer = time.time() - initialTime
            cv2.putText(imgBG,str(int(timer)),(405,230),cv2.FONT_HERSHEY_PLAIN,4,(0,0,255),4)
            if timer > 3 :
                stateResult = True 
                timer = 0

                if hands:   
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand) 
                    print(fingers) 
                    if fingers == [0,0,0,0,0]: 
                        playerMove = 1 
                    if fingers == [1,1,1,1,1]:  
                        playerMove = 2 
                    if fingers == [0,1,1,0,0]: 
                        playerMove = 3 
                    # print(playerMove) 

                    randomNumber = random.randint(1,3)
                    imgBot = cv2.imread(f'Resource/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                    imgBot = cv2.resize(imgBot,(154,154))
                    imgBG = cvzone.overlayPNG(imgBG,imgBot,(150,160))

                    # player wins 
                    if (playerMove == 1 and randomNumber == 3) or (playerMove == 2 and randomNumber == 1) or (playerMove == 3 and randomNumber ==2): 
                        score[1]+=1

                    # Bot win
                    if (playerMove == 3 and randomNumber == 1) or (playerMove == 1 and randomNumber == 2) or (playerMove == 2 and randomNumber ==3): 
                        score[0]+=1
    # cv2.imshow("Image",img)
    if stateResult : 
        imgBG = cvzone.overlayPNG(imgBG,imgBot,(150,160))

    cv2.putText(imgBG,str(score[1]),(714,110),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),4)
    cv2.putText(imgBG,str(score[0]),(280,110),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),4)
    cv2.imshow("BG",imgBG)
    key = cv2.waitKey(1) 
    if key == ord('q'):
        break   
    elif key == ord('s'): 
        startGame = True 
        initialTime = time.time()
        stateResult = False

