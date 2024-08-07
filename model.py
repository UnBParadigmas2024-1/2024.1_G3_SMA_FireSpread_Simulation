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
        self.red_steps = 0    

    def step(self):
        if self.state == 'red':
            self.red_steps += 1
            if self.red_steps > 20:
                self.state = 'gray'
        if self.state == 'green':
            neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False)
            red_neighbors = sum(1 for neighbor in neighbors if neighbor.state == 'red')
            
            prob = 0.003 * (2 ** red_neighbors)
            if random.random() < prob:
                self.state = 'red'
                self.red_steps = 1

class Modelo(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        agent_id = 0
        for x in range(width):
            for y in range(height):
                agent = StaticAgent(agent_id, self, x, y)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
                agent_id += 1

    def step(self):
        self.schedule.step()