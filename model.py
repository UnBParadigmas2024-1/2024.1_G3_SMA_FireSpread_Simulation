from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import StaticAgent

class Modelo(Model):
    def __init__(self, width, height, density):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.density = density

        agent_id = 0
        for (agents, coordinates) in self.grid.coord_iter():
            x, y = coordinates
            if self.random.random() < density:
                initial_fire = (x == 0)
                agent = StaticAgent(agent_id, self, x, y, initial_fire)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
                agent_id += 1

    def step(self):
        self.schedule.step()
