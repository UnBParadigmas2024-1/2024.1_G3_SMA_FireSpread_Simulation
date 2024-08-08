from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import Slider
from model import Modelo

def agent_portrayal(agent):
    portrayal = {
        "Shape": "rect",
        "Filled": True,
        "Color": agent.state,
        "Layer": 0,
        "w": 1,
        "h": 1
    }
    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

model_params = {
    "width": 20,
    "height": 20
}

server = ModularServer(Modelo, [grid], "Simulação de Grid com Agente semifixo", model_params)
server.port = 8080
server.launch()
