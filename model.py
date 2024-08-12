from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import StaticAgent, DynamicAgent  # Importa DynamicAgent
import random

class Modelo(Model):
    def __init__(self, width, height, density, num_dynamic_agents=1, terrain_type=1):
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.density = density

        agent_id = 0

        
        if terrain_type == 1:  # Cerrado
            vegetation_distribution = {'grama': 0.6, 'arbusto': 0.3, 'árvore': 0.1, 'terreno_úmido': 0.0}
        elif terrain_type == 2:  # Pântano
            vegetation_distribution = {'grama': 0.1, 'arbusto': 0.2, 'árvore': 0.2, 'terreno_úmido': 0.5}
        elif terrain_type == 3:  # Floresta Densa
            vegetation_distribution = {'grama': 0.1, 'arbusto': 0.2, 'árvore': 0.6, 'terreno_úmido': 0.1}
        elif terrain_type == 4:  # Campo Aberto
            vegetation_distribution = {'grama': 0.8, 'arbusto': 0.1, 'árvore': 0.1, 'terreno_úmido': 0.0}
        elif terrain_type == 5:  # Distribuição aleatória (opção padrão)
            vegetation_distribution = {'grama': 0.25, 'arbusto': 0.25, 'árvore': 0.25, 'terreno_úmido': 0.25}
        else:
            # Valor padrão para vegetação caso o tipo de terreno não seja reconhecido
            vegetation_distribution = {'grama': 0.25, 'arbusto': 0.25, 'árvore': 0.25, 'terreno_úmido': 0.25}

        tipos_vegetacao = list(vegetation_distribution.keys())
        probabilidades = list(vegetation_distribution.values())

        for (contents, (x, y)) in self.grid.coord_iter():

            if self.random.random() < density:
                initial_fire = (y == 99)  # Incêndio inicial na última linha de y
                tipo_vegetacao = random.choices(tipos_vegetacao, probabilidades)[0]
                agent = StaticAgent(agent_id, self, x, y, tipo_vegetacao, initial_fire)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
                agent_id += 1

        # Adiciona agentes dinâmicos
        for i in range(num_dynamic_agents):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while not self.grid.is_cell_empty((x, y)):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            dynamic_agent = DynamicAgent(agent_id, self, x, y)
            self.schedule.add(dynamic_agent)
            self.grid.place_agent(dynamic_agent, (x, y))
            agent_id += 1

        self.updates = []  # Lista de atualizações a serem aplicadas


    def step(self):
        # Reinicia a lista de atualizações a cada etapa e executa todos os agentes
        self.updates = []
        self.schedule.step()
        self.apply_updates()

    def apply_updates(self):
        # Aplica as atualizações de estado dos agentes
        for (x, y) in self.updates:
            agent = self.grid.get_cell_list_contents([(x, y)])[0]
            if agent.state == 'green':
                agent.state = 'red'
                # Contador de passos de red
                agent.red_steps = 1
