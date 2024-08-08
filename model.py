from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import StaticAgent  # Importa a classe StaticAgent do arquivo agent.py

class Modelo(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        agent_id = 0
        for x in range(width):
            for y in range(height):
                initial_fire = (x == 0)
                agent = StaticAgent(agent_id, self, x, y, initial_fire)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
                agent_id += 1

    def step(self):
        self.schedule.step()
