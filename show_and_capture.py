"""
なんか変更するたびに関数とか変えるの面倒なのでモジュールとか関数とか後から考えよう
本当は変更込みで作っとくべきなんだろうけどめんどくさい
"""

import image_loader as i_l
import video_capture as v_c
import cv2
import numpy as np
import os
from timeit import default_timer as timer


class Video_Capture(v_c.video_capture):

    def __init__(self, fps, log_name):
        super().__init__()
        self.out = cv2.VideoWriter('output.mp4', self.fourcc,   fps, (self.re_w,self.re_h), True)
        self.log = open(log_name, 'w')


    def draw_to_image(self, frame, image_name):
        super().draw_to_image(frame)
        # draw image name
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
        elif key == 0:
            return "up"
        elif key == 1:
            return "down"
        elif key == 2:
            return "left"
        elif key == 3:
            return "right"
        elif key == 32:
            return "space"
        elif key == -1:
            return "none"


    def capture_end(self):
        super().capture_end()
        self.log.close()

class Image_Loader(i_l.image_loader):
    def __init__(self, text_path):
        with open(text_path) as setting:
            self.user_name = setting.readline().strip()
            self.dir_name = setting.readline().strip()
            self.dir_names = setting.readline().split()

            self.iamge_path_list = []
            self.image_name_list = []
            self.image_list = []

            self.search_image()
            self.load_image()



class Show_And_Capture():

    def __init__(self):
        #todo ウィンドウフルサイズは下のが邪魔なのでサイズ調整する
        self.dw = 1440
        self.dh = 900
        self.fps = 20
        self.IL = Image_Loader("setting.txt")
        try:
            os.mkdir(self.IL.user_name)
        except FileExistsError:
            pass
        self.log_name = self.IL.user_name+'/'+self.IL.user_name+"_log.csv"
        self.VC = Video_Capture(self.fps, self.log_name)
        self.win_name = "window"
        self.i,self.j = 0,0

        self.VC.out = cv2.VideoWriter(self.IL.user_name+'/'+self.IL.user_name+'_'+self.IL.dir_names[self.i]+".mp4", self.VC.fourcc, self.fps, (self.VC.re_w, self.VC.re_h), True)
        cv2.namedWindow(self.win_name, cv2.WINDOW_FULLSCREEN)
        self.show_fitted_image(self.IL.image_list[self.i][self.j])

    def show_fitted_image(self, image):
        iw = image.shape[1]
        ih = image.shape[0]

        as_w = self.dw / iw
        as_h = self.dh / ih

        if as_w < as_h:
            resized_image = cv2.resize(image, (int(iw*as_w), int(ih*as_w)))
        else:
            resized_image = cv2.resize(image, (int(iw*as_h), int(ih*as_h)))
        cv2.imshow(self.win_name, resized_image)
        #todo ここにウィンドウの位置の調整を入れる

    def key_control(self, key):
        if key == "break":
            return "break"

        elif key == "right":
            self.j -= 1
            if self.j<0:
                self.j=0
            self.show_fitted_image(self.IL.image_list[self.i][self.j])

        elif key == "left":
            self.j += 1
            if self.j >= len(self.IL.image_list[self.i]):
                if self.i < len(self.IL.dir_names)-1:
                    self.i += 1
                    self.j = 0
                    self.VC.out.release()
                    self.VC.out = cv2.VideoWriter(self.IL.user_name+'/'+self.IL.user_name+'_'+self.IL.dir_names[self.i]+".mp4", self.VC.fourcc, self.fps, (self.VC.re_w, self.VC.re_h), True)
                    self.VC.log.close()
                    self.VC.log = open(self.log_name, 'a')
                else:
                    return "break"
            self.show_fitted_image(self.IL.image_list[self.i][self.j])


    def main_loop(self):
        while True:
            ret, frame = self.VC.cap.read()
            if ret == False:
                print("False in cap.read")
                break

            self.VC.calc_fps()
            self.VC.draw_to_image(frame, self.IL.image_name_list[self.i][self.j])
            self.VC.output(frame, self.IL.image_name_list[self.i][self.j])

            key = self.VC.check_keyboard()
            if key != "none":
                if self.key_control(key) == "break":
                    break

            self.VC.frame_count += 1
        self.VC.capture_end()


