import random
import math

class Map3:
    def __init__(self,x,y):
        self.map = [[0 for i in range(x)] for j in range(y)]

        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                z = (math.sin(x*0.5) - math.sin(y*0.5))

                terr = {}
                terr["water"] = z < -1.5
                terr["mountain"] = z > 1.5
                terr["critter"] = None

                self.map[x][y] = terr

    def generate(self):
        #print(self.map[0][0])
        str1 = ""
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y]['water']:
                    str1 += "W"
                elif self.map[x][y]['mountain']:
                    str1 += "M"
                elif self.map[x][y]['critter']:
                    str1 += self.map[x][y]['critter'].get_animal()[0]
                else:
                    str1 += " "
            str1 = str1[:-1]
            str1 += "\n"
        print(str1)

    def get_spaces(self):
        coords = []
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if not self.map[x][y]["water"] and not self.map[x][y]["mountain"] and self.map[x][y]["critter"] is None:
                    coords.append((x,y))
        return coords

    def add_critter(self,x,y,crit):
        self.map[x][y]["critter"] = crit
    
    def remove_critter(self,x,y):
        self.map[x][y]["critter"] = None

    def get_critter(self,x,y,crit):
        return self.map[x][y]["critter"]

def decision(probability):
    return random.random() < probability

def main():
    map = Map3(190,17)
    map.generate()

if __name__=="__main__":
    main()