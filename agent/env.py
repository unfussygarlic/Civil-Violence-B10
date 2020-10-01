import sys
import random
import statistics as s
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from .people import Citizen
from .authority import Cop
from .params import reduction_factor

def get_poor_confidence(model):
    confidence = [a.confidence for a in model.schedule.agents if a.status == "Poor"]
    if confidence:
        mean = s.mean(confidence)
        return mean
    else:
        return 0

def get_middle_confidence(model):
    confidence = [a.confidence for a in model.schedule.agents if a.status == "Middle"]
    if confidence:
        mean = s.mean(confidence)
        return mean
    else:
        return 0

def get_rich_confidence(model):
    confidence = [a.confidence for a in model.schedule.agents if a.status == "Rich"]
    if confidence:
        mean = s.mean(confidence)
        return mean
    else:
        return 0

class World(Model):

    def __init__(self, 
                gridsize, 
                cop_density, 
                citizen_density, 
                agent_type, 
                c_state, 
                d_state, 
                e_state, 
                reduction_constant):

        self.cop_density = cop_density
        self.citizen_density = citizen_density
        self.agent_type = agent_type

        self.c_state = c_state
        self.d_state = d_state
        self.e_state = e_state

        self.corruption = 0.0
        self.democracy = 1.0
        self.employment = 1.0

        self.reduction_constant = reduction_constant

        self.rich_count = 0
        self.middle_count = 0
        self.poor_count = 0

        self.mean = 0
        self.grid = MultiGrid(gridsize,gridsize,True)
        self.schedule = SimultaneousActivation(self)
        self.placement(gridsize)
        self.running = True

        
    def placement(self,gridsize):

        unique_id = 0

        if self.cop_density + self.citizen_density > 1:
            print("Density ratios must not exceed 1", file=sys.stderr)
        
        for (_,x,y) in self.grid.coord_iter():

            if self.random.random() < self.cop_density:
                a = Cop(unique_id,self)
                self.schedule.add(a)
                self.grid.place_agent(a,(x,y))
                unique_id += 1

            elif self.random.random() < (self.cop_density + self.citizen_density):
                a = Citizen(unique_id, self, self.agent_type)
                self.schedule.add(a)
                self.grid.place_agent(a,(x,y))
                unique_id += 1
                
        self.datacollector = DataCollector(
            model_reporters={"Poor": get_poor_confidence,
                            "Middle": get_middle_confidence,
                            "Rich": get_rich_confidence})
    
    def update_agent_count(self):
        self.rich_count = len([a for a in self.schedule.agents if a.status == "Rich"])
        self.middle_count = len([a for a in self.schedule.agents if a.status == "Middle"])
        self.poor_count = len([a for a in self.schedule.agents if a.status == "Poor"])
    
    def update_core(self):
        if self.c_state:
            if self.corruption < 1.0:
                self.corruption += self.reduction_constant
            else:
                self.corruption = 1.0
        if self.d_state:
            if self.democracy > 0.0:
                self.democracy -= self.reduction_constant
            else:
                self.democracy = 0.0
        if self.e_state:
            if self.employment > 0.0:
                self.employment -= self.reduction_constant
            else:
                self.employment = 0.0
    
    def mean_wealth(self):
        self.agents = [agent.wealth for agent in self.schedule.agents if agent.alignment == "Citizen"]
        self.mean = s.mean(self.agents)

    def step(self):
        self.update_agent_count()
        self.datacollector.collect(self)
        self.mean_wealth()
        self.schedule.step()
        self.update_core()