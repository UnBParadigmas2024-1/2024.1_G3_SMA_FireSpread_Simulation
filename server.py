from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import Slider
from model import Modelo

def agent_portrayal(agent):
    # Define a aparencia do agente na visualização
    portrayal = {
        "Shape": "rect",
        "Filled": True,
        "Color": agent.state,
        "Layer": 0,
        "w": 1,
        "h": 1
    }
    return portrayal

# Configura a grade de visualizacao
grid = CanvasGrid(agent_portrayal, 100, 100, 500, 500)

# Parametros do grid, incluindo um slider para ajustar a densidade da floresta
grid_params = {
    "width": 100,
    "height": 100,
    "density": Slider("Densidade", 0.5, 0.1, 1.0, 0.1)
}

# Cria o servidor da simulacao, vinculando o modelo e a grade de visualizacao
server = ModularServer(Modelo, [grid], "Simulação de Grid com Agente semifixo", grid_params)
server.port = 8080
server.launch()
