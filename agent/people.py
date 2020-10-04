import numpy as np
from mesa import Agent
from .authority import Cop
from .params import k_c, k_d, k_e, k_p, k_af, r_c
from .params import wealth_inc, timestep, confidence_threshold
from .params import jail_period

# An agent that emulates the behavior of a citizen, he can be a rich
# class citizen, middle class citizen or poor citizen.
# A citizen can go 3 states: Calm, Revolt, Jail
# It has the following attributes:
#     unique_id
#     model
#     agent_type = cop or citizen
#     wealth


class Citizen(Agent):
    def __init__(self, unique_id, model, agent_type):
        super().__init__(unique_id, model)
        self.alignment = "Citizen"

        # Randomizing each class of the citizen

        cat = ["Rich", "Middle", "Poor"]
        self.status = np.random.choice(cat, p=[0.33, 0.33, 0.34])

        # self.wealth = self.random.uniform(0,1)
        self.wealth = 1.0

        # State of the agent ["Calm", "Revolt", "Jail"]
        self.state = "Calm"
        self.movement = True

        self.grievance = 0.0
        self.t = 0
        self.confidence = 0.0

        # Jail timestep and Total number of jailing
        self.j_time = 0
        self.n_j = 0

    # Decide whether the move is applicable
    def step(self):
        self.update_jail_time()
        self.update_wealth()
        self.update_neighbors()
        self.measure_confidence()
        if self.movement:
            self.update_state()
            self.move()

    def update_jail_time(self):
        if self.state == "Jail":
            self.j_time += 1
            if self.j_time > jail_period:
                self.movement = True
                self.update_state()
                self.j_time = 0
                self.n_j += 1
        else:
            pass

    # Updates each iteration to see if his state will change

    def update_state(self):
        if self.confidence > confidence_threshold and self.random.random() > r_c:
            self.state = "Revolt"
        else:
            self.state = "Calm"
            
    def update_wealth(self):
        net_wealth = wealth_inc[self.status] * (1 - self.model.corruption + 0.1)
        self.wealth += net_wealth

    # Look around and see for neighbors

    def update_neighbors(self):
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
    
    def kill_cops(self):
        # TODO
        pass
    
    #movement of the agent

    def move(self):
        if self.empty_cells:
            pos = self.random.choice(self.empty_cells)
            self.model.grid.move_agent(self, pos)

    def measure_confidence(self):
        p_r = k_p * np.exp(-(self.wealth / self.model.mean))

        # corruption, democracy and employment factors
        c_r = k_c[self.status] * self.model.corruption
        d_r = k_d[self.status] * (1 - self.model.democracy)
        e_r = k_e[self.status] * (1 - self.model.employment)

        self.grievance = 1 - np.exp(-(c_r + d_r + e_r + p_r))

        n_g = (len(self.citizens) * sum([a.grievance for a in self.citizens])) + 0.01
        n_c = len(self.cops) * 1.0
        self.risk_factor = k_af * np.exp(-(n_c / n_g))

        if self.cops:
            self.confidence = self.grievance * self.risk_factor
        else:
            self.confidence = self.grievance
