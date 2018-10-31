import os
import numpy as np
import cv2

class image_loader:

    def __init__(self, path):
        with open(path) as textfile:
            self.dir_name = textfile.readline().strip()
            self.dir_names = textfile.readline().split()

            #それぞれはディレクトリごとのリストのリストをもつ
            self.iamge_path_list = []
            self.image_name_list = []
            self.image_list = []

            self.search_image()
            self.load_image()

    # ディレクトリごとにjpg,pngファイルを探し、その相対パスと画像名をリストに保存
    def search_image(self):
        for d_name in self.dir_names:
            path = self.dir_name+'/'+d_name
            files = os.listdir(path)
            files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
            image_list_in_dir = [s for s in files_file if ".jpg" in s or ".png" in s]

            self.iamge_path_list.append([path+'/'+s for s in image_list_in_dir])
            self.image_name_list.append(image_list_in_dir)

    # image_path_listに従いimage_listに画像のリストのリストを格納
    def load_image(self):
        img_list = []
        for list in self.iamge_path_list:
            for item in list:
                img = cv2.imread(item)
                img_list.append(img)
            self.image_list.append(img_list)
            img_list =[]




if __name__=="__main__":
    il = image_loader("setting.txt")

    print(il.iamge_path_list)
    print(il.image_name_list)


    for list in il.image_list:
        for item in list:
            cv2.imshow("image", item)
            cv2.waitKey(0)

    cv2.destroyAllWindows()

