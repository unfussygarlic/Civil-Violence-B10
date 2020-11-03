import numpy as np
import math
from mesa import Agent
from utils.params import k_c, k_d, k_e, k_p, k_af, r_c
from utils.params import wealth_inc, timestep
from utils.params import jail_period, citizen_vision


class Citizen(Agent):
    """
    An agent that emulates the behavior of a citizen, he can be a rich
    class citizen, middle class citizen or poor citizen.
    A citizen can go 3 states: Calm, Revolt, Jail
    Attributes:
        unique_id: Every agent has a unique id allowing them to perform individual tasks
        model: World model
        hardship: Hardship value of a single agent
        risk_aversion: Varying aversion constant of a single agent
        bank: Bank agent
        rich_threshold: Thresold constant for status separation
    """

    def __init__(self, unique_id, model, hardship, risk_aversion, bank, rich_threshold):

        super().__init__(unique_id, model)
        # Indicating whether the agent is citizen or cop
        self.alignment = "Citizen"

        # Set initial status of the agent
        self.status = "None"

        # State of the agent ["Calm", "Revolt", "Jail"]
        self.state = "Calm"
        self.movement = True

        self.grievance = 0.0
        self.confidence = 0.0
        self.net_risk = 0.0
        self.hardship = hardship
        self.risk_aversion = risk_aversion

        # Jail timestep and Total number of jailing
        self.j_time = 0
        self.n_j = 0
        self.t = 0

        # the amount each person has in savings
        self.savings = 0
        # total loan amount person has outstanding
        self.loans = 0
        """start everyone off with a random amount in their wallet from 1 to a
           user settable rich threshold amount"""
        self.wallet = self.random.randint(1, rich_threshold + 1)
        # savings minus loans, see balance_books() below
        self.wealth = 0
        # person to trade with, see do_business() below
        self.customer = 0
        # person's bank, set at __init__, all people have the same bank in this model
        self.bank = bank

    def do_business(self):
        """check if person has any savings, any money in wallet, or if the
        bank can loan them any money"""
        if self.savings > 0 or self.wallet > 0 or self.bank.bank_to_loan > 0:
            # create list of people at my location (includes self)
            my_cell = self.model.grid.get_cell_list_contents([self.pos])
            my_cell = [a for a in my_cell if a.alignment == "Citizen"]
            # check if other people are at my location
            if len(my_cell) > 1:
                # set customer to self for while loop condition
                customer = self
                while customer == self:
                    """select a random person from the people at my location
                    to trade with"""
                    customer = self.random.choice(my_cell)
                # 50% chance of trading with customer
                if self.random.randint(0, 1) == 0:
                    # 50% chance of trading $5
                    if self.random.randint(0, 1) == 0:
                        # give customer $5 from my wallet (may result in negative wallet)
                        customer.wallet += 5
                        self.wallet -= 5
                    # 50% chance of trading $2
                    else:
                        # give customer $2 from my wallet (may result in negative wallet)
                        customer.wallet += 2
                        self.wallet -= 2

    def balance_books(self):
        # check if wallet is negative from trading with customer
        if self.wallet < 0:
            # if negative money in wallet, check if my savings can cover the balance
            if self.savings >= (self.wallet * -1):
                """if my savings can cover the balance, withdraw enough
                money from my savings so that my wallet has a 0 balance"""
                self.withdraw_from_savings(self.wallet * -1)
            # if my savings cannot cover the negative balance of my wallet
            else:
                # check if i have any savings
                if self.savings > 0:
                    """if i have savings, withdraw all of it to reduce my
                    negative balance in my wallet"""
                    self.withdraw_from_savings(self.savings)
                # record how much money the bank can loan out right now
                temp_loan = self.bank.bank_to_loan
                """check if the bank can loan enough money to cover the
                   remaining negative balance in my wallet"""
                if temp_loan >= (self.wallet * -1):
                    """if the bank can loan me enough money to cover
                    the remaining negative balance in my wallet, take out a
                    loan for the remaining negative balance"""
                    self.take_out_loan(self.wallet * -1)
                else:
                    """if the bank cannot loan enough money to cover the negative
                    balance of my wallet, then take out a loan for the
                    total amount the bank can loan right now"""
                    self.take_out_loan(temp_loan)
        else:
            """if i have money in my wallet from trading with customer, deposit
            it to my savings in the bank"""
            self.deposit_to_savings(self.wallet)
        # check if i have any outstanding loans, and if i have savings
        if self.loans > 0 and self.savings > 0:
            # check if my savings can cover my outstanding loans
            if self.savings >= self.loans:
                # payoff my loans with my savings
                self.withdraw_from_savings(self.loans)
                self.repay_a_loan(self.loans)
            # if my savings won't cover my loans
            else:
                # pay off part of my loans with my savings
                self.withdraw_from_savings(self.savings)
                self.repay_a_loan(self.wallet)
        # calculate my wealth
        self.wealth = self.savings * self.model.legitimacy - self.loans
        if self.wealth == 0.0:
            self.wealth += 1

    # part of balance_books()
    def deposit_to_savings(self, amount):
        # take money from my wallet and put it in savings
        self.wallet -= amount
        self.savings += amount
        # increase bank deposits
        self.bank.deposits += amount

    # part of balance_books()
    def withdraw_from_savings(self, amount):
        # put money in my wallet from savings
        self.wallet += amount
        self.savings -= amount
        # decrease bank deposits
        self.bank.deposits -= amount

    # part of balance_books()
    def repay_a_loan(self, amount):
        # take money from my wallet to pay off all or part of a loan
        self.loans -= amount
        self.wallet -= amount
        # increase the amount the bank can loan right now
        self.bank.bank_to_loan += amount
        # decrease the bank's outstanding loans
        self.bank.bank_loans -= amount

    # part of balance_books()
    def take_out_loan(self, amount):
        """borrow from the bank to put money in my wallet, and increase my
        outstanding loans"""
        self.loans += amount
        self.wallet += amount
        # decresae the amount the bank can loan right now
        self.bank.bank_to_loan -= amount
        # increase the bank's outstanding loans
        self.bank.bank_loans += amount

    def update_jail_time(self):
        """
        Updates the jail time and resets
        it once it crosses the threshold.
        """
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
        """
        Updates the status of the agent
        based on the rich_threshold
        """
        if self.savings > self.model.rich_threshold:
            self.status = "Rich"
        if self.savings < 10 and self.loans < 10:
            self.status = "Middle"
        if self.loans > 10:
            self.status = "Poor"

    def update_state(self):
        """
        Updates the state of the agent
        based on the threshold
        """
        if self.confidence > self.model.active_threshold and self.random.random() > r_c:
            self.state = "Revolt"
        else:
            self.state = "Calm"

    def update_neighbors(self):
        """
        Checks the neighborhood based on the
        agents radius and separates them
        based on their alignment and state.
        """
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=citizen_vision
        )
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
        """
        Function for eliminating the cops
        from the grid based on the given
        condition.
        """
        if self.state == "Revolt":
            citizens = len(self.revolt_citizens) + 1
            cops = len(self.cops)
            if cops:
                if (citizens - cops) >= (8 * citizen_vision) // 2:
                    self.model.kill_agents.append(self.random.choice(self.cops))

    def sigmoid(self, x):
        """
        Sigmoid function to crunch
        the numbers between 0-1.
        """
        return 1 / (1 + math.exp(-x))

    def measure_confidence(self):

        if self.model.include_wealth:
            try:
                self.hardship = 1 - self.sigmoid(self.wealth / self.model.mean)
            except ZeroDivisionError:
                self.hardship = 0

        self.grievance = self.hardship * (1 - self.model.legitimacy)
        alpha = self.status == "Jail"

        n_g = len(self.revolt_citizens) + 1
        n_c = len(self.cops)
        self.arrest_probability = 1 - math.exp(
            -1 * self.model.ap_constant * (n_c / n_g)
        )
        self.net_risk = (
            self.arrest_probability * self.risk_aversion * (jail_period) ** alpha
        )
        self.confidence = self.grievance - self.net_risk

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, True, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

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
