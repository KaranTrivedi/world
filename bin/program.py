import random
from time import sleep
import sys
import subprocess

#My classes
from rabbit import Rabbit
from world import World
from wolf import Wolf

def place(world,animals):
    '''
    Place animals on world
    '''
    coords = list(world.get_spaces())

    for i in animals:
        val = random.randint(0, len(coords)-1)
        #This is causing issues, list out of index error due to more animals than map size?

        try:
            world.add_critter(x=coords[val][0], y=coords[val][1], crit=i)
        except Exception as e:
            print(e)
            print(val)
            print(len(animals))
        
        i.set_location(x=coords[val][0], y=coords[val][1])
        del coords[val]
    #return coords

def turn(animals, world):
    '''
    Play the game
    '''
    coords = []
    for obj in animals:
        #Check hunger first
        
        #This could be a lot shorter.
        (x,y) = obj.get_location()
        coords.append((x,y))
        #print(obj.get_hunger_incr())
        (x,y) = obj.move_animal(world=world,x=x,y=y)
        if (x,y) is not None:
            world.add_critter(x,y,obj)

        obj.set_location(x,y)
        coords.append((x,y))

    #subprocess.call(["pkill", "-f", "display /tmp/tmp"])
    return coords
    #img = world.generate(img,coords)

def main():
    '''
    Main function
    '''
    world = World(1000, 1920)

    #Place 100 rabbits
    rabbits = 10000
    rabbits = [Rabbit() for i in range(rabbits)]
    place(world, rabbits)

    #Generate 100 wolves
    wolves = 300
    wolves = [Wolf() for i in range(wolves)]
    place(world, wolves)

    img = world.generate(img=None, coords=None)

    counter = 1
    while counter < 1000:
        coords = []
        #coords = turn(rabbits, world)
        coords += turn(wolves, world)

        img = world.generate(img,set(coords))
        counter +=1

if __name__=="__main__":
    main()
