from .env import World
from .people import Citizen
from .params import model_params, gridsize
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from .portrayal import agent_portrayal

class Core_parameters(TextElement):
    def render(self, model):
        corruption = model.corruption
        democracy = model.democracy
        employment = model.employment

        text = f"Corruption: {round(corruption*100,2)}%  Democracy: {round(democracy*100,2)}%  Employment: {round(employment*100,2)}% <br> \
                Rich count: {model.rich_count} Middle count: {model.middle_count} Poor count: {model.poor_count}"

        return text

chart = ChartModule([{"Label": "Poor", "Color": "Red"},
                    {"Label": "Middle", "Color": "Yellow"},
                    {"Label": "Rich", "Color": "Green"}],
                    data_collector_name='datacollector')

grid = CanvasGrid(agent_portrayal, gridsize, gridsize, 500, 500)

server = ModularServer(World, [grid, Core_parameters(), chart], "World", model_params)
server.port = 8521