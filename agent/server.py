from .env import World
from .people import Citizen
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def agent_portrayal(agent):
    portrayal = {"Shape": "circle","Layer" : 0, "Filled": "True", "r": "0.6"}

    if agent.status == "Rich":
        portrayal["Color"] = "green"

    elif agent.status == "Middle":
        portrayal["Color"] = "blue"

    elif agent.status == "Poor":
        portrayal["Color"] = "red"
    
    else:
        portrayal["Color"] = "black"

    return portrayal

gridsize = 50

grid = CanvasGrid(agent_portrayal, gridsize, gridsize, 500, 500)
model_params = {"gridsize" : gridsize,
                "cop_density" : UserSettableParameter("slider", "Cop Density", 0.01, 0, 1, 0.001) }
server = ModularServer(World, [grid], "World", model_params)
server.port = 8521