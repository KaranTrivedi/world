#!./venv/bin/python

"""
Generate world.
"""

# TODO: https://stackoverflow.com/questions/35590724/filling-color-on-image-with-python 
# PIL.ImageDraw.floodfill

import os
import random
import time
import math
import timeit
import sys
import cv2
import noise
import numpy as np

from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

height = 1080
width = 1920

shape = (height, width)

# Increase to zoom into continents.
scale = 300

octaves = 9
# Increase to get more and more islands.
persistence = 0.6
# Increase to increase fuziness within a smaller range.
lacunarity = 2
# seed = 2
seed = random.randint(0, 100)
# displace = 25000
displace = random.randint(0, 500000)

class World:
    """
    Generate a map.

    Returns:
        [type]: [description]
    """

    # generate values -> filter output.
    # build land with dictc. etc. This object would get updated with animals seeding.
    # translate output to image function

    def __init__(self, x_len, y_len):
        """
        Initialize world.
        """

        coord = coords(x_len, y_len)

        # POOL
        start = timeit.default_timer()
        self.image = map(world_perlin, coord)
        print("Create Noise img: ", timeit.default_timer() - start)

    def add_colour(self, val):
        """
        Add colour based on elevation.
        """

        threshold = 0.0
        # BGR
        # Ocean
        if val < threshold + 0.05:
            return [89, 0, 0]
        # middle
        elif val < threshold + 0.15:
            return [224, 13, 13]
        # sea
        elif val < threshold + 0.375:
            return [225, 105, 65]
        # Beach
        elif val < threshold + 0.4:
            return [175, 214, 238]
        # Grass
        elif val < threshold + 0.5:
            return [34, 139, 34]
        # Trees
        elif val < threshold + 0.6:
            return [0, 100, 0]
        # Hill
        elif val < threshold + 0.7:
            return [35, 87, 133]
        # Mountain
        elif val < threshold + 0.8:
            return [176, 176, 176]
        # Return snowcap.
        return [255, 255, 255]

    def generate(self, elipse=None, img=None, coords=None):
        """
        Generate image.
        Pass image and only update certain values.
        """
        start = timeit.default_timer()

        img = np.zeros((shape) + (3,))

        # new = np.fromiter(self.image, dtype=[tuple])

        # Leave this as an iterator? 
        image = list(self.image)
        height = [img[2] for img in image]

        # Normalize given heights.
        c = np.array(height)
        mn = min(c)
        mx = max(c)
        norm_height = (c - mn) / (mx - mn)

        # Load eclipse vals here. Normalize.
        print("Setup: ", timeit.default_timer() - start)

        start = timeit.default_timer()
        # POOL THIS
        for index in range(len(image)):
            x_val = image[index][0]
            y_val = image[index][1]
            z_val = norm_height[index]

            # Multiplying z val to actually add elipse.
            if elipse:
                z_val *= 1 - elipse[index]

            img[x_val][y_val] = self.add_colour(z_val)
        print("Create img: ", timeit.default_timer() - start)
        # This could be done better..
        return img
        # toimage(img).show()


def world_perlin(coords):
    """
    Initialize world.
    """
    z_val = noise.pnoise2(
        (coords[0] + displace) / scale,
        (coords[1] + displace) / scale,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        repeatx=shape[0],
        repeaty=shape[1],
        base=seed,
    )

    return [coords[0], coords[1], z_val]


def generate_elipse(coords):
    """
    For coordinated, generate elipse...
    Normalise output here?
    """

    scalar = 0.9

    centre_x = shape[0] / 2
    centre_y = shape[1] / 2

    denom_x = pow(centre_x, 2)
    denom_y = pow(centre_y, 2.2)

    delta_x = coords[0] - centre_x
    delta_y = coords[1] - centre_y

    z_val = pow(delta_x, 2) / denom_x + pow(delta_y, 2) / denom_y

    return z_val

def write_image(path, image):    
    """
    Commit image to disk.

    Args:
        path (str): Path to write image to, including name.
        image (list): image object.
    """

    cv2.imwrite(path, image)
    print(path)
    # Image.open(image_path).show()

def coords(x_axis, y_axis):
    """
    Generate list of coordinates.
    """
    for x_iter in range(x_axis):
        for y_iter in range(y_axis):
            yield x_iter, y_iter

def add_border():

    images_path = Path("/home/karan/q8ueato/cache/")

    map_image = Image.open(str(images_path / "test.png"))
    border_image = Image.open(str(images_path / "border2.jpg"))

    border_resize = 75
    border_image = border_image.resize((border_resize, border_resize))

    for y in range(int(map_image.size[1]/border_resize)+1):
        map_image.paste(border_image, (0, y*border_resize))
        map_image.paste(border_image, (width-border_resize, y*border_resize))

    border_image = border_image.rotate(90)
    #image brightness enhancer
    enhancer = ImageEnhance.Brightness(border_image)

    # factor = 1 #gives original image
    # factor = 0.5 #darkens the image
    factor = 1.5 #brightens the image
    border_image = enhancer.enhance(factor)

    for x in range(int(map_image.size[0]/border_resize)+1):
        map_image.paste(border_image, (x*border_resize, 0))
        map_image.paste(border_image, (x*border_resize, height-border_resize))

    font_colour = (255,255,255)
    # font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 25)
    draw = ImageDraw.Draw(map_image)
    draw.text((border_resize, height-border_resize-10), f"Scale: {scale}", font_colour)
    draw.text((border_resize, height-border_resize-20), f"octaves: {octaves}", font_colour)
    draw.text((border_resize, height-border_resize-30), f"persistence: {persistence}", font_colour)
    draw.text((border_resize, height-border_resize-40), f"lacunarity: {lacunarity}", font_colour)
    draw.text((border_resize, height-border_resize-50), f"seed: {seed}", font_colour)
    draw.text((border_resize, height-border_resize-60), f"displace: {displace}", font_colour)

    map_image.save(str(images_path / "test2.png"))

    sys.exit()

def main():
    """
    Main function.
    """

    images_path = Path("/home/karan/q8ueato/cache/")

    start = timeit.default_timer()

    # world = World(1920, 1080)
    world = World(shape[0], shape[1])
    # print(map.shape)

    eplipse_array = map(generate_elipse, coords(shape[0], shape[1]))
    print("Elipse creation: ", timeit.default_timer() - start)

    start = timeit.default_timer()

    # Leave this as an iterator? 

    elipse_height = list(eplipse_array)
    print("List elipse height: ", timeit.default_timer() - start)

    generated_image = world.generate(elipse=elipse_height)
    # generated_image = world.generate()

    # Need to add rivers?
    # Need to add legend?

    write_image(str(images_path / "test.png"), generated_image)

    add_border()

if __name__ == "__main__":
    main()
