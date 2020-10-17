from .env import World
from .people import Citizen
from .params import model_params, gridsize, confidence_threshold

# All agents will be circle in a 25x25 grid
#   Description of colors agents will take(all agents are circles):
#     revolt agent will be gray
#     cop agent will be black
#     rich class agent will be a tone of sour cherry
#     middle class agent will be red
#     poor class agent will be yellow
#     any agent that gets jailed becomes a black square


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "True", "Layer": 0, "r": "0.5"}

    if isinstance(agent,Citizen):
        portrayal[
            "Text"
        ] = f"{agent.status} | {round(agent.confidence,2)} | {round(agent.grievance,2)}"

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
