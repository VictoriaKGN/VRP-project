from data.models import create_model
from data.graphs import draw_solution, draw_map
from algorithms.nearest_neighbor import nearest_neighbor
from algorithms.two_opt import two_opt
from algorithms.guided_local_search import guided_local_search
from algorithms.tabu_search import tabu_search
import time
import numpy as np
import copy

def random_routes(data):
  """
  Returns a random assignment of routes to the vehicles
  """
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


def calc_route_distance(route, dist_matrix):
  """
  Calculate distance of a route taken by a vehicle
  For algorithms implemented by us
  """
  total_dist = 0
  num_locations = len(route)
    
  for i in range(num_locations - 1):
    curr_location = route[i]
    next_location = route[i + 1]
    total_dist += dist_matrix[curr_location][next_location]
  
  return total_dist


def calc_total_distance(routes, distance_matrix):
  """
  Calculate the total distance travelled by every vehicle
  For algorithms implemented by us
  """
  total = 0
  for route in routes:
    total += calc_route_distance(route, distance_matrix)
  return total


def calc_route_distance_ortools(routing, solution, vehicle_id):
  """
  Calculate distance of a route taken by a vehicle
  For algorithms implemented by OR-Tools
  """
  total_dist = 0
  index = routing.Start(vehicle_id)
    
  while not routing.IsEnd(index):
    previous_index = index
    index = solution.Value(routing.NextVar(index))
    total_dist += routing.GetArcCostForVehicle(
        previous_index, index, vehicle_id
    )
  
  return total_dist


def calc_total_distance_ortools(num_vehicles, routing, solution):
  """
  Calculate the total distance travelled by every vehicle
  For algorithms implemented by OR-Tools
  """
  total = 0
  for vehicle_id in range(num_vehicles):
    total += calc_route_distance_ortools(routing, solution, vehicle_id)
  return total


def get_routes_ortools(manager, routing, solution, num_vehicles):
  """
  Returns routes of OR-Tools algorithms
  """
  routes = []

  for vehicle_id in range(num_vehicles):
    vehicle_route = []
    index = routing.Start(vehicle_id)
    while not routing.IsEnd(index):
      node_index = manager.IndexToNode(index)
      vehicle_route.append(node_index)
      index = solution.Value(routing.NextVar(index))
    vehicle_route.append(manager.IndexToNode(index))
    routes.append(vehicle_route)

  return routes


def test_nearest_neighbour(model):
  """
  Returns routes, total distance and execution time of nearest neighbour algorithm
  """
  start = time.perf_counter_ns()
  routes = nearest_neighbor(model)
  end = time.perf_counter_ns()
  exec_time = (end - start) / 1000000000
  distance = calc_total_distance(routes, model['distance_matrix'])

  return routes, distance, exec_time


def test_random(model):
  """
  Returns routes, total distance and execution time of randomized algorithm
  """
  start = time.perf_counter_ns()
  routes = random_routes(model)
  end = time.perf_counter_ns()
  exec_time = (end - start) / 1000000000
  distance = calc_total_distance(routes, model['distance_matrix'])

  return routes, distance, exec_time


def test_two_opt(model, init_routes, iterations):
  """
  Returns routes, total distance and execution time of two-opt algorithm
  """
  start = time.perf_counter_ns()
  routes = two_opt(model, copy.deepcopy(init_routes), iterations)
  end = time.perf_counter_ns()
  exec_time = (end - start) / 1000000000
  distance = calc_total_distance(routes, model['distance_matrix'])

  return routes, distance, exec_time


def test_guided_local_search(model):
  """
  Returns routes, total distance and execution time of guided local search algorithm
  """
  start = time.perf_counter_ns()
  manager, routing, solution = guided_local_search(model)
  end = time.perf_counter_ns()
  exec_time = (end - start) / 1000000000
  distance = calc_total_distance_ortools(model["num_vehicles"], routing, solution)
  routes = get_routes_ortools(manager, routing, solution, model["num_vehicles"])

  return routes, distance, exec_time


