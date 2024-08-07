from mesa.visualization.ModularVisualization import ModularServer

# Essa classe vai ser realocada para futuro arquivo model
class ModeloEmBranco:
    def __init__(self):
        pass

server = ModularServer(ModeloEmBranco, [], "Simulação de Propagação de Fogo", {})
server.port = 8080
