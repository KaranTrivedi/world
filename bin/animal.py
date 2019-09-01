import random

from rabbit import Rabbit

class Animal(object):

    def __init__(self):
        pass

    def get_name(self):
        '''
        Get name of critter.
        '''
        return self.name
    
    def get_gender(self):
        '''
        Get gender of critter
        '''
        return self.gender
    
    def set_location(self, x, y):
        '''
        define location of animal.
        '''
        self.x = x
        self.y = y

    def get_hunger_incr(self):
        '''
        Get hunger increase value.
        '''
        return self.hunger_incr

    def get_hunger(self):
        return self.total_hunger

    def set_hunger(self, food):
        '''
        Set hunger level.
        '''
        self.total_hunger = self.total_hunger + food - self.hunger_incr
        #print("set_hunger: %s, food: %s, hunger_incr: %s" %  (self.total_hunger, food, self.hunger_incr))
        if self.total_hunger <= 0:
            return False
        else:
            return True

    def get_location(self):
        return (self.x,self.y)

    def get_animal(self):
        return self.animal

    def get_sight(self):
        return self.sight

    def check_surroundings(self,x,y,coords):
        range = self.get_sight()
        filtered = [a for a in coords if a[0]-range < x < a[0]+range]
        filtered = [a for a in filtered if a[1]-range < y < a[1]+range]

        return filtered
    
    def get_age(self):
        return self.age
    
    def set_age(self,age):
        self.age = age