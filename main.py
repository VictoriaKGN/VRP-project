import numpy as np
from algorithms.models import create_6L2V_capacity_data_model
from algorithms.two_opt import two_opt
from algorithms.nearest_neighbor import nearest_neighbor


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
print(f"Total distance travelled: {distance}")