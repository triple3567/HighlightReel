import cv2
import time

cap= cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cv2.CAP_PROP_FRAME_WIDTH)
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer= cv2.VideoWriter('basicvideo.mjpg', cv2.VideoWriter_fourcc(*'mjpg'), 30, (1280, 720))

start_time = time.time()
while True:
    ret,frame= cap.read()

    writer.write(frame)

    if start_time + 5 < time.time():
        break


cap.release()
writer.release()
cv2.destroyAllWindows()
