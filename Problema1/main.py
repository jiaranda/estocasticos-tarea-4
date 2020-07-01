import random
from distributions import exponential_instance_generator, uniform_instance_generator
from cashier import Cashier
from client import Client


# todo el tiempo sera manejado en segundos

class Simulation:
    def __init__(self):
        self.time = None
        self.end_time = None
        self.system_capacity = None
        self.cashier1 = None
        self.cashier2 = None
        self.cashier3 = None
        self.clients_inside = list()
        self.clients_queue = list()
        self.clients_lost = 0
        self.time_empty = 0
        self.queue_history = dict()
        # events
        self.clients_arrivals = list()
        self.clients_product_selection = list()
        self.cashier1_ready = None
        self.cashier2_ready = None
        self.cashier3_ready = None
        # params
        self.client_params = None

    def prepare(self):
        print("Preparing Simulation")

        self.time = 60 * 60 * 10 # 10:00:00, seconds from 00:00:00
        self.end_time = 60 * 60 * 22 # 22:00:00, seconds from 00:00:00
        self.system_capacity = 30 # clients inside

        self.client_params = {
            "arrival_10_to_12_distr": uniform_instance_generator(60 * 2, 60 * 3),
            "arrival_12_to_16_distr": exponential_instance_generator(60 / 60 / 60),
            "arrival_16_to_22_distr": uniform_instance_generator(60 * 1, 60 * 2),
            "products_qty_distr": uniform_instance_generator(1, 50),
            "products_ready_distr": exponential_instance_generator(1 / (5 * 60))
        }

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

    def generate_client(self):
        new_client = Client(**self.client_params)
        new_client.calculate_arrival_time(self.time)
        self.clients_arrivals.append(new_client)
        self.clients_arrivals.sort(key=lambda c: c.arrival_time)
        
    def get_possible_events(self):
        events = dict()
        if not (len(self.clients_arrivals) == 0):
            events["client_arrival"] = self.clients_arrivals[0].arrival_time
        if not (len(self.clients_product_selection) == 0):
            events["client_product_selection"] = self.clients_product_selection[0].products_ready_time
        if self.cashier1_ready:
            events["cashier1_ready"] = self.cashier1_ready
        if self.cashier2_ready:
            events["cashier2_ready"] = self.cashier2_ready
        if self.cashier3_ready:
            events["cashier3_ready"] = self.cashier3_ready
        return events

    def handle_client_arrival(self):
        client = self.clients_arrivals.pop(0)
        self.time = client.arrival_time
        client.calculate_products_ready_time(self.time)
        self.clients_product_selection.append(client)
        self.clients_product_selection.sort(key=lambda c: c.products_ready_time)
        self.generate_client()

    def handle_client_product_selection(self):
        client = self.clients_product_selection.pop(0)
        self.time = client.products_ready_time
        free_cashiers = list()
        if self.cashier1.current_client == None:
            free_cashiers.append(self.cashier1)
        if self.cashier2.current_client == None:
            free_cashiers.append(self.cashier2)
        if self.cashier3.current_client == None:
            free_cashiers.append(self.cashier3)

        if (len(free_cashiers) != 0): # no queue
            selected_cashier = random.choice(free_cashiers)
            selected_cashier.current_client = client
            selected_cashier.client_ready_time(self.time)
            



    def run(self):
        print("Running")
        while self.time <= self.end_time:
            # new client arrival
            if len(self.clients_arrivals) == 0:
                self.generate_client()
            # get next event
            events = self.get_possible_events()
            next_event = min(events, key=events.get)
            print(events)
            if next_event == "client_arrival":
                self.handle_client_arrival()
                print("arrival")
            elif next_event == "client_product_selection":
                self.handle_client_product_selection()
                print("selection")
    
            

        # debug
        # self.generate_client()
        # self.generate_client()
        # self.generate_client()
        # self.generate_client()
        # self.generate_client()
        # for c in self.clients_arrivals:
        #     print(c.arrival_time)


if __name__ == "__main__":
    simulation = Simulation()
    simulation.prepare()
    simulation.run()

        
