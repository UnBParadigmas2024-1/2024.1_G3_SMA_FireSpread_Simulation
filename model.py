from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import StaticAgent

class Modelo(Model):
    def __init__(self, width, height, density):
        self.grid = MultiGrid(width, height, torus=False)
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

        self.updates = []

    def step(self):
        self.updates = []
        self.schedule.step()
        self.apply_updates()

    def apply_updates(self):
        for (x, y) in self.updates:
            agent = self.grid.get_cell_list_contents([(x, y)])[0]
            if agent.state == 'green':
                agent.state = 'red'
                agent.red_steps = 1
