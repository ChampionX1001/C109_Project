import cv2
from pynput.keyboard import Key, Controller
import mediapipe as mp 
import pyautogui
imgNum = 0

keyboard = Controller()

cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
mpdrawing = mp.solutions.drawing_utils

hands = mphands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIDs = [4,8,12,16,20]
state = None
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

def drawhandlandmarks(image, hand_landmarks):
    if hand_landmarks:
        for landmarks in hand_landmarks:
            mpdrawing.draw_landmarks(image, landmarks, mphands.HAND_CONNECTIONS)

def countfingers(image, hand_landmarks, handNO=0):
    global state
    global imgNum
    if hand_landmarks:
        landmarks = hand_landmarks[handNO].landmark
        print(landmarks)
        fingers = []

        for lmindex in tipIDs:
            fingertipY = landmarks[lmindex].y
            fingerbottomY = landmarks[lmindex-2].y

            if lmindex != 4:
                if fingertipY < fingerbottomY:
                    fingers.append(1)
                    print("finger with ID ", lmindex, " is open")
                
                if fingertipY > fingerbottomY:
                    fingers.append(0)
                    print("finger with ID ", lmindex, " is closed")
        
        totalfingers = fingers.count(1)
        if totalfingers == 4:
            state = "Play"
        if totalfingers == 0 and state == "Play":
            state = "Pause"
            keyboard.press(Key.space)
        fingertipX = (landmarks[8].x) * width
        if totalfingers == 1:
            if fingertipX < width-400:
                print("Play Backward")
                keyboard.press(Key.left)
            if fingertipX > width-50:
                print("Play Forward")
                keyboard.press(Key.right)
        if totalfingers == 0:
            pyautogui.screenshot("straight_to_disk_"+str(imgNum)+".png")
            imgNum += 1
        text = f"fingers:{totalfingers}"
        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    result = hands.process(image)
    
    hand_landmarks = result.multi_hand_landmarks

    drawhandlandmarks(image, hand_landmarks)
    countfingers(image, hand_landmarks)
    
    cv2.imshow("image", image)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()