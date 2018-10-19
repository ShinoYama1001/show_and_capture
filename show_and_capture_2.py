import cv2
import numpy as np
from timeit import default_timer as timer

class ShowCapture:
    """
    comment
    """

    re_w = 640
    re_h = 480

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ImportError("Couldn't open video file or webcam")
        #print(self.cap.set(cv2.CAP_PROP_FPS, 10))

        #aspect of video before
        self.cap_w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.cap_h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(str(self.cap_w) + "  " + str(self.cap_h))

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.re_w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.re_h)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter('output.mp4', self.fourcc,   20.0, (self.re_w,self.re_h), True)

        #aspect of video after
        self.cap_w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.cap_h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
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
            
            # Resize
            #im_size = (self.re_w, self.re_h)
            #resized = cv2.resize(frame, im_size)
            #frame = resized.copy()
            
            self.calc_fps()

            self.draw_to_image(frame)

            self.output(frame)

            if self.check_keyboard() == "break":
                break

            self.frame_count += 1

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()


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
        
    def draw_to_image(self, frame):
        # draw fps 
        cv2.rectangle(frame, (250,0), (300,17), (0,0,0), -1)
        cv2.putText(frame, self.fps, (255,10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,255,255), 1)
        # draw frame number
        cv2.rectangle(frame, (0,0), (50,17), (0,0,0), -1)
        cv2.putText(frame, str(self.frame_count), (0,10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,255,255), 1)

    def output(self, frame):
        cv2.imshow("Result", frame)
        self.out.write(frame)
        cv2.imwrite("frames/"+str(self.frame_count)+".jpg", frame)

    def check_keyboard(self):
        key = cv2.waitKey(1)

        if key == ord('q'):
            return "break"


def main():
    print("Opencv Version:", cv2.__version__)

    SC = ShowCapture()

    SC.mainloop()



if __name__ == "__main__":
    main()
