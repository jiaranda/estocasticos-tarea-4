class Cashier:
    def __init__(self, attention_10_to_14_distr, attention_14_to_20_distr, attention_20_to_22_distr):
        self.attention_10_to_14_distr = attention_10_to_14_distr
        self.attention_14_to_20_distr = attention_14_to_20_distr
        self.attention_20_to_22_distr = attention_20_to_22_distr
        self.time_free = 0
        self.current_client = None

    def client_ready_time(self, time):
        res = time
        for _ in range(self.current_client.products_qty):
            if 60 * 60 * 10 <= res <= 60 * 60 * 14:
                time_per_product = self.attention_10_to_14_distr()
            elif 60 * 60 * 14 < res <= 60 * 60 * 20:
                time_per_product = self.attention_14_to_20_distr()
            elif 60 * 60 * 20 < res <= 60 * 60 * 22:
                time_per_product = self.attention_20_to_22_distr()
            res += time_per_product
        return res
