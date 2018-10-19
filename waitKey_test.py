import cv2
import time

cv2.namedWindow("hoge")

while True:
    key = cv2.waitKey(1)

    print(key)

    if key == ord('q'):
        break

    time.sleep(0.5)


"""
none -1

-> (63235) 3
<- (63234) 2

"""