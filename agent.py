from mesa import Agent
import random

class StaticAgent(Agent):
    def __init__(self, unique_id, model, x, y, initial_fire=False):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.state = 'red' if initial_fire else 'green'
        self.red_steps = 0    

    def step(self):
        if self.state == 'red':
            self.red_steps += 1
            if self.red_steps > 20:
                self.state = 'gray'
        elif self.state == 'green':
            neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False)
            if any(neighbor.state == 'red' for neighbor in neighbors):
                self.red_steps = 1
                self.state = 'red'
