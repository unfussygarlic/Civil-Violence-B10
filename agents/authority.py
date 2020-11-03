from mesa import Agent
import sys
from utils.params import kill_threshold, cop_threshold, r_c


class Bank(Agent):
    """
    A central authority agent whose task is to update it's reserves
    depending on the saving of the agents and decide the amount to
    loan.
    Attributes:
        unique_id: Every agent has a unique id allowing them to perform individual tasks
        model: World model
    """

    def __init__(self, unique_id, model):
        # initialize the parent class with required parameters
        super().__init__(unique_id, model)
        # for tracking total value of loans outstanding
        self.bank_loans = 0
        """percent of deposits the bank must keep in reserves - this is a
           UserSettableParameter in server.py"""
        self.giveaway = 0
        # for tracking total value of deposits
        self.deposits = 0
        # amount the bank is currently able to loan
        self.bank_to_loan = 0

    """update the bank's reserves and amount it can loan;
       this is called every time a person balances their books
       see below for Person.balance_books()"""

    def bank_balance(self):
        # amount the bank willing to loan
        self.giveaway = self.model.legitimacy * self.deposits
        self.bank_to_loan = self.deposits - (self.giveaway + self.bank_loans)


class Cop(Agent):

    """
    A central authority agent whose task to capture or eliminate revolting citizen.
    Rule: Eliminate citizen if it is revolting and has been jailed a set number of
    times before, else jail the citizen for set amount of time and increase the
    jailed counter.

    Attributes:
        unique_id: unique int indentifier of the agent
        model: model instance under which the agent is running
    """

    def __init__(self, unique_id, model):

        #  Initialize the Cop agent with a unique_id and the model instance

        super().__init__(unique_id, model)
        self.alignment = "Cop"

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

        self.revolt_citizens = [a for a in self.citizens if a.state == "Revolt"]

    def jail_citizen(self):

        # Jail or eliminate the citizen based on the number of times a citizen
        # has been jailed before

        for i in self.citizens:
            if i.n_j > kill_threshold:
                self.model.kill_agents.append(i)
                self.model.agents_killed += 1
            # elif i.state == "Revolt" and self.random.random() > 0.2:
            #     i.state = "Jail"
            #     i.movement = False
        if self.random.random() > self.model.legitimacy:
            if self.revolt_citizens:
                r_c = self.random.choice(self.revolt_citizens)
                r_c.state = "Jail"
                r_c.movement = False

    def step(self):
        """
        A single step(or tick) in the model and the calucations that should be done.
        In a single step the cop agent should know its neighbor, move to a new
        position and jail revolitng citizen(if found)
        """
        self.get_neighbors()
        self.move()
        self.jail_citizen()
