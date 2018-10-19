"""
memo


keyWait
-> : 63235
<- : 63234
q  : ord('q')


"""
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))

img = cv2.imread("cloud.png")
img2 = cv2.imread("image.png")

cv2.imshow("image", img)

wait = 0
count = 0

while(cap.isOpened()):
    ret, frame = cap.read()
    

    if ret==True:
        # write the frame
        #cv2.imwrite("frames/"+str(count)+".png", frame)
        #count += 1

        out.write(frame)

        if wait>0:
            wait = wait-1

        if wait==0:
            key = cv2.waitKey(1)

            if key == 3:
                wait = 5
                print("right")
                cv2.imshow("image", img)
            elif key == 2:
                wait = 5
                print("left")
                cv2.imshow("image", img2)
            elif key == ord("q"):
                break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()