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
        os.remove("output.mp4")

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
        # ウィンドウの解像度
        self.dw = 1440
        self.dh = 900 - 50 #上の枠ぶんはみ出ることに気づいた
        self.fps = 20
        self.IL = Image_Loader("setting.txt")
        # データ格納用フォルダがなければ作る
        try:
            os.mkdir(self.IL.user_name)
        except FileExistsError:
            pass
        # 諸々の下準備
        self.log_name = self.IL.user_name+'/'+self.IL.user_name+"_log.csv"
        self.VC = Video_Capture(self.fps, self.log_name)
        self.win_name = "test_program"
        self.i,self.j = 0,0
        self.VC.out = cv2.VideoWriter(self.IL.user_name+'/'+self.IL.user_name+'_'+self.IL.dir_names[self.i]+".mp4", self.VC.fourcc, self.fps, (self.VC.re_w, self.VC.re_h), True)
        # 最初に表示する分
        cv2.namedWindow(self.win_name, cv2.WINDOW_FULLSCREEN)
        self.show_fitted_image(self.IL.image_list[self.i][self.j])

    # 画像を画面の大きさに合わせて表示する関数　表示には全部これを使う
    def show_fitted_image(self, image):
        # 画像サイズ取得
        iw = image.shape[1]
        ih = image.shape[0]
        # 画像の比率計算
        as_w = self.dw / iw
        as_h = self.dh / ih
        # 調整後のサイズ格納用変数
        resized_w, resized_h = 0,0

        # 縦か横かどっちかに合わせる
        if as_w < as_h:
            resized_w = int(iw*as_w)
            resized_h = int(ih*as_w)
            resized_image = cv2.resize(image, (resized_w, resized_h))
        else:
            resized_w = int(iw*as_h)
            resized_h = int(ih*as_h)
            resized_image = cv2.resize(image, (resized_w, resized_h))
        # 合わせた大きさで表示し、中央へ移動する
        cv2.imshow(self.win_name, resized_image)
        cv2.moveWindow(self.win_name, int((self.dw - resized_w)/2), int((self.dh - resized_h)/2))

    # キー入力による処理の分岐
    def key_control(self, key):
        if key == "break":
            return "break"

        # 右で戻る　前のディレクトリには戻れない
        elif key == "right":
            self.j -= 1
            if self.j<0:
                self.j=0
            self.show_fitted_image(self.IL.image_list[self.i][self.j])

        # 左で進む　ディレクトリをまたぐ時、記録ファイルを区切る
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

        # 上で上側を拡大表示
        elif key == "up":
            iw = self.IL.image_list[self.i][self.j].shape[1]
            ih = self.IL.image_list[self.i][self.j].shape[0]
            cutted_image = self.IL.image_list[self.i][self.j].copy()[0:int(ih*0.6), 0:iw]
            self.show_fitted_image(cutted_image)

        # 下で下側を拡大表示
        elif key == "down":
            iw = self.IL.image_list[self.i][self.j].shape[1]
            ih = self.IL.image_list[self.i][self.j].shape[0]
            cutted_image = self.IL.image_list[self.i][self.j].copy()[int(ih*0.4):ih, 0:iw]
            self.show_fitted_image(cutted_image)

        # スペースで元の大きさに戻す
        elif key == "space":
            self.show_fitted_image(self.IL.image_list[self.i][self.j])

    # メインの処理
    def main_loop(self):
        while True:
            # フレームの取得
            ret, frame = self.VC.cap.read()
            if ret == False:
                print("False in cap.read")
                break

            # 諸々出力
            self.VC.calc_fps()
            self.VC.draw_to_image(frame, self.IL.image_name_list[self.i][self.j])
            self.VC.output(frame, self.IL.image_name_list[self.i][self.j])

            # キーボード操作
            key = self.VC.check_keyboard()
            if key != "none":
                if self.key_control(key) == "break":
                    break

            self.VC.frame_count += 1
        # 出て来たら終わり
        self.VC.capture_end()


# メイン関数
if __name__ == "__main__":
    SAC = Show_And_Capture()
    SAC.main_loop()