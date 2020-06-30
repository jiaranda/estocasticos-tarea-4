class Cashier:
    def __init__(self, attention_10_to_14_distr, attention_14_to_20_distr, attention_20_to_22_distr):
        self.attention_10_to_14_distr = attention_10_to_14_distr
        self.attention_14_to_20_distr = attention_14_to_20_distr
        self.attention_20_to_22_distr = attention_20_to_22_distr
        self.time_free = 0

    def client_ready_time(self, time, client):
        if 60 * 60 * 10 <= time <= 60 * 60 * 14:
            time_per_product = self.attention_10_to_14_distr()
        elif 60 * 60 * 14 < time <= 60 * 60 * 20:
            time_per_product = self.attention_14_to_20_distr()
        elif 60 * 60 * 20 < time <= 60 * 60 * 22:
            time_per_product = self.attention_20_to_22_distr()

        res = time
        for _ in range(client.products_qty):
            res += time_per_product()
        return res
