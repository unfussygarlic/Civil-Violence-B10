import numpy as np
from mesa import Agent
from .authority import Cop
from .params import k_c, k_d, k_e, k_p, k_af, wealth_inc, timestep

class Citizen(Agent):

    def __init__(self, unique_id, model, agent_type, corruption, democracy, employment):
        super().__init__(unique_id,model)
        self.corruption = corruption
        self.democracy = democracy
        self.employment = employment
        self.alignment = "Citizen"
        cat = ["Rich","Middle","Poor"]
        self.status = np.random.choice(cat,p = [0.33,0.33,0.34])
        # self.status = agent_type
        self.wealth = 1
        self.grievance = 0.0
        self.t = 0
        self.confidence = 0.0

    def step(self):
        if self.t % timestep == 0:
            self.update_wealth()
        self.get_neighbors()
        self.measure_confidence()
        self.move()
    
    def update_wealth(self):
        choice = np.random.choice(wealth_inc[self.status])
        self.wealth += choice
    
    def move(self):
        if self.empty_cells:
            pos = self.random.choice(self.empty_cells)
            self.model.grid.move_agent(self,pos)
    
    def get_neighbors(self):
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, radius = 1)
        self.empty_cells = [c for c in neighborhood if self.model.grid.is_cell_empty(c)]
        neighbors = self.model.grid.get_neighbors(self.pos, True)
        self.citizens = []
        self.cops = []
        if neighbors:
            for neighbor in neighbors:
                if type(neighbor) == Citizen:
                    self.citizens.append(neighbor)
                elif type(neighbor) == Cop:
                    self.cops.append(neighbor)

    def measure_confidence(self):
        p_r = k_p * np.exp(-(self.wealth / self.model.mean))
        c_r = k_c[self.status] * self.corruption
        d_r = k_d[self.status] * (1 - self.democracy)
        e_r = k_e[self.status] * (1 - self.employment)
        self.grievance = 1 - np.exp(-(c_r + d_r + e_r + p_r))

        n_g = (len(self.citizens) * sum([a.grievance for a in self.citizens]))+ 0.01
        n_c = len(self.cops) * 1.0
        self.risk_factor = k_af * np.exp(-(n_c / n_g))

        if self.cops:
            self.confidence = self.grievance * self.risk_factor
        else:
            self.confidence = self.grievance

        print(f"{self.status} :: {self.wealth} :: {p_r} :: {self.grievance} :: {self.risk_factor} :: {self.confidence} :: {len(self.cops)} :: {len(self.citizens)}")