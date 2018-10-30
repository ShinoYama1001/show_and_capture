import image_loader as i_l
import video_capture as v_c
import cv2
import numpy as np
from timeit import default_timer as timer


class Video_Capture(v_c.video_capture):

    def __init__(self, fps):
        super().__init__()
        self.out = cv2.VideoWriter('output.mp4', self.fourcc,   fps, (self.re_w,self.re_h), True)
        self.log = open("log.csv", 'w')

    
    def draw_to_image(self, frame, image_name):
        super().draw_to_image(frame)
        cv2.rectangle(frame, (450,0), (550,17), (0,0,0), -1)
        cv2.putText(frame, image_name, (455,10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,255,255), 1)

    def output(self, frame, image_name):
        #cv2.imshow("Result", frame)
        self.out.write(frame)
        self.log.write(str(self.frame_count)+','+str(self.total_time)+','+image_name+'\n')


    def check_keyboard(self):
        key = cv2.waitKey(1)

        if key == ord('q'):
            return "break"
        if key == 3:
            return "right"
        if key == 2:
            return "left"

    def capture_end(self):
        super().capture_end()
        self.log.close()




if __name__ == "__main__":
    VC = Video_Capture(30)
    IL = i_l.image_loader("testlist.txt")

    i=0
    cv2.imshow("window", IL.image_list[i])

    while True:
        ret, frame = VC.cap.read()
        if ret == False:
            print("Finish")
            break
            
        VC.calc_fps()
        VC.draw_to_image(frame, IL.image_name_list[i])
        VC.output(frame, IL.image_name_list[i])

        key = VC.check_keyboard()
        if key == "break":
            break
        if key == "right":
            i += 1
            i = i % len(IL.image_list)
            cv2.imshow("window", IL.image_list[i])
        if key == "left":
            i -= 1
            i = i % len(IL.image_list)
            cv2.imshow("window", IL.image_list[i])

        VC.frame_count += 1
        
    VC.capture_end()