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

        self.tiles =[]
        self.colors=[]

        data = json.loads(open(str(self.dataFile)).read())

        print("Loading images...")
        for d in data:
            img_path = str(self.tilesFolder / d["name"])
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (76, 86))
            self.tiles.append(img)
            color=d['average_color']
            self.colors.append( [color[2],color[1],color[0]] )

        self.kdTree=spatial.KDTree(self.colors, balanced_tree=False)

        # self.color_cache = np.int16(np.zeros(256*256*256)-1)
        self.color_cache={}

    def findNearestNeighbor(self, color):
        r, g, b = int(color[0]), int(color[1]), int(color[2])

        index = (r<<16) | (g<<8) | b
        # if self.color_cache[index]!=-1:
        if index in self.color_cache:
            return self.color_cache[index]

        closest=self.kdTree.query(color)[1]
        self.color_cache[index] = closest
        return closest

def getAverageColor(img):
    return [img[:, :, i].mean() for i in range(img.shape[-1])]
