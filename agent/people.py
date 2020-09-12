import numpy as np
from mesa import Agent

class Citizen(Agent):

    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        cat = ["Rich","Middle","Poor"]
        self.status = np.random.choice(cat,p = [0.33,0.33,0.34])

    def step(self):
        # print('Hello I am agent {}'.format(self.unique_id))
        pass