import sys
import random
import statistics as s
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from agents.citizen import Citizen
from agents.authority import Cop, Bank
from utils.params import reduction_factor


class World(Model):
    """
    The class World which inherits from Model and is responsible for the
    intarations for the experiment.

    Attributs:
      gridsize: dimentions of the world grid
      cop_density: density of the cops placed in world
      citizen_density: density of the citizens in world
      agent_type: the alignment of agent either as cop or citizen
      l_state: the legitimacy state in world
      reduction_constant: the constant attribute which decide by what rate
      the state of l_state will reduce
    """

    def __init__(
        self,
        gridsize,
        cop_density,
        citizen_density,
        agent_type,
        legitimacy,
        l_state,
        reduction_constant,
        active_threshold,
        include_wealth,
        rich_threshold,
    ):

        # Create a new World instance.

        # Args:
        #    gridsize: the size of grid
        #    cop_density: density of cops to be placed
        #    citizen_density: density of citizens to be placed
        #    agent_type: the alignment of agent either as cop or citizen
        #    l_state: the legitimacy state
        #    reduction_constant: the constant attribute which decide by what rate
        #        the state of l_state will reduce

        self.cop_density = cop_density
        self.citizen_density = citizen_density
        self.agent_type = agent_type

        self.legitimacy = legitimacy
        self.l_state = l_state

        self.reduction_constant = reduction_constant
        self.active_threshold = active_threshold
        self.include_wealth = include_wealth
        self.rich_threshold = rich_threshold

        self.ap_constant = 2.3

        # Agent count r_c: rich_count, r_a_c: rich_active_count, m_c: middle_count, m_a_c: middle_active_count, p_c: poor_count, p_a_c: poor_active_count,.
        self.r_c = 0
        self.r_a_c = 0
        self.m_c = 0
        self.m_a_c = 0
        self.p_c = 0
        self.p_a_c = 0

        self.mean = 0
        self.kill_agents = []
        self.agents_killed = 0
        self.grid = MultiGrid(gridsize, gridsize, False)
        self.schedule = SimultaneousActivation(self)
        self.placement(gridsize)
        self.running = True

    def placement(self, gridsize):

        # Placement of agents inside the Grid

        # Arguments:
        # gridsize: Dimensions of grid

        unique_id = 1

        if self.cop_density + self.citizen_density > 1:
            print("Density ratios must not exceed 1", file=sys.stderr)

        self.bank = Bank(1, self)

        for (_, x, y) in self.grid.coord_iter():

            if self.random.random() < self.cop_density:
                a = Cop(unique_id, self)
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))
                unique_id += 1

            elif self.random.random() < (self.cop_density + self.citizen_density):
                a = Citizen(
                    unique_id,
                    self,
                    hardship=self.random.random(),
                    risk_aversion=self.random.random(),
                    bank=self.bank,
                    rich_threshold=self.rich_threshold,
                )
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))
                unique_id += 1

        self.datacollector = DataCollector(
            model_reporters={
                "Poor Grievance": lambda m: self.measure_poor_grievance(m),
                "Middle Grievance": lambda m: self.measure_middle_grievance(m),
                "Rich Grievance": lambda m: self.measure_rich_grievance(m),
                "Calm": lambda m: self.count_calm(m),
                "Revolt": lambda m: self.count_revolt(m),
                "Jail": lambda m: self.count_jailed(m),
                "Cops": lambda m: self.count_cops(m),
                "Rich": lambda m: self.count_rich(m),
                "Middle": lambda m: self.count_middle(m),
                "Poor": lambda m: self.count_poor(m),
                "Rich Wealth": lambda m: self.measure_rich_wealth(m),
                "Middle Wealth": lambda m: self.measure_middle_wealth(m),
                "Poor Wealth": lambda m: self.measure_poor_wealth(m),
                "Rich Confidence": lambda m: self.measure_rich_confidence(m),
                "Middle Confidence": lambda m: self.measure_middle_confidence(m),
                "Poor Confidence": lambda m: self.measure_poor_confidence(m),
                "Rich Hardship": lambda m: self.measure_rich_hardship(m),
                "Middle Hardship": lambda m: self.measure_middle_hardship(m),
                "Poor Hardship": lambda m: self.measure_poor_hardship(m),
                "Legitimacy": lambda m: self.measure_legitimacy(m),
                "WO Revolt": lambda m: self.wo_wealth_active(m),
                "WO Calm": lambda m: self.wo_wealth_calm(m),
                "WO Jail": lambda m: self.wo_wealth_jail(m),
            }
        )

    def update_agent_count(self):

        # Updates the number of current and active agents

        self.r_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen" and a.status == "Rich"
            ]
        )
        self.r_a_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen"
                and a.status == "Rich"
                and a.state == "Revolt"
            ]
        )

        self.m_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen" and a.status == "Middle"
            ]
        )
        self.m_a_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen"
                and a.status == "Middle"
                and a.state == "Revolt"
            ]
        )

        self.p_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen" and a.status == "Poor"
            ]
        )
        self.p_a_c = len(
            [
                a
                for a in self.schedule.agents
                if a.alignment == "Citizen"
                and a.status == "Poor"
                and a.state == "Revolt"
            ]
        )

    def mean_wealth(self):

        # Calculate the mean wealth of all the citizen agents

        self.agents = [
            agent.savings
            for agent in self.schedule.agents
            if agent.alignment == "Citizen"
        ]
        self.mean = s.mean(self.agents)

    def update_core(self):
        if self.l_state:
            if self.legitimacy > 0.0:
                self.legitimacy -= self.reduction_constant
            else:
                self.legitimacy = 0.0

    def step(self):

        # Calculation of world attributes in one step(iteration) of execution

        self.update_agent_count()
        self.datacollector.collect(self)
        self.mean_wealth()
        self.schedule.step()
        self.update_core()

        if self.kill_agents:
            self.kill_agents = list(dict.fromkeys(self.kill_agents))
            for i in self.kill_agents:
                self.grid.remove_agent(i)
                self.schedule.remove(i)
            self.kill_agents = []

        total_agents = len(
            [a for a in self.schedule.agents if a.alignment == "Citizen"]
        )
        if total_agents < 2:
            self.running = False

    @staticmethod
    def count_calm(model):
        a = len(
            [
                a
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.state == "Calm"
            ]
        )
        return a

    @staticmethod
    def count_revolt(model):
        a = len(
            [
                a
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.state == "Revolt"
            ]
        )
        return a

    @staticmethod
    def count_jailed(model):
        a = len(
            [
                a
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.state == "Jail"
            ]
        )
        return a

    @staticmethod
    def count_cops(model):
        a = len([a for a in model.schedule.agents if a.alignment == "Cop"])
        return a

    @staticmethod
    def count_rich(model):
        a = len(
            [
                a
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.status == "Rich"
            ]
        )
        return a

    @staticmethod
    def count_middle(model):
        a = len(
            [
                a
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.status == "Middle"
            ]
        )
        return a

    @staticmethod
    def count_poor(model):
        a = len(
            [
                a
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.status == "Poor"
            ]
        )
        return a

    @staticmethod
    def measure_poor_grievance(model):
        if model.include_wealth:
            confidence = [
                a.grievance
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.status == "Poor"
            ]
            if confidence:
                total = sum(confidence)
                return total
            else:
                return 0
        else:
            confidence = [
                a.grievance for a in model.schedule.agents if a.alignment == "Citizen"
            ]
            return sum(confidence)

    @staticmethod
    def measure_middle_grievance(model):
        confidence = [
            a.grievance
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Middle"
        ]
        if confidence:
            total = sum(confidence)
            return total
        else:
            return 0

    @staticmethod
    def measure_rich_grievance(model):
        confidence = [
            a.grievance
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Rich"
        ]
        if confidence:
            total = sum(confidence)
            return total
        else:
            return 0

    @staticmethod
    def measure_rich_wealth(model):
        wealth = [
            a.wealth
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Rich"
        ]
        return s.mean(wealth) if wealth else 0

    @staticmethod
    def measure_middle_wealth(model):
        wealth = [
            a.wealth
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Middle"
        ]
        return s.mean(wealth) if wealth else 0

    @staticmethod
    def measure_poor_wealth(model):
        wealth = [
            a.wealth
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Poor"
        ]
        return s.mean(wealth) if wealth else 0

    @staticmethod
    def measure_poor_confidence(model):
        confidence = [
            a.confidence
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Poor"
        ]
        if confidence:
            total = s.mean(confidence)
            return total
        else:
            return 0

    @staticmethod
    def measure_middle_confidence(model):
        confidence = [
            a.confidence
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Middle"
        ]
        if confidence:
            total = s.mean(confidence)
            return total
        else:
            return 0

    @staticmethod
    def measure_rich_confidence(model):
        confidence = [
            a.confidence
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Rich"
        ]
        if confidence:
            total = s.mean(confidence)
            return total
        else:
            return 0

    @staticmethod
    def measure_total_reserves(model):
        return s.mean(model.bank.total_reserves)

    @staticmethod
    def measure_poor_hardship(model):

        confidence = [
            a.hardship
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Poor"
        ]
        if confidence:
            total = sum(confidence)
            return total
        else:
            return 0

    @staticmethod
    def measure_middle_hardship(model):
        confidence = [
            a.hardship
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Middle"
        ]
        if confidence:
            total = sum(confidence)
            return total
        else:
            return 0

    @staticmethod
    def measure_rich_hardship(model):
        confidence = [
            a.hardship
            for a in model.schedule.agents
            if a.alignment == "Citizen" and a.status == "Rich"
        ]
        if confidence:
            total = sum(confidence)
            return total
        else:
            return 0

    @staticmethod
    def measure_legitimacy(model):
        return model.legitimacy * 100

    @staticmethod
    def wo_wealth_active(model):
        if model.include_wealth == False:
            active = [
                a
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.state == "Revolt"
            ]
            return len(active)
        else:
            return 0

    @staticmethod
    def wo_wealth_calm(model):
        if model.include_wealth == False:
            active = [
                a
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.state == "Calm"
            ]
            return len(active)
        else:
            return 0

    @staticmethod
    def wo_wealth_jail(model):
        if model.include_wealth == False:
            active = [
                a
                for a in model.schedule.agents
                if a.alignment == "Citizen" and a.state == "Jail"
            ]
            return len(active)
        else:
            return 0
