from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import StaticAgent, DynamicAgent  # Importa DynamicAgent
import random

class Modelo(Model):
    def __init__(self, width, height, density, num_dynamic_agents=1):
        # Inicializa MultiGrid e RandomActivation
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.density = density

        agent_id = 0
        tipos_vegetacao = ['grama', 'arbusto', 'árvore', 'terreno_úmido']

        # Itera sobre todas as coordenadas na grade
        for (agents, coordinates) in self.grid.coord_iter():
            x, y = coordinates
            # Adiciona agentes estáticos com base na densidade fornecida
            if self.random.random() < density:
                initial_fire = (y == 99)  # Incêndio inicial na última linha de y
                tipo_vegetacao = random.choice(tipos_vegetacao)
                agent = StaticAgent(agent_id, self, x, y, tipo_vegetacao, initial_fire)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
                agent_id += 1

        # Adiciona agentes dinâmicos
        for i in range(num_dynamic_agents):
            # Escolhe uma posição aleatória para o agente dinâmico
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
