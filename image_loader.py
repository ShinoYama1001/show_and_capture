import os
import numpy as np
import cv2

class image_loader:

    def __init__(self, path):
        with open(path) as textfile:
            self.dir_name = textfile.readline().strip()
            self.dir_names = textfile.readline().split()

            self.iamge_path_list = []
            self.image_name_list = []
            self.image_list = []

            self.search_image()
            self.load_image()

    def search_image(self):
        for d_name in self.dir_names:
            path = self.dir_name+'/'+d_name
            files = os.listdir(path)
            files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]

            for item in files_file:
                if ".jpg" in item or ".png" in item:
                    self.iamge_path_list.append(path+'/'+item)
                    self.image_name_list.append(item)
                    #print(item)
            #print(self.iamge_path_list)

    def load_image(self):
        for item in self.iamge_path_list:
            img = cv2.imread(item)
            self.image_list.append(img)






if __name__=="__main__":
    il = image_loader("testlist.txt")

    print(il.iamge_path_list)
    print(il.image_name_list)

    for image in il.image_list:
        cv2.imshow("image", image)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

