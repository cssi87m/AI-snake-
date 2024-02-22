# Conduct a USR buffer for training 
from Model import *
from random import sample 
class USR:
    def __init__(self):
        self.buffer = []

    def append(self, experience):
        if len(self.buffer) < 100:
            self.buffer.append(experience)
        else:
            self.buffer.pop(0)
            self.buffer.append(experience)

    def sample(self, batch_size):
        batch = sample(self.buffer, batch_size)
        return batch

    def __len__(self):
        return len(self.buffer)