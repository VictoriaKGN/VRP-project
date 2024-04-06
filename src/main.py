import numpy as np
from data.models import create_6L2V_capacity_data_model
from algorithms.two_opt import two_opt
from algorithms.nearest_neighbor import nearest_neighbor
from algorithms.guided_local_search import guided_local_search
from algorithms.tabu_search import tabu_search
from benchmark import benchmark_suite, random_routes, calc_total_distance

def print_solution(data, manager, routing, solution):
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}\n")


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
print(f"Total distance travelled: {distance}\n")

print(f"Guided Local Search routes:")
manager, routing, solution = guided_local_search(model)
print_solution(model, manager, routing, solution)

print(f"Tabu Search routes:")
manager, routing, solution = tabu_search(model)
print_solution(model, manager, routing, solution)

benchmark_suite()