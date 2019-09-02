#!/projects/world/venv/bin/python

'''
Generate world.
'''

import os
import random
import time
import timeit

import cv2
import noise
import numpy as np


scale = 100.0
octaves = 7
persistence = 0.6
lacunarity = 2.0
seed = random.randint(0, 100)
displace = random.randint(0, 500000)
shape = (1080, 1920)

#from PIL import Image

class World():
    '''
    Generate a map.
    '''
    #generate values -> filter output.
    #build land with dictc. etc. This object would get updated with animals seeding.
    #Animals would spawn x,y,z bound.
    #translate output to image function

    def __init__(self, x_len, y_len):
        '''
        Initialize world.
        '''

        coord = coords(x_len, y_len)

        self.image = map(world_perlin, coord)

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
        Pass image and only update certain values.
        '''
        start = timeit.default_timer()
        img = np.zeros((shape)+(3,))

        #if img is None:
        #    img = np.zeros((self.shape)+(3,))
        #    for x in range(self.shape[0]):
        #        for y in range(self.shape[1]):
        #            try:
        #                img[x][y] = self.add_colour(self.image[x][y])[::-1]
        #            except Exception as exp:
        #                print(exp)
        #                print(x, y)
        #            #print(self.land[y][x]["terrain"])
        #else:
        #    for i in coords:
        #        (x, y) = i
        #        try:
        #            img[x][y] = self.add_colour(self.land[x][y])
        #        except Exception as exp:
        #            print(exp)
        #            print(i[0], i[1])

        image = list(self.image)

        for pixel in image:
            img[pixel[0]][pixel[1]] = self.add_colour(pixel[2])[::-1]

        #This could be done better..
        image = os.path.join(os.getcwd(), "data", "{}.png".format(str(time.time())))
        #image = "/projects/world/data/" + str(time.time()) + ".jpg"
        cv2.imwrite(image, img)

        print("generate time: ", timeit.default_timer()-start)

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


def world_perlin(coords):
    '''
    Initialize world.
    '''

    z_val = noise.pnoise2((coords[0]+displace)/scale,
                                (coords[1]+displace)/scale,
                                octaves=octaves,
                                persistence=persistence,
                                lacunarity=lacunarity,
                                repeatx=shape[0],
                                repeaty=shape[1],
                                base=seed
                                )
        
    return coords[0], coords[1], z_val

def coords(x_axis, y_axis):
    '''
    Generate list of coordinates.
    '''
    for x_iter in range(x_axis):
        for y_iter in range(y_axis):
            yield x_iter, y_iter

def main():
    '''
    Main function.
    '''
    #world = World(1920, 1080)
    world = World(shape[0], shape[1])
    #print(map.shape)
    world.generate()

if __name__ == "__main__":
    main()
