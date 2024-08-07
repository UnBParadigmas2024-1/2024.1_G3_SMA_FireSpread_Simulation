from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from mesa import Agent

class FixedPositionAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Inicializa a posição
        self.x, self.y = None, None  # Valores temporários até o agente ser colocado na grid

    def step(self):
        # Se a posição ainda não foi inicializada, inicializa com a posição atual
        if self.x is None or self.y is None:
            self.x, self.y = self.pos

        # Verifica se o agente está na última coluna
        if self.x == self.model.grid.width - 1:
            # Move para a próxima linha
            new_x = 0
            new_y = self.y + 1
        else:
            # Move para a direita na mesma linha
            new_x = self.x + 1
            new_y = self.y
        # Remove o agente da posição atual
        self.model.grid.remove_agent(self)

        # Atualiza a posição do agente
        self.x, self.y = new_x, new_y
        self.pos = (self.x, self.y)

        # Coloca o agente na nova posição
        self.model.grid.place_agent(self, (self.x, self.y))

        # Imprime a nova posição
        print(f"Nova posição: ({self.x}, {self.y})")

class ModeloEmBranco(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        # Criar um agente e colocá-lo na posição fixa (4, 4)
        agent = FixedPositionAgent(1, self)
        self.schedule.add(agent)
        self.grid.place_agent(agent, (0, 0))

    def step(self):
        self.schedule.step()