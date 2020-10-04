from mesa import Agent
from .params import kill_threshold, cop_threshold, confidence_threshold, r_c

# TODO: 
# Changing behaviour based on core parameters
# 

class Cop(Agent):
    """
    A central authority agent whose task to capture or eliminate revolting citizen.
    Rule: Eliminate citizen if it is revolting and has been jailed a set number of 
    times before, else jail the citizen for set amount of time and increase the 
    jailed counter.
    
    Attributes:
        unique_id: unique int indentifier of the agent
        model: model instance under which the agent is running
        alignment: tell the alignment of agent(whether Cop or Citizen)
        empty_cells: empty locations around the agent
        neighborhood: the status of other agents around the agent in consideration
        neighbors: the neighboring agents
        citizens: list of citizen around the agent
        cops: list of cops around the agent
        kill_threshold: the number of times a citizen can be jailed before being 
            eliminated by Cop
    """
    def __init__(self, unique_id, model):
        """
        Initialize the Cop agent with a unique_id and the model instance
        """
        super().__init__(unique_id, model)
        self.alignment = "Cop"

    def step(self):
        """
        A single step(or tick) in the model and the calucations that should be done.
        In a single step the cop agent should know its neighbor, move to a new 
        position and jail revolitng citizen(if found) 
        """
        self.get_neighbors()
        self.move()
        self.jail_citizen()

    def move(self):
        """
        Move the agent to a new empty position on the grid
        """
        if self.empty_cells:
            pos = self.random.choice(self.empty_cells)
            self.model.grid.move_agent(self, pos)

    def get_neighbors(self):
        """
        Find the neighbor(s) around the Cop agent and categorize into two either
        citizen or cops
        """
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
        """
        Jail or eliminate the citizen based on the number of times a citizen 
        has been jailed.
        """
        for i in self.citizens:
            if i.n_j > kill_threshold:
                self.model.kill_agents.append(i)
            elif i.state == "Revolt" and self.random.random() > 0.2:
                i.state = "Jail"
                i.movement = False
