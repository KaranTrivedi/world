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
from PIL import Image

scale = 100.0
octaves = 7
persistence = 0.6
lacunarity = 2.0
shape = (1920, 1080)
seed = random.randint(0, 100)
displace = random.randint(0, 500000)

centre_x = shape[0]/2
centre_y = shape[1]/2

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

def elipse(coords):
    '''
    For coordinated, generate elipse...
    Normalise output here?
    '''

    delta_x = coords[0]-centre_x
    delta_y = coords[1]-centre_y
    
    z_val = pow(delta_x, 2)/pow(centre_x, 2) + pow(delta_y, 2)/pow(centre_y, 2)
    
    return [coords[0], coords[1], z_val]

def main():

    start = timeit.default_timer()

    eplipse_array = map(elipse, coords(shape[0], shape[1]))

    #image = map(world_perlin, coords(1920, 1080))
    #image = list(image)
    #print(len(image))

    #elipse_grad = np.zeros_like(image)

    image = list(eplipse_array)
    print(len(image))
    height = [img[2] for img in image]
    img = np.zeros((shape))

    c=np.array(height)
    mn = min(c)
    mx = max(c)
    norm_height = (c - mn) / (mx - mn)

    print(min(norm_height))
    print(max(norm_height))

    for index in range(len(image)):
        image[index][2] = norm_height[index]

    #return image

    #for index in range(len(image)):
    #    x_val = image[index][0]
    #    y_val = image[index][1]
    #    z_val = norm_height[index] #image[index][2]
    #    #z_val *= eclipse[index][2]
    #    img[x_val][y_val] = float(z_val)

    #image = os.path.join(os.getcwd(), "data", "{}.png".format(str(time.time())))

    #cv2.imwrite(image, img)
    ##print(image)
    ##Image.open(image).show()
    
    Image.fromarray(img).show()
    
    end = timeit.default_timer()
    print("__init__ time: ", end-start)

if __name__ == "__main__":
    main()