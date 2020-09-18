from mesa import Agent

class Cop(Agent):

    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        self.alignment = "Cop"
    
    def step(self):
        pass