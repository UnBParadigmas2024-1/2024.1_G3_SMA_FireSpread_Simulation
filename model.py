from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

class FixedPositionAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class ModeloEmBranco(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        # Criar um agente e colocá-lo na posição fixa (4, 4)
        agent = FixedPositionAgent(1, self)
        self.schedule.add(agent)
        self.grid.place_agent(agent, (3, 16))

    def step(self):
        self.schedule.step()