import random
import names
import sys

from animal import Animal

class Wolf(Animal):
    def __init__(self, gender=bool(random.getrandbits(1))):
        '''
        Create wolf object
        '''
        self.sight          = random.randint(2,5)
        self.hunger_incr    = random.randint(1,3)
        self.total_hunger   = random.randint(80,120)
        self.age            = random.randint(1,12)
        self.animal         = "wolf"

        if gender:
            self.gender = "male"
            self.name   = names.get_first_name(gender='male')
        else:
            self.gender = "female"
            self.name   = names.get_first_name(gender='female')
        
    def move_animal(self, world, x, y):
        world.remove_critter(x, y)
        #data = self.check_surroundings(x,y,coords)
        #Check surroundings. Move away from wolves, move towards rabbit, water or pause to eat.

        #For not get 1 tile next to you.
        coords = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if 0 <= i < world.shape[0] and 0 <= j < world.shape[1]:
                    (feature, animal) = world.get_feature(i, j)
                    if feature in ("grass", "sand") and not animal:
                        coords.append((i, j))
        
        if coords:
            (new_x, new_y) = random.choice(coords)
            return (new_x, new_y)

def main():
    Wolf()

if __name__=="__main__":
    main()