import numpy as np


def exponential_instance_generator(lambd):
    def ExponentialInstance():
        # codigo visto en clases
        u = np.random.uniform(0, 1)
        return -np.log(1 - u) / lambd
    return ExponentialInstance

def uniform_instance_generator(a, b):
    def UniformInstance():
        # codigo visto en clases
        u = np.random.uniform(0, 1)
        return (b - a) * u + a
    return UniformInstance