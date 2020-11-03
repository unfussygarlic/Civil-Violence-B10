from env import World
from agents.citizen import Citizen
from utils.params import model_params, gridsize
from utils.portrayal import agent_portrayal, grievance_portrayal
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer

# Chart showing the varying grievance levels of agents
grievance_chart = ChartModule(
    [
        {"Label": "Poor Grievance", "Color": "Red"},
        {"Label": "Middle Grievance", "Color": "Yellow"},
        {"Label": "Rich Grievance", "Color": "Green"},
    ],
    data_collector_name="datacollector"
)

# Chart showing the varying confidence levels of agents
confidence_chart = ChartModule(
    [
        {"Label": "Poor Confidence", "Color": "Red"},
        {"Label": "Middle Confidence", "Color": "Yellow"},
        {"Label": "Rich Confidence", "Color": "Green"},
    ],
    data_collector_name="datacollector"
)

# Chart showing the varying hardship levels of agents
hardship_chart = ChartModule(
    [
        {"Label": "Poor Hardship", "Color": "Red"},
        {"Label": "Middle Hardship", "Color": "Yellow"},
        {"Label": "Rich Hardship", "Color": "Green"},
    ],
    data_collector_name="datacollector"
)

# Chart showing the varying wealth of agents
wealth_chart = ChartModule(
    [
        {"Label": "Poor Wealth", "Color": "Red"},
        {"Label": "Middle Wealth", "Color": "Yellow"},
        {"Label": "Rich Wealth", "Color": "Green"},
    ],
    data_collector_name="datacollector"
)

# Chart showing the overall count agents
citizen_count_chart = ChartModule(
    [
        {"Label": "Poor", "Color": "Red"},
        {"Label": "Middle", "Color": "Yellow"},
        {"Label": "Rich", "Color": "Green"},
        {"Label": "Legitimacy", "Color": "Blue"},
        {"Label": "Cops", "Color": "Black"}
    ],
    data_collector_name="datacollector"
)

# Chart showing the state of agents when wealth is not included
without_chart = ChartModule([{"Label": "WO Calm", "Color": "Green"},
                            {"Label": "WO Revolt", "Color": "Red"},
                            {"Label": "WO Jail", "Color": "Gray"},
                            {"Label": "Cops", "Color": "Black"},
                            {"Label": "Legitimacy", "Color": "Blue"}],
                            data_collector_name="datacollector")

# Chart showing the state of agents when wealth is included
state_chart = ChartModule([{"Label": "Calm", "Color": "Green"},
                            {"Label": "Revolt", "Color": "Red"},
                            {"Label": "Jail", "Color": "Gray"},
                            {"Label": "Cops", "Color": "Black"},
                            {"Label": "Legitimacy", "Color": "Blue"}],
                            data_collector_name="datacollector")

# Main grid showcasing the simulation of agents
grid = CanvasGrid(agent_portrayal, gridsize, gridsize, 500, 500)
# Grievance grid potratying the varying grievance levels of agents
grievance_grid = CanvasGrid(grievance_portrayal, gridsize, gridsize, 500, 500)

# Initializing the environment and placement of grids
server = ModularServer(World, [grid, grievance_grid, state_chart, citizen_count_chart, grievance_chart, hardship_chart, wealth_chart, without_chart], "World", model_params)
# Port number for visualization
server.port = 8521