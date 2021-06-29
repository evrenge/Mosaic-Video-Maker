import numpy as np
import cv2
import json
from pathlib import Path
from scipy import spatial

class HelperOBJ:

    def __init__(self):
        self.rootFolder = Path('./')
        self.tilesFolder = self.rootFolder / "tiles/"
        self.dataFile = self.rootFolder / "out/data.json"

        self.colors=[]
        self.resolutions=[(12,12), (16,16), (24,24), (36,36), (48,48), (72,72), (108,108)] #W,H
        self.tiles =    [[] for i in self.resolutions]

        data = json.loads(open(str(self.dataFile)).read())

        print("Loading images...")
        for d in data:
            img_path = str(self.tilesFolder / d["name"])
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (76, 86))
            for i,resolution in enumerate(self.resolutions):
                img_tmp=img
                if(img.shape[0]*img.shape[1]>16*resolution[0]*resolution[1]):
                    img_tmp=cv2.resize(img_tmp, (resolution[0]*2,resolution[1]*2) ,interpolation=cv2.INTER_AREA)

                self.tiles[i].append(cv2.resize(img_tmp, resolution,interpolation=cv2.INTER_CUBIC))

            color=d['average_color']
            self.colors.append( [color[2],color[1],color[0]] )

        self.kdTree=spatial.KDTree(self.colors, balanced_tree=False)

        # self.color_cache = np.int16(np.zeros(256*256*256)-1)
        self.color_cache={}

    def findNearestNeighbor(self, color):
        index = (int(color[0])<<16) | (int(color[1])<<8) | int(color[2])

        # if self.color_cache[index]!=-1:
        if index in self.color_cache:
            return self.color_cache[index]

        closest=self.kdTree.query(color)[1]
        self.color_cache[index] = closest
        return closest

def getAverageColor(img):
    return [img[:, :, i].mean() for i in range(img.shape[-1])]