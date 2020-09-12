import sys
import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from .people import Citizen
from .authority import Cop

class World(Model):

    def __init__(self, gridsize, cop_density):
        self.cop_density = cop_density
        self.citizen_density = 1 - self.cop_density
        self.grid = MultiGrid(gridsize,gridsize,True)
        self.scheduler = RandomActivation(self)
        self.placement(gridsize)
        self.running = True

        
    def placement(self,gridsize):

        unique_id = 0

        if self.cop_density + self.citizen_density > 1:
            print("Density ratios must not exceed 1", file=sys.stderr)
        
        for (_,x,y) in self.grid.coord_iter():

            if random.random() < self.cop_density:
                a = Cop(unique_id,self)
                self.scheduler.add(a)
                self.grid.place_agent(a,(x,y))
                unique_id += 1

            else:
                a = Citizen(unique_id,self)
                self.scheduler.add(a)
                self.grid.place_agent(a,(x,y))
                unique_id += 1
    
    def step(self):
        self.scheduler.step()