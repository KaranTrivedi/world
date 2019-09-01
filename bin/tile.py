
'''
Define Tile in the world.
'''

import noise
import numpy as np
#from scipy.misc import toimage
import sys
import random
import cv2
from time import sleep
import time
import subprocess

#from PIL import Image

class Tile():
    '''
    Generate a Tile.
    '''
    #generate values -> filter output.
    #build land with dictc. etc. This object would get updated with animals seeding.
    #Animals would spawn x,y,z bound.
    #translate output to image function
    def __init__(self,x,y):
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                z   = noise.pnoise2((x+displace)/self.scale,
                                    (y+displace)/self.scale,
                                    octaves=self.octaves,
                                    persistence=self.persistence,
                                    lacunarity=self.lacunarity,
                                    repeatx=self.shape[0],
                                    repeaty=self.shape[1],
                                    base=self.seed)
                
                self.land[x][y] = self.add_features(z)
    
    def add_features(self, z):
        feature = {}
        feature["z"]        = z
        feature["critter"]  = None
        if z < -0.25:
            feature["terrain"] = "deep"
        elif z < -0.05:
            feature["terrain"] = "water"
        elif z < 0:
            feature["terrain"] = "beach"
        elif z < 0.2:
            feature["terrain"] = "grass"
        elif z < 0.35:
            feature["terrain"] = "mountain"
        else:
            feature["terrain"] = "snow"
        return feature
    
    def get_feature(self,x,y):
        (x,y) = (self.land[x][y]["terrain"],self.land[x][y]["critter"])
        return (x,y)

    def add_colour(self, obj):
        terrains = {
            "deep"    : [0, 0, 89],
            "water"   : [65, 105, 225],
            "grass"   : [34, 139, 34],
            "beach"   : [238, 214, 175],
            "mountain": [150, 75, 0],
            "snow"    : [255, 255, 255]
        }
        critter = {
            "rabbit": [0, 0, 0],
            "wolf"  : [255, 255, 255]
        }
        if obj["critter"]:
            return critter[obj["critter"].get_animal()]
        else:
            return terrains[obj["terrain"]]

    def generate(self,img,coords):
        '''
        Generate image. 
        This could be sped up by looking up only a list of pixels that have not yet been assigned.
        Pass image and only update certain values.
        '''
        if img is None:
            img     = np.zeros((self.shape)+(3,))

            for x in range(self.shape[0]):
                for y in range(self.shape[1]):
                    try:
                        img[x][y] = self.add_colour(self.land[x][y])[::-1]
                    except Exception as e:
                        print(e)
                        print(x,y)
                    #print(self.land[y][x]["terrain"])
        else:
            for i in coords:
                (x,y) = i
                try:
                    img[x][y] = self.add_colour(self.land[x][y])[::-1]
                except Exception as e:
                    print(e)
                    print(i[0],i[1])

        #This could be done better.. 
        image = "/projects/sim/data/" + str(time.time()) + ".jpg"
        cv2.imwrite(image,img)
        return img
        #toimage(img).show()
                    
    def get_spaces(self):
        coords = []
        for x in range(len(self.land)):
            for y in range(len(self.land[x])):
                if self.land[x][y]["terrain"] == "grass" and self.land[x][y]["critter"] is None:
                    coords.append((x, y))
        return coords

    def add_critter(self,x,y,crit):
        self.land[x][y]["critter"] = crit
    
    def remove_critter(self,x,y):
        self.land[x][y]["critter"] = None
    
    def get_critter(self,x,y,crit):
        return self.land[x][y]["critter"]

def main():
    pass
    tile = Tile()
    #print(map.shape)
    #world.generate(img=None,coords=None)

if __name__=="__main__":
    main()
