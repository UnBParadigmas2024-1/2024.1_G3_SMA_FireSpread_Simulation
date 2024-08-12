from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import Slider, StaticText
from model import Modelo
from agent import StaticAgent, DynamicAgent


def agent_portrayal(agent):
    # Define as cores para os agentes estaticos com base no tipo de vegetacao
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
    "info_text": StaticText("<div style='position: absolute; top: 150px; right: 10px; width: 300px;'>"
    "Esse é um simulador da propagação de fogo em uma floresta.<br><br>"
    "Nesse contexto, o fogo se propaga entre as células adjacentes, dependendo da densidade da vegetação e do tipo de vegetação.<br><br>"
    "O ambiente contém diferentes tipos de vegetação, cada um com uma probabilidade específica de ignição.<br><br>"
    "Agentes dinâmicos (bombeiros) se movem pelo ambiente e podem extinguir o fogo nas células dentro de seu alcance."
    "</span>""</div>"),

    "width": 100,
    "height": 100,
    "density": Slider("Densidade", 0.5, 0.1, 0.9, 0.1),
    "num_dynamic_agents": Slider("Número de Bombeiros", 250, 0, 500, 1),
    "terrain_type": Slider('Tipo de Terreno', 1, 1, 5, 1),

    "info_text2": StaticText("<span style='font-size: 10px;'>"
        "<br>Terrenos disponíveis:<br>"
        "1. Cerrado: Vegetação mista de gramíneas, arbustos e árvores esparsas.<br>"
        "2. Pântano: Terreno úmido com alta presença de áreas alagadas, vegetação mista.<br>"
        "3. Floresta Densa: Alta concentração de árvores com arbustos e pouca grama.<br>"
        "4. Campo Aberto: Predominância de gramíneas com poucas árvores e arbustos.<br>"
        "5. Distribuição Aleatória: Distribuição uniforme de tipos de vegetação."
    ),

    "info_text3": StaticText("<span style='font-size: 10px;'>"
        "<br>Cores:<br>Grama: Verde claro<br>Arbusto: Verde escuro<br>Árvore: Marrom<br>Terreno úmido: Azul")
}

# Cria o servidor da simulação, vinculando o modelo e a grade de visualização
server = ModularServer(Modelo, [grid], "Simulação de Grid com Agente semifixo", grid_params)
server.port = 8080
server.launch()
