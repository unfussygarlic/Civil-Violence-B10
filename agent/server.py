from .env import World
from .people import Citizen
from .params import model_params, gridsize
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from .portrayal import agent_portrayal

# Displaying current level of legitimacy, hardship and risk_aversion in percentage
# Displaying current count of Rich class people, Middle class people, Poor class people


class Core_parameters(TextElement):
    def render(self, model):
        legitimacy = model.legitimacy

        text = f"legitimacy: {round(legitimacy*100,2)}%  <br> \
                Rich count: {model.r_c}({model.r_a_c}) Middle count: {model.m_c}({model.m_a_c}) Poor count: {model.p_c}({model.p_a_c})"

        return text


# A graph showing the growth in population with each iteration

grievance_chart = ChartModule(
    [
        {"Label": "Poor Grievance", "Color": "Red"},
        {"Label": "Middle Grievance", "Color": "Yellow"},
        {"Label": "Rich Grievance", "Color": "Green"},
    ],
    data_collector_name="datacollector",
)

confidence_chart = ChartModule(
    [
        {"Label": "Poor Confidence", "Color": "Red"},
        {"Label": "Middle Confidence", "Color": "Yellow"},
        {"Label": "Rich Confidence", "Color": "Green"},
    ],
    data_collector_name="datacollector",
)

wealth_chart = ChartModule(
    [
        {"Label": "Poor Wealth", "Color": "Red"},
        {"Label": "Middle Wealth", "Color": "Yellow"},
        {"Label": "Rich Wealth", "Color": "Green"},
    ],
    data_collector_name="datacollector",
)


pie_chart = PieChartModule([{"Label": "Calm", "Color": "Green"},
                            {"Label": "Revolt", "Color": "Red"},
                            {"Label": "Jail", "Color": "Black"}], 200, 500)

grid = CanvasGrid(agent_portrayal, gridsize, gridsize, 500, 500)

server = ModularServer(World, [grid, Core_parameters(), pie_chart, grievance_chart, confidence_chart, wealth_chart], "World", model_params)
server.port = 8521
