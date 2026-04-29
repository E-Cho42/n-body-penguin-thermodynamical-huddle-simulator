# penguin class file
import random as rd
class Penguin:
    def __init__(self, heat, location, velocity, t):
        self.heat = heat
        self.location = list(location)
        self.velocity = list(velocity)
        self.t = t
        self.dircetion = rd.randint(0,1)
        if self.dircetion == 0:
            self.dircetion = -1
            
    
    