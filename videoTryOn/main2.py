import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

import os

# video and pose detector start
cap = cv2.VideoCapture("C:\\Users\\viv91\\Desktop\\virtualTryOn\\videoTryOn\\Resources\\Videos\\1.mp4")
# cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirtFolderPath = "C:\\Users\\viv91\\Desktop\\virtualTryOn\\videoTryOn\\Resources\\Shirts"
shirtsList = os.listdir("C:\\Users\\viv91\\Desktop\\virtualTryOn\\videoTryOn\\Resources\\Shirts")

fixedRatio = 262/190

# buttons data
imageNumber = 0
counterLeft = 0
counterRight = 0 
selectionSpeed =10
rightButton = cv2.imread("C:\\Users\\viv91\\Desktop\\virtualTryOn\\videoTryOn\\Resources\\button.png", cv2.IMREAD_UNCHANGED)
leftButton = cv2.flip(rightButton, 1)


while True:
    success, img = cap.read()
    img = detector.findPose(img,draw=True)
    landmarksList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=True)

    # if landmarks recognized then overlay image 
    if landmarksList:
        center = bboxInfo["center"]
        clothImage = cv2.imread(os.path.join(shirtFolderPath, shirtsList[imageNumber]),cv2.IMREAD_UNCHANGED)
        
        # get width of shirt
        rightupperArm = landmarksList[11][0:2]
        leftupperArm = landmarksList[12][0:2]
        landmarksWidth = rightupperArm[0] - leftupperArm[0]
        print("landmarksWidth",landmarksWidth)
        clothHeight,clothWidth = clothImage.shape[:2]
        clothHeightWidthRatio = clothHeight/clothWidth

        shirtWidth = int(landmarksWidth * fixedRatio)
        
        clothImage = cv2.resize(clothImage, (shirtWidth, int(shirtWidth*clothHeightWidthRatio)))
        currentScale = landmarksWidth / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        # overlaying cloth and video frame
        print(shirtWidth)
        try:
            img = cvzone.overlayPNG(img, clothImage, (leftupperArm[0] - offset[0], leftupperArm[1] - offset[1]))
        except:
            pass


        #Button pressing logic
        img = cvzone.overlayPNG(img, rightButton, (1074, 293))
        img = cvzone.overlayPNG(img, leftButton, (72, 293))

        if landmarksList[16][1] < 500:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)
            
            if counterRight * selectionSpeed >= 360:
                counterRight = 0
                if imageNumber < len(shirtsList) - 1:
                    imageNumber += 1

        elif landmarksList[15][1] > 770:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 10)
            if counterLeft * selectionSpeed >= 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    
    if key == 13:
        break

cap.release()
cv2.destroyAllWindows()




