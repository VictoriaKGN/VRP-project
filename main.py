import numpy as np
from algorithms.models import create_6L2V_capacity_data_model
from algorithms.two_opt import two_opt
from algorithms.nearest_neighbor import nearest_neighbor
from algorithms.guided_local_search import guided_local_search


def random_routes(data):
  distance_matrix = data["distance_matrix"]
  num_vehicles = data["num_vehicles"]
  num_locations = len(distance_matrix)
  depot_index = data["depot"]
  routes = [[] for _ in range(num_vehicles)]

  locations = list(range(num_locations))
  locations.remove(depot_index)
  np.random.shuffle(locations)

  for i, location in enumerate(locations):
    routes[i % num_vehicles].append(location)

  for route in routes:
    route.insert(0, depot_index)
    route.append(depot_index)

  return routes

def calc_total_distance(route, dist_matrix):
    total_dist = 0
    num_locations = len(route)
    
    for i in range(num_locations - 1):
      curr_location = route[i]
      next_location = route[i + 1]
      total_dist += dist_matrix[curr_location][next_location]
      
    return total_dist

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
    print(f"Total load of all routes: {total_load}")


model = create_6L2V_capacity_data_model()

routes = nearest_neighbor(model)
distance = 0
print("Nearest Neighbor routes:")
for route in routes:
  print(route)
  distance += calc_total_distance(route, model["distance_matrix"])
print(f"Total distance travelled: {distance}\n")

init_solution = random_routes(model)
init_distance = 0
print(f"Randomized routes:")
for route in init_solution:
  print(route)
  init_distance += calc_total_distance(route, model["distance_matrix"])
print(f"Total distance travelled: {init_distance}\n")

routes = two_opt(model, init_solution, 1000)
distance = 0
print("Two-Opt routes:")
for route in routes:
  print(route)
  distance += calc_total_distance(route, model["distance_matrix"])
print(f"Total distance travelled: {distance}\n")

manager, routing, solution = guided_local_search(model)
print_solution(model, manager, routing, solution)