class Client:
    def __init__(self, arrival_10_to_12_distr, arrival_12_to_16_distr, arrival_16_to_22_distr, products_distr):
        self.arrival_10_to_12_distr = arrival_10_to_12_distr
        self.arrival_12_to_16_distr = arrival_12_to_16_distr
        self.arrival_16_to_22_distr = arrival_16_to_22_distr
        self.products_distr = products_distr

        