#!/projects/world/venv/bin/python

'''
Generate world.
'''

import os
import random
import time
import timeit
import sys
import cv2
import noise
import numpy as np
from PIL import Image
#from sklearn import preprocessing

#import matplotlib.pyplot as plt

scale = 100
octaves = 7
persistence = 0.55
lacunarity = 3.0
seed = random.randint(0, 100)
displace = random.randint(0, 500000)
shape = (1000, 1000)
#shape = (600, 600)

centre_x = shape[0]/2
centre_y = shape[1]/2

denom_x = pow(centre_x*0.001, 2)
denom_y = pow(centre_y*0.001, 2)

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

        threshold = 0.15

        #Ocean
        if val < threshold + 0.15:
            return  [89, 0, 0]
        #middle
        elif val <  threshold + 0.25:
            return [224, 13, 13]
        #sea
        elif val < threshold + 0.35:
            return [225, 105, 65]
        #Beach
        elif val < threshold + 0.4:
            return [175, 214, 238]
        #Grass
        elif val < threshold + 0.5:
            return [34, 139, 34]
        #Trees
        elif val < threshold + 0.6:
            return [0, 100, 0]
        #Hill
        elif val < threshold + 0.7:
            return [176, 176, 176]
        #Snowcap
        else:
            return [255, 255, 255]
        #if obj["critter"]:
        #    return critter[obj["critter"].get_animal()]

        #return terrains[obj["terrain"]]

    def generate(self, elipse, img=None, coords=None):
        '''
        Generate image.
        Pass image and only update certain values.
        '''
        
        img = np.zeros((shape)+(3,))

        image = list(self.image)
        height = [img[2] for img in image]

        #sys.exit()

        #height = np.asarray(height)
        #norm_height = preprocessing.normalize([height]).tolist()

        c=np.array(height)
        mn = min(c)
        mx = max(c)

        norm_height = (c - mn) / (mx - mn)

        #Load eclipse vals here. Normalize.

        for index in range(len(image)):
            x_val = image[index][0]
            y_val = image[index][1]
            z_val = norm_height[index] #image[index][2]

            z_val *= (1-elipse[index])

            img[x_val][y_val] = self.add_colour(z_val)
            #image[index][2] = norm_height[index]

        #This could be done better..
        image = os.path.join(os.getcwd(), "data", "{}.png".format(str(time.time())))

        cv2.imwrite(image, img)
        print(image)
        Image.open(image).show()

        #return img
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

    return (coords[0], coords[1], z_val)

def elipse(coords):
    '''
    For coordinated, generate elipse...
    Normalise output here?
    '''

    delta_x = coords[0]-centre_x
    delta_y = coords[1]-centre_y
    
    z_val = pow(delta_x, 2)/denom_x + pow(delta_y, 2)/denom_y
    
    return z_val

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

    start = timeit.default_timer()

    #world = World(1920, 1080)
    world = World(shape[0], shape[1])
    #print(map.shape)
    eplipse_array = map(elipse, coords(shape[0], shape[1]))

    #image = map(world_perlin, coords(1920, 1080))
    #image = list(image)
    #print(len(image))

    #elipse_grad = np.zeros_like(image)

    elipse_height = list(eplipse_array)

    c=np.array(elipse_height)
    mn = min(c)
    mx = max(c)
    norm_height = (c - mn) / (mx - mn)

    world.generate(elipse=norm_height)

    print("generate time: ", timeit.default_timer()-start)        

if __name__ == "__main__":
    main()
