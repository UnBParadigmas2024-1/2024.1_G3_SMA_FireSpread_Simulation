from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from model import ModeloEmBranco

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Color": "red",
        "Layer": 0
    }
    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

server = ModularServer(ModeloEmBranco, [grid], "Simulação de Grid com Agente Fixo", {"width": 20, "height": 20})
server.port = 8080
server.launch()