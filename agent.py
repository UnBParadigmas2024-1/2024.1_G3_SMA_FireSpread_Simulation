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
            for neighbor in neighbors:
                dx = abs(neighbor.pos[0] - self.x)
                dy = abs(neighbor.pos[1] - self.y)
                
                # Determina o tipo de adjacencia do vizinho
                if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):  # Adjacente ortogonalmente
                    ignition_probability = 1.0
                elif dx == 1 and dy == 1:  # Adjacente diagonalmente
                # Necessario pensar melhor em que numero usar. Usei como referencia um trecho do seguinte site: https://scipython.com/blog/the-forest-fire-model/
                    ignition_probability = 0.573
                else:
                    continue

                # Verifica se o vizinho pega fogo com base na probabilidade
                if neighbor.state == 'red' and random.random() < ignition_probability:
                    self.model.updates.append((self.x, self.y))
                    break
