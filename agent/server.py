from .env import World
from .people import Citizen
from .params import model_params, gridsize, grienvance_threshold
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Layer" : 0, "Filled": "True", "r": "0.6"}

    if agent.alignment == "Citizen":
        if agent.grievance > grienvance_threshold:
            portrayal["Color"] = "gray"
        else:
            if agent.status == "Rich":
                portrayal["Color"] = "green"

            elif agent.status == "Middle":
                portrayal["Color"] = "blue"

            elif agent.status == "Poor":
                portrayal["Color"] = "red"
    
    elif agent.alignment == "Cop":
        portrayal["Color"] = "black"

    return portrayal

grid = CanvasGrid(agent_portrayal, gridsize, gridsize, 500, 500)

server = ModularServer(World, [grid], "World", model_params)
server.port = 8521