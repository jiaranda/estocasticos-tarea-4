from simulation import Simulation
from distributions import exponential_instance_generator, uniform_instance_generator


# primera parte del problema 1
print("Primera parte del problema 1\n")
simulation = Simulation(
    client_params = {
            "arrival_10_to_12_distr": uniform_instance_generator(60 * 2, 60 * 3),
            "arrival_12_to_16_distr": exponential_instance_generator(1/60),
            "arrival_16_to_22_distr": uniform_instance_generator(60 * 1, 60 * 2),
            "products_qty_distr": uniform_instance_generator(1, 50),
            "products_ready_distr": exponential_instance_generator(1 / (5 * 60))
    },
    cashier1_params = {
            "attention_10_to_14_distr": uniform_instance_generator(5, 11),
            "attention_14_to_20_distr": uniform_instance_generator(10, 20),
            "attention_20_to_22_distr": uniform_instance_generator(10, 30)
    },
    cashier2_params = {
            "attention_10_to_14_distr": exponential_instance_generator(1/6),
            "attention_14_to_20_distr": exponential_instance_generator(1/10),
            "attention_20_to_22_distr": exponential_instance_generator(1/15)
    },
    cashier3_params = {
            "attention_10_to_14_distr": uniform_instance_generator(4, 16),
            "attention_14_to_20_distr": uniform_instance_generator(6, 18),
            "attention_20_to_22_distr": uniform_instance_generator(10, 22)
    }
)
simulation.run(100)
simulation.analytics()

# segunda parte del problema 1
print("\n\n\nSegunda parte del problema 1\n")
simulation = Simulation(
    client_params = {
            "arrival_10_to_12_distr": uniform_instance_generator(60 * 2, 60 * 3),
            "arrival_12_to_16_distr": exponential_instance_generator(1/60),
            "arrival_16_to_22_distr": uniform_instance_generator(60 * 1, 60 * 2),
            "products_qty_distr": uniform_instance_generator(1, 50),
            "products_ready_distr": exponential_instance_generator(1 / (5 * 60))
    },
    cashier1_params = {
            "attention_10_to_14_distr": exponential_instance_generator(1/5),
            "attention_14_to_20_distr": exponential_instance_generator(1/5),
            "attention_20_to_22_distr": exponential_instance_generator(1/5)
    },
    cashier2_params = {
            "attention_10_to_14_distr": exponential_instance_generator(1/5),
            "attention_14_to_20_distr": exponential_instance_generator(1/5),
            "attention_20_to_22_distr": exponential_instance_generator(1/5)
    },
    cashier3_params = {
            "attention_10_to_14_distr": exponential_instance_generator(1/5),
            "attention_14_to_20_distr": exponential_instance_generator(1/5),
            "attention_20_to_22_distr": exponential_instance_generator(1/5)
    }
)
simulation.run(100)
simulation.analytics()