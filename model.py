from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import StaticAgent

class Modelo(Model):
    def __init__(self, width, height, density):
        # Inicializa MultiGrid e RandomActivation
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.density = density

        agent_id = 0
        # Itera sobre todas as coordenadas na grade
        for (agents, coordinates) in self.grid.coord_iter():
            x, y = coordinates
            # Adiciona agentes com base na densidade fornecida
            if self.random.random() < density:
                initial_fire = (y == 99)  # Incendio inicial na ultima linha de y
                agent = StaticAgent(agent_id, self, x, y, initial_fire)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
                agent_id += 1

        self.updates = []  # Lista de atualizações a serem aplicadas

    def step(self):
        # Reinicia a lista de atualizacoes a cada etapa e executa todos os agentes
        self.updates = []
        self.schedule.step()
        self.apply_updates()

    def apply_updates(self):
        # Aplica as atualizacoes de estado dos agentes
        for (x, y) in self.updates:
            agent = self.grid.get_cell_list_contents([(x, y)])[0]
            if agent.state == 'green':
                agent.state = 'red'
                # Contador de passos de red
                agent.red_steps = 1
