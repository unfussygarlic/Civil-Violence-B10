from mesa.visualization.UserParam import UserSettableParameter

gridsize = 50

model_params = {"gridsize" : gridsize,
                "cop_density" : UserSettableParameter("slider", "Cop Density", 0.01, 0, 1, 0.001) }


model_params_test = {gridsize,
                    0.01}