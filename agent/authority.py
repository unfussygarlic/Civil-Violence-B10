from mesa import Agent
from .params import kill_threshold, cop_threshold, confidence_threshold


class Cop(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alignment = "Cop"

    def step(self):
        self.get_neighbors()
        self.move()
        self.jail_citizen()

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
            if i.n_j > kill_threshold:
                self.model.kill_agents.append(i)
            elif i.state == "Revolt":
                i.state = "Jail"
                i.movement = False
