import numpy as np
from algorithms.models import create_6L2V_capacity_data_model
from algorithms.two_opt import two_opt
from algorithms.nearest_neighbor import nearest_neighbor
from algorithms.benchmark import benchmark_suite, random_routes, calc_total_distance

model = create_6L2V_capacity_data_model()

routes = nearest_neighbor(model)
print("Nearest Neighbor routes:")
distance = calc_total_distance(routes)
print(f"Total distance travelled: {distance}\n")

init_solution = random_routes(model)
print(f"Randomized routes:")
init_distance = calc_total_distance(init_solution)
print(f"Total distance travelled: {init_distance}\n")


routes = two_opt(model, init_solution, 1000)
print("Two-Opt routes:")
distance = calc_total_distance(routes)
print(f"Total distance travelled: {distance}")

benchmark_suite()