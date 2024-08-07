from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import random


class StaticAgent(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.state = 'green'
        self.red_steps = 0    # Contador de passos em que o agente está vermelho

    def step(self):
        if self.state == 'red':
            self.red_steps += 1
            # Se o agente estiver vermelho por mais de dois passos, muda para cinza
            if self.red_steps > 20:
                self.state = 'gray'
        if self.state == 'green':
            neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False)
            red_neighbors = sum(1 for neighbor in neighbors if neighbor.state == 'red')
            
            # Ajusta a probabilidade de mudar para vermelho
            prob = 0.003 * (2 ** red_neighbors)  # Dobra a chance para cada vizinho vermelho
            if random.random() < prob:
                self.state = 'red'
                self.red_steps = 1  # Reinicia o contador quando muda para vermelho

class Modelo(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Preencher a grid com agentes estáticos
        agent_id = 0
        for x in range(width):
            for y in range(height):
                # Cria um novo agente estático em cada posição (x, y)
                agent = StaticAgent(agent_id, self, x, y)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
                agent_id += 1

    def step(self):
        self.schedule.step()