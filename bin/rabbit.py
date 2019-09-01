import random
import names
import sys

from animal import Animal

class Rabbit(Animal):
    '''
    Create a rabbit animal.
    '''
    def __init__(self, gender=bool(random.getrandbits(1))):
        '''
        Create rabbit object
        '''
        self.sight          = random.randint(2,5)
        self.hunger_incr    = random.randint(1,3)
        self.total_hunger   = random.randint(80,120)
        self.age            = random.randint(1,12)
        self.animal         = "rabbit"

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

        #If rabbit doest move, means it has eaten.
        #if feature == "grass":
        #    #self.hunger(self.get_hunger_incr()*-1,map)
        #    #hunger meter check if rabbit dies.
        #    if (new_x, new_y) == (x, y):
        #        food = self.hunger_incr
        #    else:
        #        food = 1
        #    if not self.set_hunger(food):
        #        #print(self.total_hunger)
        #        return False
        #    else:
        #        #print("Placed..")
        #        self.set_location(new_x, new_y)
        #        map.add_critter(new_x, new_y, self)
        #        return True

def main():
    '''
    Main function
    '''
    rabbit = Rabbit("male")
    #rabbit.hunger(hunger_incr = rabbit.get_hunger_incr(map))
    rabbit.set_hunger(hunger_incr = 1)

if __name__=="__main__":
    main()