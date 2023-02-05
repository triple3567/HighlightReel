import cv2
import time
import sys

cap = cv2.VideoCapture(sys.argv[1])

ret,frame = cap.read()
cv2.imwrite('../out/test.jpg', frame)

cap.release()
