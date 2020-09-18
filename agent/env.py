import sys
import random
import statistics as s
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from .people import Citizen
from .authority import Cop

class World(Model):

    def __init__(self, gridsize, cop_density, citizen_density, agent_type, corruption, democracy, employment):
        self.cop_density = cop_density
        self.citizen_density = citizen_density
        self.agent_type = agent_type
        self.corruption = corruption
        self.democracy = democracy
        self.employment = employment

        self.mean = 0
        self.grid = MultiGrid(gridsize,gridsize,True)
        self.scheduler = SimultaneousActivation(self)
        self.placement(gridsize)
        self.running = True

        
    def placement(self,gridsize):

        unique_id = 0

        if self.cop_density + self.citizen_density > 1:
            print("Density ratios must not exceed 1", file=sys.stderr)
        
        for (_,x,y) in self.grid.coord_iter():

            if self.random.random() < self.cop_density:
                a = Cop(unique_id,self)
                self.scheduler.add(a)
                self.grid.place_agent(a,(x,y))
                unique_id += 1

            elif self.random.random() < (self.cop_density + self.citizen_density):
                a = Citizen(unique_id, self, self.agent_type, self.corruption, self.democracy, self.employment)
                self.scheduler.add(a)
                self.grid.place_agent(a,(x,y))
                unique_id += 1
                
        self.agents = [agent.wealth for agent in self.scheduler.agents if agent.alignment == "Citizen"]
    
    def mean_wealth(self):
        self.agents = [agent.wealth for agent in self.scheduler.agents if agent.alignment == "Citizen"]
        self.mean = s.mean(self.agents)

    def step(self):
        self.mean_wealth()
        self.scheduler.step()