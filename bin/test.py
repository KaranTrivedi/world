#!/projects/world/venv/bin/python

'''
Generate world.
'''

import os
import random
import time
import timeit
from threading import Thread
import cv2
import noise
import numpy as np
from opensimplex import OpenSimplex

scale = 100.0
octaves = 7
persistence = 0.6
lacunarity = 2.0
shape = (1920, 1080)
seed = random.randint(0, 100)
displace = random.randint(0, 500000)

def coords(x_axis, y_axis):
    '''
    Generate list of coordinates.
    '''
    for x_iter in range(x_axis):
        for y_iter in range(y_axis):
            yield x_iter, y_iter

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
        #yield coords[0], coords[1], z_val

def world_simplex(coords):

    x = coords[0]
    y = coords[1]

    simplex = OpenSimplex()
    return simplex.noise2d(x=y, y=y)

def main():

    start = timeit.default_timer()
    
    image = map(world_perlin, coords(1920, 1080))

    image = list(image)

    print(len(image))
    end = timeit.default_timer()
    print("__init__ time: ", end-start)

if __name__ == "__main__":
    main()