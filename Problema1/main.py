from distributions import exponential_instance_generator, uniform_instance_generator
from cashier import Cashier

class Simulation:
    def __init__(self):
        self.time = 0
        self.system_capacity = None
        self.cashier1 = None
        self.cashier2 = None
        self.cashier3 = None
        self.clients_inside = list()
        self.clients_queue = list()
        # events
        self.clients_arrivals = list()
        self.clients_product_selection = list()
        self.cashier_ready = list()

    def prepare(self):
        print("Preparing Simulation")
        
        self.system_capacity = 30

        cashier1_params = {
            "attention_10_to_14_distr": uniform_instance_generator(5, 11),
            "attention_14_to_20_distr": uniform_instance_generator(10, 20),
            "attention_20_to_22_distr": uniform_instance_generator(10, 30)
        }
        self.cashier1 = Cashier(**cashier1_params)

        cashier2_params = {
            "attention_10_to_14_distr": exponential_instance_generator(1/6),
            "attention_14_to_20_distr": exponential_instance_generator(1/10),
            "attention_20_to_22_distr": exponential_instance_generator(1/15)
        }
        self.cashier2 = Cashier(**cashier2_params)

        cashier3_params = {
            "attention_10_to_14_distr": uniform_instance_generator(4, 16),
            "attention_14_to_20_distr": uniform_instance_generator(6, 18),
            "attention_20_to_22_distr": uniform_instance_generator(10, 22)
        }
        self.cashier3 = Cashier(**cashier3_params)

    def run(self):
        print("Running")

if __name__ == "__main__":
    simulation = Simulation()
    simulation.prepare()
    simulation.run()

        
