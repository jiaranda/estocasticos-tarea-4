import plotly.figure_factory as ff
import numpy as np

def instance_generator():
    def instance():
        # codigo visto en clases
        u = np.random.uniform(0, 1)
        return (u * (7/4)) ** (4/7)
    return instance

x = list()
gen = instance_generator()
c = (7/4)**(4/7)
for i in range(10000):
    g = gen()
    x.append(g)


hist_data = [x]


group_labels = ['distplot'] # name of the dataset

fig = ff.create_distplot(hist_data, group_labels, bin_size=0.02, histnorm='probability')
fig.show()