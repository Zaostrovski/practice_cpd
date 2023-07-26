import cv2
import pyautogui
import mediapipe as mp

pyautogui.FAILSAFE = False
width, height = pyautogui.size()

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_tracking_confidence=0.25,
                      min_detection_confidence=0.25)
mpDraw = mp.solutions.drawing_utils

cv2.namedWindow("camera")
last_x = 0
last_y = 0

while True:
    flag, img = cap.read()
    img = cv2.flip(img,1) # отражение кадра вдоль оси Y
    RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB)
    

    if results.multi_hand_landmarks:
        handlms = results.multi_hand_landmarks[0]
        mpDraw.draw_landmarks(img, handlms, mphands.HAND_CONNECTIONS)
        for id, lm in enumerate(handlms.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            if id == 8:
                cv2.circle(img, (cx, cy), 10 ,(255,0,0), cv2.FILLED)
                if abs(last_x - cx) > 2 or abs(last_y - cy) > 2:
                    pyautogui.moveTo(cx * width/w, cy * height/h)
                    last_y = cy
                    last_x = cx

    cv2.imshow('camera', img)
    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()