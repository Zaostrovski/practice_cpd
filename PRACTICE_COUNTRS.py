import cv2
import numpy as np 

import math

if __name__ == '__main__':
    def callback(*arg):
        pass

blue_ball = np.array(((95, 105, 160),(102, 255, 255)))
green_ball = np.array(((95, 105, 160),(102, 255, 255)))

cv2.namedWindow("result")
cv2.namedWindow("camera")
cv2.namedWindow( "settings" ) # создаем окно настроек

cap = cv2.VideoCapture(0)

# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0,   255, callback)
cv2.createTrackbar('s1', 'settings', 0,   255, callback)
cv2.createTrackbar('v1', 'settings', 0,   255, callback)
cv2.createTrackbar('h2', 'settings', 255, 255, callback)
cv2.createTrackbar('s2', 'settings', 255, 255, callback)
cv2.createTrackbar('v2', 'settings', 255, 255, callback)

color_blue = (255,0,0)
color_red = (0,0,128)

while True:
    flag, img = cap.read()
    img = cv2.flip(img,1) # отражение кадра вдоль оси Y
    img_blur = cv2.GaussianBlur(img,(7,7),0) 
    # преобразуем RGB картинку в HSV модель
    try:
        hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV )

    # считываем значения бегунков
        h1 = cv2.getTrackbarPos('h1', 'settings')
        s1 = cv2.getTrackbarPos('s1', 'settings')
        v1 = cv2.getTrackbarPos('v1', 'settings')
        h2 = cv2.getTrackbarPos('h2', 'settings')
        s2 = cv2.getTrackbarPos('s2', 'settings')
        v2 = cv2.getTrackbarPos('v2', 'settings')

        hsv_min = np.array((h1, s1, v1), np.uint8)
        hsv_max = np.array((h2, s2, v2), np.uint8)


    # накладываем фильтр на кадр в модели HSV
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)
        contours0, hierarchy = cv2.findContours( thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   
        for cnt in contours0:
            if len(cnt)>4:
                ellipse = cv2.fitEllipse(cnt)
                area = round((ellipse[1][0])*(ellipse[1][1]),2) # вычисление площади
                if area > 500:
                    x = int(ellipse[0][0])
                    y = int(ellipse[0][1])
                    ellipse = cv2.ellipse(img,ellipse,(0,0,255),2)

                    cv2.circle(img, (x,y), 5, (0,255,255), -10)
                    cv2.putText(img, "%d:%d" % (x,y), (x + 10,y+10 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            


    # формируем начальный и конечный цвет фильтра
        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        cv2.imshow('camera', img)
        cv2.imshow('result', thresh)
 
        ch = cv2.waitKey(5)
        if ch == 27:
            break

        if ch == 103:
            cv2.setTrackbarPos('h1', 'settings',blue_ball[0][0])
            cv2.setTrackbarPos('s1', 'settings',blue_ball[0][1])
            cv2.setTrackbarPos('v1', 'settings',blue_ball[0][2])
            cv2.setTrackbarPos('h2', 'settings',blue_ball[1][0])
            cv2.setTrackbarPos('s2', 'settings',blue_ball[1][1])
            cv2.setTrackbarPos('v2', 'settings',blue_ball[1][2])
    except:
        cap.release()
        raise
    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()
