from mesa import Agent
import random

class StaticAgent(Agent):
    def __init__(self, unique_id, model, x, y, initial_fire=False):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.state = 'red' if initial_fire else 'green'
        self.red_steps = 0    
        self.initial_fire = initial_fire

    def step(self):
        if self.state == 'red':
            self.red_steps += 1
            if self.red_steps > 20:
                self.state = 'gray'
        elif self.state == 'green':
            if self.initial_fire:
                return
            
            neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False)
            red_neighbors = sum(1 for neighbor in neighbors if neighbor.state == 'red')
            
            prob = 0.003 * (2 ** red_neighbors)
            if random.random() < prob:
                self.state = 'red'
                self.red_steps = 1
