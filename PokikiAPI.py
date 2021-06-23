import cv2
from Helper import HelperOBJ
import numpy as np
import time

class Pokiki:
    def __init__(self):
        self.helperOBJ = HelperOBJ()
        self.last_t3=0
        self.resultIMG=np.zeros((1,1,3), dtype=np.uint8)

    def convertFromImage(self, img, split_x, split_y):
        print("Start processing image")
        t0 = time.time()

        img = cv2.resize(img,(split_x,split_y), interpolation=cv2.INTER_AREA)
        indices = np.zeros([split_y,split_x], np.int32)

        resultIMG=self.resultIMG
        if resultIMG.shape!=(split_y*86, split_x*76,3):
            resultIMG=np.zeros((split_y*86, split_x*76,3), dtype=np.uint8)
            print("Image resized")
            self.resultIMG=resultIMG

        t1 = time.time()
        #query=self.helperOBJ.kdTree.query;
        tiles=self.helperOBJ.tiles
        findNearestNeighbor=self.helperOBJ.findNearestNeighbor

        for row_index in range(split_y):
            for col_index in range(split_x):
                tile_color = img[row_index, col_index]
                indices[row_index, col_index]=findNearestNeighbor(tile_color)

        t2=time.time()

        for row_index in range(split_y):
            row=resultIMG[row_index*86:(row_index+1)*86]
            for col_index in range(split_x):
                row[:, col_index*76:(col_index+1)*76] =tiles[indices[row_index, col_index]]

        t3 = time.time()
        #resultIMG=cv2.resize(resultIMG, (pictureW, pictureH), interpolation=cv2.INTER_CUBIC)    # interpolation=cv2.INTER_CUBIC


        print("Times: +{:.4f}  {:.4f} {:.4f} {:.4f}  ".format(t0-self.last_t3,t1-t0, t2-t1,t3-t2))
        print("FPS: {:.4f}".format(1/(t3-t0+1e-10)))
        print()

        self.last_t3=t3
        return resultIMG
