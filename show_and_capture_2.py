import argparse
import cv2
import numpy as np
from timeit import default_timer as timer

def: main():



if __name__ == "__main__":
    main()

class ShowCapture:
    """comment"""

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise ImportError("Couldn't open video file or webcam")

        #aspect ratio of video
        self.cap_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.cap_h = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        print(str(self.cap_w) + "  " + str(self.cap_h))

        #ready for calculate fps
        self.accum_time = 0
        self.curr_fps = 0
        self.fps = "FPS: ??"
        self.curr_time = 0
        self.exec_time = 0
        self.prev_time = timer()

        self.frame_count = 1

    def mainloop(self):
        while True:
            ret, frame = self.cap.read()
            if ret == False:
                print("Finish")
                return
            
            """
            # Resize
            im_size = (640, 480)
            resized = cv2.resize(frame, im_size)
            """


    def calc_fps(self):
        self.curr_time = timer()
        self.exec_time = self.curr_time - self.prev_time
        self.prev_time = self.curr_time
        self.accum_time = self.accum_time + self.exec_time
        self.curr_fps += 1
        if self.accum_time > 1:
            self.accum_time -= 1
            self.fps = "FPS." + str(self.curr_fps)
            self.curr_fps = 0
        


