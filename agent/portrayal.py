from .env import World
from .people import Citizen
from .params import model_params, gridsize, confidence_threshold

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Layer" : 0, "Filled": "True", "r": "0.6"}

    if agent.alignment == "Citizen":
        if agent.confidence > confidence_threshold:
            portrayal["Color"] = "gray"
        else:
            if agent.status == "Rich":
                portrayal["Color"] = "#b30000"

            elif agent.status == "Middle":
                portrayal["Color"] = "#ff0000"

            elif agent.status == "Poor":
                portrayal["Color"] = "#ffa64d"
            
            else:
                portrayal["Color"] = "blue"
    
    elif agent.alignment == "Cop":
        portrayal["Color"] = "black"

    return portrayal