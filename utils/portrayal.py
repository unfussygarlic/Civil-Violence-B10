from env import World
from agents.citizen import Citizen
from .params import model_params, gridsize, confidence_threshold
from .gradient import linear_gradient

# All agents will be circle in a 25x25 grid
#   Description of colors agents will take(all agents are circles):
#     revolt agent will be gray
#     cop agent will be black
#     rich class agent will be a tone of sour cherry
#     middle class agent will be red
#     poor class agent will be yellow
#     any agent that gets jailed becomes a black square

RICH_COLOR = "#b30000"
MIDDLE_COLOR = "#ff0000"
POOR_COLOR = "#ffa64d"
COP_COLOR = "#000000"
GRIEVANCE_GRAD = linear_gradient("#ffffb7", "#9b870d", n = 100)["hex"]


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
                portrayal["Color"] = RICH_COLOR

            elif agent.status == "Middle":
                portrayal["Color"] = MIDDLE_COLOR

            elif agent.status == "Poor":
                portrayal["Color"] = POOR_COLOR

            else:
                portrayal["Color"] = "blue"

    elif agent.alignment == "Cop":
        portrayal["Text"] = f"Cop {agent.unique_id}"
        portrayal["Color"] = COP_COLOR

    return portrayal

def grievance_portrayal(agent):
    portrayal = {"Shape": "rect",
                 "x": agent.pos[0], "y": agent.pos[1],
                 "Layer": 0,
                 "Filled": "true"}

    if isinstance(agent,Citizen):
        grievance_value = int(agent.grievance * 100)
        color = GRIEVANCE_GRAD[grievance_value]
        portrayal['Color'] = color 
        portrayal['w'] = 0.75
        portrayal['h'] = 0.75

    elif agent.alignment == "Cop":
        portrayal['w'] = 0.75
        portrayal['h'] = 0.75
        portrayal["Color"] = COP_COLOR

    return portrayal