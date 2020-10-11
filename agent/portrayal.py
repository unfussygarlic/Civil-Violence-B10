from .env import World
from .people import Citizen
from .params import model_params, gridsize, confidence_threshold
 
def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Layer": 0, "Filled": "True", "r": "0.5"}

    if agent.alignment == "Citizen":
        portrayal[
            "Text"
        ] = f"{agent.unique_id} | {agent.status} | {round(agent.confidence,2)}"

        if agent.state == "Revolt":
            portrayal["Color"] = "gray"

        elif agent.state == "Jail":
            portrayal["Shape"] = "rect"
            portrayal["w"] = 0.5
            portrayal["h"] = 0.5
            portrayal["Color"] = "black"

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
        portrayal["Text"] = f"Cop {agent.unique_id}"
        portrayal["Color"] = "black"

    return portrayal
