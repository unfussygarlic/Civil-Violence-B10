from mesa.visualization.UserParam import UserSettableParameter

gridsize = 10

model_params = {"gridsize" : gridsize,
                "cop_density" : UserSettableParameter("slider", "Cop Density", 0.01, 0, 1, 0.001),
                "citizen_density" : UserSettableParameter("slider", "Citizen Density", 0.7, 0, 1, 0.001),
                "agent_type" : "Poor",
                "corruption" : UserSettableParameter("slider", "Corruption", 0.0, 0, 1, 0.001),
                "democracy" : UserSettableParameter("slider", "Democracy", 0.99, 0, 1, 0.001),
                "employment" : UserSettableParameter("slider", "Employment", 0.99, 0, 1, 0.001)}

# Parameter Constants
k_c = {"Rich" : 0.3, "Middle" : 0.5, "Poor" : 0.7}
k_d = {"Rich" : 0.3, "Middle" : 0.5, "Poor" : 0.7}
k_e = {"Rich" : 0.2, "Middle" : 0.85, "Poor" : 0.9}
k_p = 0.8

wealth_inc = {"Rich" : [10, 11, 12, 13, 14, 15], "Middle" : [5, 6, 7, 8, 9], "Poor" : [0, 1, 2, 3, 4]}
timestep = 2

# Threshold
grienvance_threshold = 0.7