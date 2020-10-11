import sys
import random
import statistics as s
from mesa import Model
from mesa.space import Grid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from .people import Citizen
from .authority import Cop
from .params import reduction_factor


def get_poor_confidence(model):
    confidence = [
        a.confidence
        for a in model.schedule.agents
        if a.alignment == "Citizen" and a.status == "Poor"
    ]
    if confidence:
        mean = s.mean(confidence)
        return mean
    else:
        return 0


def get_middle_confidence(model):
    confidence = [
        a.confidence
        for a in model.schedule.agents
        if a.alignment == "Citizen" and a.status == "Middle"
    ]
    if confidence:
        mean = s.mean(confidence)
        return mean
    else:
        return 0


def get_rich_confidence(model):
    confidence = [
        a.confidence
        for a in model.schedule.agents
        if a.alignment == "Citizen" and a.status == "Rich"
    ]
    if confidence:
        mean = s.mean(confidence)
        return mean
    else:
        return 0

def get_cop_confidence(model):
    confidence = [
        a.confidence
        for a in model.schedule.agents
        if a.alignment == "Cop" and a.status == "Neutral"
    ]
    if confidence:
        mean = s.mean(confidence)
        return mean
    else:
        return 0



class World(Model):
    def __init__(
        self,
        gridsize,
        cop_density,
        citizen_density,
        agent_type,
        c_state,
        d_state,
        e_state,
        n_state,
        reduction_constant,
    ):

        self.cop_density = cop_density
        self.citizen_density = citizen_density
        self.agent_type = agent_type

        self.c_state = c_state
        self.d_state = d_state
        self.e_state = e_state
        self.n_state = n_state

        self.corruption = 0.0
        self.democracy = 1.0
        self.employment = 1.0
        self.negotiation = 0.3
        self.reduction_constant = reduction_constant

        # Agent count r_c: rich_count, r_a_c: rich_active_count ...
        self.r_c = 0
        self.r_a_c = 0
        self.m_c = 0
        self.m_a_c = 0
        self.p_c = 0
        self.p_a_c = 0
        self.c_c = 0
        self.c_a_c = 0
        self.mean = 0
        self.kill_agents = []
        self.grid = Grid(gridsize, gridsize, False)
        self.schedule = SimultaneousActivation(self)
        self.placement(gridsize)
        self.running = True

    def placement(self, gridsize):
        """
        Placement of agents inside the Grid
        Arguments:
        gridsize: Dimensions of grid
        """
        unique_id = 0

        if self.cop_density + self.citizen_density > 1:
            print("Density ratios must not exceed 1", file=sys.stderr)

        for (_, x, y) in self.grid.coord_iter():

            if self.random.random() < self.cop_density:
                a = Cop(unique_id, self)
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))
                unique_id += 1

            elif self.random.random() < (self.cop_density + self.citizen_density):
                a = Citizen(unique_id, self, self.agent_type)
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))
                unique_id += 1

        self.datacollector = DataCollector(
            model_reporters={
                "Poor": get_poor_confidence,
                "Middle": get_middle_confidence,
                "Rich": get_rich_confidence,
                "Cop" : get_cop_confidence,
            }
        )

    def update_agent_count(self):
        """
        Updates the number of current and active agents
        """
        self.r_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen" and a.status == "Rich"
            ]
        )
        self.r_a_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen"
                and a.status == "Rich"
                and a.state == "Revolt"
            ]
        )

        self.m_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen" and a.status == "Middle"
            ]
        )
        self.m_a_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen"
                and a.status == "Middle"
                and a.state == "Revolt"
            ]
        )

        self.p_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen" and a.status == "Poor"
            ]
        )
        self.p_a_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen"
                and a.status == "Poor"
                and a.state == "Revolt"
            ]
        )
        self.c_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Cop" and a.status == "Neutral"
            ]
        )
        self.c_a_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Cop"
                and a.status == "Neutral"
                and a.state == "Calm"
            ]
        )

    def update_core(self):
        """
        Updated the core paramenters
        (corruption, democracy and employment)
        using reduction_constant.
        """
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
        
        if self.n_state:
            if self.negotiation > 0.2:
                self.negotiation -= (self.reduction_constant)*10
            else:
                self.negotiation = 0.2

    # def negotiation(self):
    #     if self.

    def mean_wealth(self):
        self.agents = [
            agent.wealth
            for agent in self.schedule.agents
            if agent.alignment == "Citizen"
        ]
        self.mean = s.mean(self.agents)

    def step(self):
        self.update_agent_count()
        self.datacollector.collect(self)
        self.mean_wealth()
        self.schedule.step()
        self.update_core()
        

        # Code from stackoverflow. Stuart Ball'answered in
        # https://stackoverflow.com/questions/62821720/deleting-agent-in-mesa
        if self.kill_agents:
            self.kill_agents = list(dict.fromkeys(self.kill_agents))
            for i in self.kill_agents:
                self.grid.remove_agent(i)
                self.schedule.remove(i)
            self.kill_agents = []

        total_agents = self.r_c + self.m_c + self.p_c + self.c_c
        if total_agents < 3:
            self.running = False
