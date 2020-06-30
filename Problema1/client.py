class Client:
    def __init__(self, arrival_10_to_12_distr, arrival_12_to_16_distr, arrival_16_to_22_distr, products_qty_distr, products_ready_distr):
        self.arrival_10_to_12_distr = arrival_10_to_12_distr
        self.arrival_12_to_16_distr = arrival_12_to_16_distr
        self.arrival_16_to_22_distr = arrival_16_to_22_distr
        self.products_ready_distr = products_ready_distr()
        self.products_qty = products_qty_distr()
    
    def arrival_time(self, time):
        if 60 * 60 * 10 <= time <= 60 * 60 * 12:
            return time + self.arrival_10_to_12_distr()
        elif 60 * 60 * 12 < time <= 60 * 60 * 16:
            return time + self.arrival_12_to_16_distr()
        elif 60 * 60 * 16 < time <= 60 * 60 * 22:
            return time + self.arrival_16_to_22_distr()
    
    def products_ready_time(self, time):
        return time + self.products_ready_distr()
        

        