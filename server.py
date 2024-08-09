from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import Slider
from model import Modelo
from agent import StaticAgent, DynamicAgent

def agent_portrayal(agent):
    # Define the colors for static agents based on vegetation type
    color_map = {
        'grama': 'lightgreen',
        'arbusto': 'darkgreen',
        'árvore': 'brown',
        'terreno_úmido': 'blue'
    }

    if isinstance(agent, StaticAgent) or isinstance(agent, DynamicAgent):
        if agent.state == 'red':
            color = 'red'
        elif agent.state == 'gray':
            color = 'gray'
        elif agent.state == 'active':
            color = 'black'
        else:
            color = color_map[agent.vegetation_type]
        portrayal = {
            "Shape": "rect",
            "Filled": True,
            "Color": color,
            "Layer": 0, 
            "w": 1,
            "h": 1
        }

    return portrayal



# Configura a grade de visualização
grid = CanvasGrid(agent_portrayal, 100, 100, 500, 500)

# Parâmetros do grid, incluindo sliders para ajustar a densidade da floresta e o número de agentes dinâmicos
grid_params = {
    "width": 100,
    "height": 100,
    "density": Slider("Densidade", 0.5, 0.1, 1.0, 0.1),
    "num_dynamic_agents": Slider("Número de Agentes Dinâmicos", 1000, 0, 1000, 1)
}

# Cria o servidor da simulação, vinculando o modelo e a grade de visualização
server = ModularServer(Modelo, [grid], "Simulação de Grid com Agente semifixo", grid_params)
server.port = 8080
server.launch()
