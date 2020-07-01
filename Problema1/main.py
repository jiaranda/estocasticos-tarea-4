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
        self.queue_history = list()
        self.clients_ready = 0
        self.system_history = list()
        # events
        self.clients_arrivals = list()
        self.clients_product_selection = list()
        self.cashier1_ready = None
        self.cashier2_ready = None
        self.cashier3_ready = None
        # params
        self.client_params = None
        # analytics
        self.clients_per_day = list()
        self.time_in_queue = list()
        self.queue_length_per_day = list()
        self.system_empty_per_day = list()


    def prepare(self):
        self.time = 60 * 60 * 10 # 10:00:00, seconds from 00:00:00
        self.end_time = 60 * 60 * 22 # 22:00:00, seconds from 00:00:00
        self.system_capacity = 30 # clients inside

        self.queue_history.append({
            "from": self.time,
            "length": 0
        })

        self.system_history.append({
            "from": self.time,
            "qty": 0
        })

        self.client_params = {
            "arrival_10_to_12_distr": uniform_instance_generator(60 * 2, 60 * 3),
            "arrival_12_to_16_distr": exponential_instance_generator(1/60),
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
        if self.cashier1.client_ready_time != None:
            events["cashier1_ready"] = self.cashier1.client_ready_time
        if self.cashier2.client_ready_time != None:
            events["cashier2_ready"] = self.cashier2.client_ready_time
        if self.cashier3.client_ready_time != None:
            events["cashier3_ready"] = self.cashier3.client_ready_time
        return events

    def handle_client_arrival(self):
        client = self.clients_arrivals.pop(0)
        self.time = client.arrival_time
        if len(self.clients_inside) == self.system_capacity:
            self.clients_lost += 1
            self.generate_client()
        else:
            client.calculate_products_ready_time(self.time)
            self.clients_product_selection.append(client)
            self.clients_product_selection.sort(key=lambda c: c.products_ready_time)
            self.clients_inside.append(client)

            self.system_history[-1]["to"] = self.time
            self.system_history.append({
                "from": self.time,
                "qty": len(self.clients_inside)
            })

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
            selected_cashier.calculate_client_ready_time(self.time)

        
        else: # all cashiers busy, go to the queue
            client.time_started_queue = self.time
            self.clients_queue.append(client)
            self.queue_history[-1]["to"] = self.time
            self.queue_history.append({
                "from": self.time,
                "length": len(self.clients_queue)
            })
            
    def handle_cashier_ready(self, cashier):
        self.time = cashier.client_ready_time
        self.clients_inside.remove(cashier.current_client)
        cashier.client_ready()
        self.clients_ready += 1

        self.system_history[-1]["to"] = self.time
        self.system_history.append({
            "from": self.time,
            "qty": len(self.clients_inside)
        })

        if len(self.clients_queue) != 0:
            client = self.clients_queue.pop(0)
            client.time_ended_queue = self.time

            self.queue_history[-1]["to"] = self.time
            self.queue_history.append({
                "from": self.time,
                "length": len(self.clients_queue)
            })

            self.time_in_queue.append(client.time_ended_queue - client.time_started_queue)
            free_cashiers = list()
            if self.cashier1.current_client == None:
                free_cashiers.append(self.cashier1)
            if self.cashier2.current_client == None:
                free_cashiers.append(self.cashier2)
            if self.cashier3.current_client == None:
                free_cashiers.append(self.cashier3)

            selected_cashier = random.choice(free_cashiers)
            selected_cashier.current_client = client
            selected_cashier.calculate_client_ready_time(self.time)
    
    def reset_simulation(self):
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
        self.queue_history = list()
        self.clients_ready = 0
        # events
        self.clients_arrivals = list()
        self.clients_product_selection = list()
        self.cashier1_ready = None
        self.cashier2_ready = None
        self.cashier3_ready = None
        # params
        self.client_params = None


    def run(self, number_of_simulations):
        for _ in range(number_of_simulations):
            self.reset_simulation()
            self.prepare()
            # generate first client
            self.generate_client()
            while self.time <= self.end_time:
                # get next event
                events = self.get_possible_events()
                next_event = min(events, key=events.get)
                if events[next_event] > self.end_time:
                    break
                if next_event == "client_arrival":
                    self.handle_client_arrival()
                    
                elif next_event == "client_product_selection":
                    self.handle_client_product_selection()
                    
                elif next_event in ["cashier1_ready", "cashier2_ready", "cashier3_ready"]:
                    if next_event == "cashier1_ready":
                        cashier = self.cashier1
                    elif next_event == "cashier2_ready":
                        cashier = self.cashier2
                    elif next_event == "cashier3_ready":
                        cashier = self.cashier3
                    self.handle_cashier_ready(cashier)
            
            # clients per day
            self.clients_per_day.append(self.clients_ready)

            # queue length mean per day
            length_sum = 0
            time_sum = 0
            for reg in self.queue_history:
                if reg.get("to") and reg.get("from"):
                    t = reg["to"] - reg["from"]
                    time_sum += t
                    length_sum += t * reg["length"]
            self.queue_length_per_day.append(length_sum/time_sum)

            # time with 0 clients
            time_sum = 0
            for reg in self.system_history:
                if reg.get("to") and reg.get("from") and reg["qty"] == 0:
                    t = reg["to"] - reg["from"]
                    time_sum += t
            self.system_empty_per_day.append(time_sum)


    
    def analytics(self):
        print("a) Cantidad de clientes atendidos en en un día promedio")
        # print(self.clients_per_day)
        res = sum(self.clients_per_day)/len(self.clients_per_day)
        print(f'{res} clientes')

        print("b) Tiempo promedio de un cliente en la cola")
        time_in_seconds = sum(self.time_in_queue) / len(self.time_in_queue)
        time_in_minutes = time_in_seconds / 60
        res = round(time_in_minutes, 3)
        print(f'{res} minutos')

        print("c) Largo promedio de la cola en un dia cualquiera")
        res = round(sum(self.queue_length_per_day) / len(self.queue_length_per_day), 3)
        print(f'{res} clientes')

        print("d) Tiempo en el que la tienda esta vacia en un dia promedio")
        res = sum(self.system_empty_per_day) / len(self.system_empty_per_day)
        res = round(res / 60, 3)
        print(f'{res} minutos')


if __name__ == "__main__":
    simulation = Simulation()
    simulation.run(100)
    simulation.analytics()

        
