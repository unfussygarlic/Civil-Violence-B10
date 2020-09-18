import numpy as np
from mesa import Agent
from .params import k_c, k_d, k_e, k_p, wealth_inc, timestep

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

    def step(self):
        if self.t % timestep == 0:
            self.update_wealth()
        self.measure_grievance()
        self.get_neighbors()
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
    
    def measure_grievance(self):
        p_r = k_p * np.exp(-(self.wealth / self.model.mean))
        c_r = k_c[self.status] * self.corruption
        d_r = k_d[self.status] * (1 - self.democracy)
        e_r = k_e[self.status] * (1 - self.employment)
        self.grievance = 1 - np.exp(-(c_r + d_r + e_r + p_r))
        print(f"wealth : {self.wealth} :: p_rate : {p_r} :: grievance : {self.grievance} :: {self.corruption} :: {self.democracy} :: {self.employment}")