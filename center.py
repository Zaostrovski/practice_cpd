import cv2
import numpy as np 

if __name__ == '__main__':
    def callback(*arg):
        pass

green = np.array(((30, 90, 130),(110, 255, 255)))

cv2.namedWindow("result")
cv2.namedWindow("camera")
cv2.namedWindow( "settings" )

cap = cv2.VideoCapture(0)

lastx = 0
lasty = 0
path_color = (0,0,255)

cv2.createTrackbar('h1', 'settings', 0,   255, callback)
cv2.createTrackbar('s1', 'settings', 0,   255, callback)
cv2.createTrackbar('v1', 'settings', 0,   255, callback)
cv2.createTrackbar('h2', 'settings', 255, 255, callback)
cv2.createTrackbar('s2', 'settings', 255, 255, callback)
cv2.createTrackbar('v2', 'settings', 255, 255, callback)

while True:
    flag, img = cap.read()
    img = cv2.flip(img,1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )

    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    hsv_min = np.array((h1, s1, v1), np.uint8)
    hsv_max = np.array((h2, s2, v2), np.uint8)

    thresh = cv2.inRange(hsv, hsv_min, hsv_max)

    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    if dArea > 100:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x, y), 10, (0,0,255), 2)
        cv2.putText(img, "%d-%d" % (x,y), (x+10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    cv2.imshow('camera', img)
    cv2.imshow('result', thresh)
 
    ch = cv2.waitKey(5)
    if ch == 27:
        break

    if ch == 103:
        cv2.setTrackbarPos('h1', 'settings',green[0][0])
        cv2.setTrackbarPos('s1', 'settings',green[0][1])
        cv2.setTrackbarPos('v1', 'settings',green[0][2])
        cv2.setTrackbarPos('h2', 'settings',green[1][0])
        cv2.setTrackbarPos('s2', 'settings',green[1][1])
        cv2.setTrackbarPos('v2', 'settings',green[1][2])

cap.release()
cv2.destroyAllWindows()
