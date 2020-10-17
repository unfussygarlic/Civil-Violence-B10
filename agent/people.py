import numpy as np
import math
from mesa import Agent
from .business import Person
from .authority import Cop
from .params import k_c, k_d, k_e, k_p, k_af, r_c
from .params import wealth_inc, timestep
from .params import jail_period, citizen_vision

# An agent that emulates the behavior of a citizen, he can be a rich
# class citizen, middle class citizen or poor citizen.
# A citizen can go 3 states: Calm, Revolt, Jail
# It has the following attributes:
#     unique_id
#     model
#     agent_type = cop or citizen
#     wealth

class Citizen(Person):
    def __init__(self,
                unique_id,
                pos,
                model,
                hardship,
                risk_aversion,
                bank,
                rich_threshold):
        super().__init__(unique_id, pos, model, bank, rich_threshold)
        self.alignment = "Citizen"
        self.hardship = hardship
        self.risk_aversion = risk_aversion

        # Randomizing each class of the citizen

        # if self.model.include_wealth:
        #     cat = ["Rich", "Middle", "Poor"]
        #     self.status = np.random.choice(cat, p=[0.33, 0.33, 0.34])
        # else:
        #     self.status = "Rich"
        self.status = "None"

        # self.wealth = self.random.uniform(0,1)
        self.wealth = 1.0

        # State of the agent ["Calm", "Revolt", "Jail"]
        self.state = "Calm"
        self.movement = True

        self.grievance = 0.0
        self.t = 0
        self.confidence = 0.0
        self.net_risk = 0.0
        self.poverty = 0.0

        # Jail timestep and Total number of jailing
        self.j_time = 0
        self.n_j = 0

    # Decide whether the move is applicable
    def step(self):
        if self.movement:
            self.update_neighbors()
            self.update_state()
            self.random_move()
            self.kill_cops()
        self.update_jail_time()
        if self.model.include_wealth and self.state != "Jail":
            self.do_business()
            self.balance_books()
            self.bank.bank_balance()
            self.update_status()
        self.measure_confidence()

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
    
    def update_status(self):
        if self.savings > self.model.rich_threshold:
            self.status = "Rich"
        if self.savings < 10 and self.loans < 10:
            self.status = "Middle"
        if self.loans > 10:
            self.status = "Poor"

    # Updates each iteration to see if his state will change

    def update_state(self):
        if self.confidence > self.model.active_threshold and self.random.random() > r_c:
            self.state = "Revolt"
        else:
            self.state = "Calm"
            
    # def update_wealth(self):
    #     if self.random.random() > (1 - self.model.legitimacy):
    #         net_wealth = wealth_inc[self.status]
    #         self.wealth += net_wealth

    # Look around and see for neighbors

    def update_neighbors(self):
        self.neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, radius = citizen_vision)
        # self.empty_cells = [c for c in neighborhood if self.model.grid.is_cell_empty(c)]
        neighbors = self.model.grid.get_neighbors(self.pos, True)
        self.citizens = []
        self.cops = []
        if neighbors:
            for neighbor in neighbors:
                if neighbor.alignment == "Citizen":
                    self.citizens.append(neighbor)
                elif neighbor.alignment == "Cop":
                    self.cops.append(neighbor)
        
        self.revolt_citizens = [a for a in self.citizens if a.state == "Revolt"]
    
    def kill_cops(self):
        if self.state == "Revolt":
            citizens = len(self.revolt_citizens) + 1
            cops = len(self.cops)
            if cops:
                if (citizens - cops) >= (8 * citizen_vision)//2:
                    self.model.kill_agents.append(self.random.choice(self.cops))
    
    #movement of the agent

    def move(self):
        # if self.empty_cells:
        #     pos = self.random.choice(self.empty_cells)
        #     self.model.grid.move_agent(self, pos)
        pos = self.random.choice(self.neighborhood)
        self.model.grid.move_agent(self,pos)
    
    def sigmoid(self,x):
        return 1 / (1 + math.exp(-x))

    def measure_confidence(self):
        
        if self.model.include_wealth:
            try:
                self.hardship =  1- self.sigmoid(self.wealth/self.model.mean)            
            except ZeroDivisionError:
                self.hardship = 0

        self.grievance = self.hardship * (1 - self.model.legitimacy)
        alpha = (self.status == "Jail")

        n_g = len(self.revolt_citizens) + 1
        n_c = len(self.cops)
        self.arrest_probability = 1 - math.exp(-1 * self.model.ap_constant * (n_c / n_g))

        self.net_risk = self.arrest_probability * self.risk_aversion * (jail_period)**alpha

        if self.model.include_wealth:
            self.poverty = k_p * math.exp(-((self.savings + 0.0001) / (self.model.mean + 0.00001)))
            self.confidence = self.grievance - self.net_risk
        else:
            self.confidence = self.grievance - self.net_risk