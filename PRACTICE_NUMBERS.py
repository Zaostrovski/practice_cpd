import cv2
import easyocr
import numpy as np 
import imutils

if __name__ == '__main__':
    def callback(*arg):
        pass
SCALE = 4
THICK = 3
WHITE = (255, 255, 255)
digits = []
for digit in map(str, range(10)):
    (width, height), bline = cv2.getTextSize(digit, cv2.FONT_HERSHEY_SIMPLEX, SCALE, THICK)
    digits.append(np.zeros((height + bline, width), np.uint8))
    cv2.putText(digits[-1], digit, (0, height), cv2.FONT_HERSHEY_SIMPLEX,SCALE, WHITE, THICK)
    x0, y0, w, h = cv2.boundingRect(digits[-1])
    digits[-1] = digits[-1][y0:y0+h, x0:x0+w]

def detect(img):
    # сравниваем полученную цифру с нашей базой
    percent_white_pix = 0
    digit = -1
    for i, d in enumerate(digits):
        scaled_img = cv2.resize(img, d.shape[:2][::-1])
        # d AND (scaled_img XOR d)
        bitwise = cv2.bitwise_and(d, cv2.bitwise_xor(scaled_img, d))
        # результат определяется наибольшей потерей белых пикселей
        before = np.sum(d == 255)
        matching = 100 - (np.sum(bitwise == 255) / before * 100)
        #cv2.imshow('digit_%d' % (9-i), bitwise)
        if percent_white_pix < matching:
            percent_white_pix = matching
            digit = i
    return digit    

cv2.namedWindow("camera")
cv2.namedWindow("result")

cap = cv2.VideoCapture(0)

while True:
    flag, img = cap.read()
    #img = cv2.flip(img,1) # отражение кадра вдоль оси Y
    # преобразуем RGB картинку в GRAY модель
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
    img_filter = cv2.bilateralFilter(gray, 10, 15, 15)
    # выполняем обратное бинарное пороговое выделение, чтобы цифры выделялись белым на черном
    ret, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
    # проверяется размер контура, чтобы избежать обработки "дефекта".
        if cv2.contourArea(cnt) > 1000 and cv2.contourArea(cnt) < 15000:
            # получаем прямоугольник, окружающий число
            brect = cv2.boundingRect(cnt)
            x,y,w,h = brect
            roi = thresh[y:y+h, x:x+w]
            # определение
            digit = detect(roi)
            cv2.rectangle(img, brect, (0,255,0), 2)
            cv2.putText(img, str(digit), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (190, 123, 68), 2)

    cv2.imshow('camera', img)
    cv2.imshow('result', thresh)
    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()