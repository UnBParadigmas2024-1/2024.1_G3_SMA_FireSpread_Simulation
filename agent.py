from mesa import Agent
import random

class StaticAgent(Agent):
    def __init__(self, unique_id, model, x, y, vegetation_type, initial_fire=False):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.vegetation_type = vegetation_type  # Tipo de vegetação
        self.state = 'red' if initial_fire else 'green'
        self.red_steps = 0
        self.ignition_probabilities = {
            'grama': 1.0,
            'arbusto': 0.8,
            'árvore': 0.6,
            'terreno_úmido': 0.3
        }
 
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
                if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
                    ignition_probability = self.ignition_probabilities[self.vegetation_type]
                elif dx == 1 and dy == 1:
                    ignition_probability = self.ignition_probabilities[self.vegetation_type] * 0.573
                else:
                    continue

                if neighbor.state == 'red' and random.random() < ignition_probability:
                    self.model.updates.append((self.x, self.y))
                    break

# Novo agente dinâmico que será capaz de se mover e apagar o fogo
class DynamicAgent(Agent):
    def __init__(self, unique_id, model, x, y, fire_extinguish_prob=0.5):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.fire_extinguish_prob = fire_extinguish_prob  # Probabilidade de apagar o fogo
        self.state = 'active'

    def move(self):
        # Obtém as posições vizinhas que estão livres (sem outros agentes)
        possible_steps = self.model.grid.get_neighborhood((self.x, self.y), moore=True, include_center=False)
        free_steps = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos)]
        
        if len(free_steps) > 0:
            # Escolhe uma nova posição aleatória e move o agente
            new_position = random.choice(free_steps)
            self.model.grid.move_agent(self, new_position)
            self.x, self.y = new_position

    def extinguish_fire(self):
        # Verifica se a célula atual ou células adjacentes têm fogo
        neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=True)
        for neighbor in neighbors:
            if isinstance(neighbor, StaticAgent) and neighbor.state == 'red':
                if random.random() < self.fire_extinguish_prob:
                    neighbor.state = 'green'  # Apaga o fogo, voltando para o estado verde

    def step(self):
        self.move()
        self.extinguish_fire()