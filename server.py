from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import Slider
from model import Modelo

def agent_portrayal(agent):
    # Defina as cores baseadas no tipo de vegetação
    color_map = {
        'grama': 'lightgreen',
        'arbusto': 'darkgreen',
        'árvore': 'brown',
        'terreno_úmido': 'blue'
    }

    # Determine a cor do agente baseado no seu estado atual
    if agent.state == 'red':
        color = 'red'
    elif agent.state == 'gray':
        color = 'gray'
    else:
        color = color_map[agent.vegetation_type]

    # Define a aparência do agente na visualização
    portrayal = {
        "Shape": "rect",
        "Filled": True,
        "Color": color,
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
