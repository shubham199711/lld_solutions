from copy import deepcopy

class MLModel:
    def __init__(self, layers, optimizer):
        self.layers = layers
        self.optimizer = optimizer
    
    def clone(self):
        return deepcopy(self)


base = MLModel(
    layers=[128, 256, 512],
    optimizer={"type": "adam", "lr": 0.001}
)


experiment = base.clone()
experiment.optimizer['lr'] = 0.0001

