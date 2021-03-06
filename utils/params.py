import numpy as np
from mesa.visualization.UserParam import UserSettableParameter


# The file contain the parameters that affect the flow of entire experiment.


# grid size of one size of the model instance
gridsize = 50

model_params = {
    "gridsize": gridsize,
    "cop_density": UserSettableParameter("slider", "Cop Density", 0.01, 0, 1, 0.001),
    "citizen_density": UserSettableParameter(
        "slider", "Citizen Density", 0.7, 0, 1, 0.001
    ),
    "agent_type": "Poor",
    "legitimacy": UserSettableParameter("slider", "Legitimacy", 1.0, 0.001, 1, 0.001),
    "l_state": UserSettableParameter("checkbox", "Decrease Legitimacy", value=False),
    "reduction_constant": UserSettableParameter(
        "number", "Reduction Constant", value=0.01
    ),
    "active_threshold": UserSettableParameter(
        "slider", "Active Threshold", 0.2, 0, 1, 0.1
    ),
    "include_wealth": UserSettableParameter("checkbox", "Include Wealth", value=True),
    "rich_threshold": UserSettableParameter("slider", "Rich Threshold", 10, 1, 20),
}

# Parameter Constants
k_c = {"Rich": 0.3, "Middle": 0.5, "Poor": 0.7}
k_d = {"Rich": 0.3, "Middle": 0.5, "Poor": 0.7}
k_e = {"Rich": 0.2, "Middle": 0.85, "Poor": 0.9}
k_p = 0.8
k_af = 0.8

# Wealth increment of individual agents
wealth_inc = {
    "Poor": np.random.uniform(0, 0.33),
    "Middle": np.random.uniform(0.33, 0.66),
    "Rich": np.random.uniform(0.66, 1.0),
}

timestep = 2

# Threshold
confidence_threshold = 0.1
reduction_factor = 0.01
cop_threshold = 0.66

# Jail parameters
jail_period = 30
kill_threshold = 10

# Agent and Cop choice
r_c = 0.2

# Vision
citizen_vision = 1
cop_vision = 1
