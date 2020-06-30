class Cashier:
    def __init__(self, attention_10_to_14_distr, attention_14_to_20_distr, attention_20_to_22_distr):
        self.attention_10_to_14_distr = attention_10_to_14_distr
        self.attention_14_to_20_distr = attention_14_to_20_distr
        self.attention_20_to_22_distr = attention_20_to_22_distr