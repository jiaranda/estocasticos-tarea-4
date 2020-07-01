class Client:
    def __init__(self, arrival_10_to_12_distr, arrival_12_to_16_distr, arrival_16_to_22_distr, products_qty_distr, products_ready_distr):
        self.arrival_10_to_12_distr = arrival_10_to_12_distr
        self.arrival_12_to_16_distr = arrival_12_to_16_distr
        self.arrival_16_to_22_distr = arrival_16_to_22_distr
        self.products_ready_distr = products_ready_distr
        self.products_qty = int(products_qty_distr())
        self.arrival_time = None
        self.products_ready_time = None
        self.time_started_queue = None
        self.time_ended_queue = None


    
    def calculate_arrival_time(self, time):
        print(time)
        if 60 * 60 * 10 <= time <= 60 * 60 * 12:
            t = time + self.arrival_10_to_12_distr()
        elif 60 * 60 * 12 < time <= 60 * 60 * 16:
            t = time + self.arrival_12_to_16_distr()
        elif 60 * 60 * 16 < time <= 60 * 60 * 22:
            t = time + self.arrival_16_to_22_distr()
        self.arrival_time = t
        return t
    
    def calculate_products_ready_time(self, time):
        t = time + self.products_ready_distr()
        self.products_ready_time = t
        return t
        

        