import cv2
import numpy as np
from timeit import default_timer as timer

class video_capture:
    """
    comment

    default
    1280 720
    """

    re_w = 1280
    re_h = 720

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ImportError("Couldn't open video file or webcam")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.re_w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.re_h)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter('output.mp4', self.fourcc,   20.0, (self.re_w,self.re_h), True)

        #aspect of video 
        self.cap_w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.cap_h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #print(str(self.cap_w) + "  " + str(self.cap_h))

        #ready for calculate fps
        self.accum_time = 0
        self.curr_fps = 0
        self.fps = "FPS: ??"
        self.curr_time = 0
        self.exec_time = 0
        self.prev_time = timer()

        self.total_time = 0
        self.frame_count = 1


    def calc_fps(self):
        self.curr_time = timer()
        self.exec_time = self.curr_time - self.prev_time
        self.prev_time = self.curr_time
        self.accum_time = self.accum_time + self.exec_time
        self.curr_fps += 1
        if self.accum_time > 1:
            self.accum_time -= 1
            self.total_time += 1
            self.fps = "FPS." + str(self.curr_fps)
            self.curr_fps = 0
        
    def draw_to_image(self, frame):
        # draw frame number
        cv2.rectangle(frame, (0,0), (200,17), (0,0,0), -1)
        cv2.putText(frame, str(self.frame_count), (0,10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,255,255), 1)
        # draw fps 
        cv2.rectangle(frame, (250,0), (300,17), (0,0,0), -1)
        cv2.putText(frame, self.fps, (255,10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,255,255), 1)
        # draw toatal time
        cv2.rectangle(frame, (350,0), (400,17), (0,0,0), -1)
        cv2.putText(frame, str(self.total_time), (355,10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,255,255), 1)

    def output(self, frame):
        cv2.imshow("Result", frame)
        self.out.write(frame)
        #cv2.imwrite("frames/"+str(self.frame_count)+".jpg", frame)

    def check_keyboard(self):
        key = cv2.waitKey(1)

        if key == ord('q'):
            return "break"

    def capture_end(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()


def main():
    #print("Opencv Version:", cv2.__version__)

    SC = video_capture()

    while True:
        ret, frame = SC.cap.read()
        if ret == False:
            print("Finish")
            break
            
        SC.calc_fps()

        SC.draw_to_image(frame)

        SC.output(frame)

        if SC.check_keyboard() == "break":
            break

        SC.frame_count += 1
        print(SC.total_time)

    SC.capture_end()


if __name__ == "__main__":
    main()
