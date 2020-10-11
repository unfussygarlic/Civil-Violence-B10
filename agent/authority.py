import numpy as np
from mesa import Agent
from .params import kill_threshold, cop_threshold, confidence_threshold, jail_period
from .params import k_c, k_d, k_e, k_p, k_af

class Cop(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alignment = "Cop"
        self.status = "Neutral"
        self.state = "Calm"
        self.confidence = 0
        self.angry_time = 0
        self.n_cop = 0
        self.movement = True
        

    def step(self):
        self.get_neighbors()
        self.jail_citizen()
        self.measure_cop_confidence()
        self.update_angry_time()
        self.update_cop_state()

        if self.movement:
            self.move()


    def update_angry_time(self):
        if self.state == "Angry":
            self.angry_time += 1
            if self.angry_time > jail_period:
                self.update_cop_state()
                self.angry_time = 0
                self.n_cop += 1
        else:
            pass

    def update_cop_state(self):
        if self.confidence < cop_threshold:
            self.state = "Angry"
        else:
            self.state = "Calm"        

    def move(self):
        if self.empty_cells:
            pos = self.random.choice(self.empty_cells)
            self.model.grid.move_agent(self, pos)

    def get_neighbors(self):
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, radius=1)
        self.empty_cells = [c for c in neighborhood if self.model.grid.is_cell_empty(c)]
        neighbors = self.model.grid.get_neighbors(self.pos, True)
        self.citizens = []
        self.cops = []
        if neighbors:
            for neighbor in neighbors:
                if neighbor.alignment == "Citizen":
                    self.citizens.append(neighbor)
                elif neighbor.alignment == "Cop":
                    self.cops.append(neighbor)

    def jail_citizen(self):
        for i in self.citizens:
            if (i.n_j +self.model.negotiation) > kill_threshold:             #to avoid the death of citizens
                self.model.kill_agents.append(i)
            elif i.state == "Revolt":
                i.state = "Jail"
                i.movement = False

    def measure_cop_confidence(self):
        
        # corruption, democracy and employment factors
        c_r = 0.33 * self.model.corruption
        d_r = 0.33 * (1 - self.model.democracy)
        e_r = 0.33 * (1 - self.model.employment)

        self.grievance = 1 - np.exp(-(c_r + d_r + e_r))

        n_g = (len(self.citizens) * sum([a.grievance for a in self.citizens])) + 0.01
        n_c = len(self.cops) * 1.0
        self.risk_factor = k_af * np.exp(-(n_c / n_g))

        if self.cops:
            self.confidence = 1-(self.grievance * self.risk_factor)

        elif self.citizens:
            self.confidence = self.grievance * self.risk_factor
       
    # def negotiation(self):
