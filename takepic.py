import cv2
import time

cap = cv2.VideoCapture(0)

ret,frame = cap.read()
cv2.imwrite('images/test.jpg', frame)

cap.release()

print(cv2.VideoWriter.getBackendName())