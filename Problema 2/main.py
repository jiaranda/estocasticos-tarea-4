import numpy as np
import matplotlib.pyplot as plt


def instance_generator():
    def instance():
        # codigo visto en clases
        u = np.random.uniform(0, 1)
        return (u * 7/4) ** (4/7)
    return instance


if __name__ == "__main__":
    data = list()
    gen = instance_generator()
    for i in range(100):
        data.append(gen())
    plt.hist(data, density=True)
    plt.show()