def test_tabu_search(model):
  """
  Returns routes, total distance and execution time of tabu search algorithm
  """
  start = time.perf_counter_ns()
  manager, routing, solution = tabu_search(model)
  end = time.perf_counter_ns()
  exec_time = (end - start) / 1000000000
  distance = calc_total_distance_ortools(model["num_vehicles"], routing, solution)
  routes = get_routes_ortools(manager, routing, solution, model["num_vehicles"])

  return routes, distance, exec_time


def test_small_map():
  """
  Test a series of small maps with 10 points and 2 vehicles with the same capacity
	"""
  model, coords = create_model(50,10,2,[5,10])
  draw_map(coords, 'small', True)
  test_all_algorithms(model, coords, 'small_map')


def test_all_algorithms(model, coords, config_name):
  """
  Run each algorithm on the given model and save to PNG with the given config name
  """
  nn_routes, nn_distance, nn_time = test_nearest_neighbour(model)
  to_routes, to_distance, to_time = test_two_opt(model, nn_routes, 1000)
  rand_routes, rand_distance, rand_time = test_random(model)
  to_rand_routes, to_rand_distance, to_rand_time = test_two_opt(model, rand_routes, 1000)
  gls_routes, gls_distance, gls_time = test_guided_local_search(model)
  ts_routes, ts_distance, ts_time = test_tabu_search(model)

  draw_map(coords, config_name, True)
  draw_solution(coords, nn_routes, config_name + ' nearest neighbour')
  draw_solution(coords,to_routes, config_name + ' two-opt (NN)')
  draw_solution(coords, rand_routes, config_name + ' random solution')
  draw_solution(coords, to_rand_routes, config_name + ' two-opt (random input)')
  draw_solution(coords, gls_routes, config_name + ' guided local search')
  draw_solution(coords, ts_routes, config_name + ' tabu search')


def test_fleets(model, coords, fleet_ratio, total_demand, num_locations):
  """
  Test different fleet configurations on the same network of locations and demands
  """
  total_capacity = int(total_demand * 1.2) # introduce a buffer to the vehicle capacities
  for ratio in fleet_ratio:
    fleet_size = int(num_locations * ratio)
    split_capacity = total_capacity//fleet_size if total_capacity//fleet_size > 0 else 1
    model = change_fleet_config(model, fleet_size, [split_capacity]*fleet_size)
    test_all_algorithms(model, coords, '{x}V,{y}L,equal_capacity'.format(x=fleet_size,y=num_locations))


def test_fleet_configs_on_maps(fleet_ratios, location_counts):
  """
  Runs each algorithm on a set of maps. Tests multiple fleet configurations for each map.
  Each algorithm runs every combination of fleet size and location count.
  """
  total_demand = 1000
  for location_count in location_counts:
    print('testing {i} locations'.format(i=location_count))
    # initially created using 1 vehicle with total_demand capacity, modified in test_fleets
    model, coords = create_model(1000, location_count, 1, [total_demand])
    test_fleets(model, coords, fleet_ratios, total_demand, location_count)


def change_fleet_config(model, num_vehicles, capacities):
  model['num_vehicles'] = num_vehicles
  model['vehicle_capacities'] = capacities
  return model


def benchmark_suite():
  """
  Run a series of tests on each algorithm and save the results
  """
  print('starting benchmarks...')
  # this is the temporary code for debugging why or_tools is returning a None solution... hmm
  # model, coords = create_model(1000, 10, 5, [200]*5)
  # routes, distance, exec_time = test_guided_local_search(model)
  
  # This is the real test, different fleets and locations
  fleet_ratios = [0.75, 0.5, 0.25, 0.15]
  location_counts = [100]
  test_fleet_configs_on_maps(fleet_ratios, location_counts)
  print('benchmark suite complete.')


benchmark_suite()