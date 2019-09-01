#!/projects/world/venv/bin/python

'''
Generate world.
'''

import random
import time
import timeit

import cv2
import noise
import numpy as np

#from PIL import Image

class World():
    '''
    Generate a map.
    '''
    #generate values -> filter output.
    #build land with dictc. etc. This object would get updated with animals seeding.
    #Animals would spawn x,y,z bound.
    #translate output to image function

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

    def __init__(self, x_len, y_len):
        '''
        Initialize world.
        '''
        start = timeit.default_timer()

        self.shape = (x_len, y_len)
        self.scale = 100.0
        self.octaves = 7
        self.persistence = 0.6
        self.lacunarity = 2.0

        #self.land = [[0 for i_it in range(self.shape[1])] for j_it in range(self.shape[0])]

        self.land = np.zeros((self.shape))
        print(self.land)

        self.seed = random.randint(0, 100)
        displace = random.randint(0, 500000)

        for i_it in range(self.shape[0]):
            for j_it in range(self.shape[1]):
                z_val = noise.pnoise2((i_it+displace)/self.scale,
                                        (j_it+displace)/self.scale,
                                        octaves=self.octaves,
                                        persistence=self.persistence,
                                        lacunarity=self.lacunarity,
                                        repeatx=self.shape[0],
                                        repeaty=self.shape[1],
                                        base=self.seed
                                        )
                self.land[i_it][j_it] = z_val
                #print(i_it, j_it)
                #print(self.land[i_it][j_it])
        end = timeit.default_timer()
        print("__init__ time: ", end-start)

    def get_feature(self, x, y):
        '''
        Return feature for coordinate.
        '''
        (x, y) = (self.land[x][y]["terrain"], self.land[x][y]["critter"])
        return (x, y)

    def add_colour(self, val):
        '''
        Add colour based on elevation.
        '''

        if val < -0.25:
            return  [0, 0, 89]
        elif val < -0.05:
            return [65, 105, 225]
        elif val < 0:
            return [238, 214, 175]
        elif val < 0.2:
            return [34, 139, 34]
        elif val < 0.35:
            return [150, 75, 0]
        else:
            return [255, 255, 255]
        #if obj["critter"]:
        #    return critter[obj["critter"].get_animal()]

        #return terrains[obj["terrain"]]

    def generate(self, img=None, coords=None):
        '''
        Generate image.
        This could be sped up by looking up only a list of pixels that have not yet been assigned.
        Pass image and only update certain values.
        '''
        if img is None:
            img = np.zeros((self.shape)+(3,))

            for x in range(self.shape[0]):
                for y in range(self.shape[1]):
                    try:
                        img[x][y] = self.add_colour(self.land[x][y])[::-1]
                    except Exception as exp:
                        print(exp)
                        print(x, y)
                    #print(self.land[y][x]["terrain"])
        else:
            for i in coords:
                (x, y) = i
                try:
                    img[x][y] = self.add_colour(self.land[x][y])
                except Exception as exp:
                    print(exp)
                    print(i[0], i[1])

        #This could be done better..
        #filename = os.path.join(os.getcwd(), "..", "data", "{}.png".format(str(time.time())))
        image = "/projects/world/data/" + str(time.time()) + ".jpg"
        #image = "../data/" + str(time.time()) + ".jpg"
        cv2.imwrite(image, img)
        return img
        #toimage(img).show()

    def get_spaces(self):
        '''
        Return list fo empty places.
        '''
        coords = []
        for x in range(len(self.land)):
            for y in range(len(self.land[x])):
                if self.land[x][y]["terrain"] == "grass" and self.land[x][y]["critter"] is None:
                    coords.append((x, y))
        return coords

    def add_critter(self, x, y, crit):
        '''
        Add animal to location.
        '''
        self.land[x][y]["critter"] = crit

    def remove_critter(self, x, y):
        '''
        Remove critter from location.
        '''
        self.land[x][y]["critter"] = None

    def get_critter(self, x, y):
        '''
        Return critter in location.
        '''
        return self.land[x][y]["critter"]

def main():
    '''
    Main function.
    '''
    world = World(1920, 1080)
    #print(map.shape)
    world.generate()

if __name__ == "__main__":
    main()
