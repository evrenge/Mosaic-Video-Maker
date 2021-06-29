import cv2
from Helper import HelperOBJ
import numpy as np
import time

class Pokiki:
    def __init__(self):
        self.helperOBJ = HelperOBJ()
        self.last_t3=0
        self.resultIMG=np.zeros((1,1,3), dtype=np.uint8)
        self.resolutions=self.helperOBJ.resolutions

    def convertFromImage(self, img, split_x, split_y):
        print("Start processing image")
        t0 = time.time()
        resolutionId=self.chooseResolution(split_x, split_y)

        tile_W,tile_H = self.resolutions[resolutionId]
        img = cv2.resize(img,(split_x,split_y), interpolation=cv2.INTER_AREA)  # BGR
        img=cv2.add(img , (np.random.randint(16, size=(split_y,split_x,3),dtype=np.int8)-8), dtype=cv2.CV_8U)

        indices = np.zeros([split_y,split_x], np.int32)

        resultIMG=self.resultIMG
        correct_shape=(split_y*tile_H, split_x*tile_W,3)
        if resultIMG.shape!=correct_shape:
            resultIMG=np.zeros(correct_shape, dtype=np.uint8)
            print(f"Image resized to {correct_shape}, tile size: {tile_W}x{tile_H}")
            self.resultIMG=resultIMG
        
        t1 = time.time()
        #query=self.helperOBJ.kdTree.query;
        tiles=self.helperOBJ.tiles[resolutionId]
        findNearestNeighbor=self.helperOBJ.findNearestNeighbor

        for row_index in range(split_y):
            for col_index in range(split_x):
                tile_color = img[row_index, col_index]
                indices[row_index, col_index]=findNearestNeighbor(tile_color)

        t2=time.time()

        for row_index in range(split_y):
            row=resultIMG[row_index*tile_H:(row_index+1)*tile_H]
            for col_index in range(split_x):
                row[:, col_index*tile_W:(col_index+1)*tile_W] =tiles[indices[row_index,col_index]]

        t3 = time.time()
        #resultIMG=cv2.resize(resultIMG, (pictureW, pictureH), interpolation=cv2.INTER_CUBIC)    # interpolation=cv2.INTER_CUBIC
        print("FPS: {:.4f}    Times: +{:.4f}  {:.4f} {:.4f} {:.4f}    {}x{}".format(1/(t3-self.last_t3+1e-10),t0-self.last_t3,t1-t0, t2-t1,t3-t2,resultIMG.shape[0],resultIMG.shape[1]))

        self.last_t3=t3

        return resultIMG

    def chooseResolution(self, split_x, split_y):
        for i,resolution in enumerate(self.resolutions):
            pixelCount=split_x*split_y*resolution[0]*resolution[1]
            if(pixelCount>=2.5e6):
                return i
        return len(self.resolutions)-1