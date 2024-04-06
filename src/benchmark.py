from data.models import create_model
from algorithms.nearest_neighbor import nearest_neighbor
from algorithms.two_opt import two_opt
import time
import numpy as np

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
  calculate the total distance travelled by every vehicle
  """
  total = 0
  for route in routes:
    total += calc_route_distance(route, distance_matrix)
  return total


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


def test_two_opt(model, routes, iterations):
  """
  Returns routes, total distance and execution time of two-opt algorithm
  """
  start = time.perf_counter_ns()
  routes = two_opt(model, routes, iterations)
  end = time.perf_counter_ns()
  exec_time = (end - start) / 1000000000
  distance = calc_total_distance(routes, model['distance_matrix'])

  return routes, distance, exec_time


def test_small_map():
  """
  Test a series of small maps with 10 points and 2 vehicles with the same capacity
	"""
  model, coords = create_model(50,10,2,[5,10])

  nn_routes, nn_distance, nn_time = test_nearest_neighbour(model)
  to_routes, to_distance, to_time = test_two_opt(model, nn_routes, 1000)
  rand_solution = random_routes(model)
  to_rand_routes, to_rand_distance, to_rand_time = test_two_opt(model, rand_solution, 1000)

  # temporary print mess, ideally we save to CSV or something?
  print("""Nearest Neighbour:
        \tDistance: {nndist}
        \tTime: {nntime}
        Two-Opt (NN):
        \tDistance: {todist}
        \tTime: {totime}
        Two-Opt (rand):
        \tDistance: {torandomdist}
        \tTime: {torandomtime}
        """.format(
          nndist=nn_distance,
          nntime=nn_time,
          todist=to_distance,
          totime=to_time,
          torandomdist=to_rand_distance,
          torandomtime=to_rand_time
        ))


def benchmark_suite():
  """
  Run a series of tests on each algorithm and save the results
  """
  print('starting benchmarks...')
  test_small_map()
  print('benchmark suite complete.')