def main_ver1():
    IL = Image_Loader("setting.txt")
    log_name = IL.user_name+"_log.csv"
    VC = Video_Capture(20, log_name)
    win_name = "window"

    VC.log.write(IL.user_name + '\n')

    i=0
    j=0
    cv2.namedWindow(win_name, cv2.WINDOW_GUI_NORMAL)
    #cv2.moveWindow("window", 200,200)

    cv2.imshow(win_name, IL.image_list[i][j])

    while True:
        ret, frame = VC.cap.read()
        if ret == False:
            print("Finish")
            break

        VC.calc_fps()
        VC.draw_to_image(frame, IL.image_name_list[i][j])
        VC.output(frame, IL.image_name_list[i][j])

        key = VC.check_keyboard()

        if key == "break":
            break

        if key == "right":
            j -= 1
            if j<0:
                i = (i-1) % len(IL.image_list)
                j = len(IL.image_list[i]) - 1
            cv2.imshow(win_name, IL.image_list[i][j])

        if key == "left":
            j += 1
            if j>=len(IL.image_list[i]):
                j = 0
                i = (i+1) % len(IL.image_list)
            cv2.imshow(win_name, IL.image_list[i][j])


        VC.frame_count += 1

    VC.capture_end()

def main_ver2():
    #ディスプレイの解像度
    dw = 1440
    dh = 900
    #再生fpsの設定
    fps = 20
    #諸々の読み込み
    IL = Image_Loader("setting.txt")
    #ディレクトリ作る
    try:
        os.mkdir(IL.user_name)
    except FileExistsError:
        pass
    #記録用諸々
    log_name = IL.user_name+'/'+IL.user_name+"_log.csv"
    VC = Video_Capture(fps, log_name)
    win_name = "window"
    #ディレクトリ参照用変数
    i,j = 0,0

    #*動画をディレクトリ毎に分けたいがための上書き
    VC.out = cv2.VideoWriter(IL.user_name+'/'+IL.user_name+'_'+IL.dir_names[i]+".mp4", VC.fourcc, fps, (VC.re_w,VC.re_h), True)
    cv2.namedWindow(win_name, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(win_name, IL.image_list[i][j])

    while True:
        ret, frame = VC.cap.read()
        if ret == False:
            print("Finish at cap.read")
            break

        VC.calc_fps()
        VC.draw_to_image(frame, IL.image_name_list[i][j])
        VC.output(frame, IL.image_name_list[i][j])

        key = VC.check_keyboard()

        if key == "break":
            break
        elif key == "right":
            j -= 1
            #*一旦ディレクトリ戻るのはなしに
            if j<0:
                j=0
            cv2.imshow(win_name, IL.image_list[i][j])
        elif key == "left":
            j += 1
            #*ディレクトリの遷移
            if j >= len(IL.image_list[i]):
                #次があればそれへ
                if i < len(IL.dir_names)-1:
                    i += 1
                    j = 0
                #なければ終了
                else:
                    break
                #*ファイル分け用の処理
                VC.out.release()
                VC.out = cv2.VideoWriter(IL.user_name+'/'+IL.user_name+'_'+IL.dir_names[i]+".mp4", VC.fourcc, fps, (VC.re_w,VC.re_h), True)
                VC.log.close()
                VC.log = open(log_name, 'a')

            cv2.imshow(win_name, IL.image_list[i][j])

        VC.frame_count += 1
    VC.capture_end()





if __name__ == "__main__":
    SAC = Show_And_Capture()
    SAC.main_loop()