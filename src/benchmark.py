from data.models import create_model
from algorithms.nearest_neighbor import nearest_neighbor
from algorithms.two_opt import two_opt
from algorithms.guided_local_search import guided_local_search
from algorithms.tabu_search import tabu_search
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


def test_guided_local_search(model):
  """
  Returns routes, total distance and execution time of guided local search algorithm
  """
  start = time.perf_counter_ns()
  manager, routing, solution = guided_local_search(model)
  end = time.perf_counter_ns()
  exec_time = (end - start) / 1000000000
  distance = calc_total_distance_ortools(model["num_vehicles"], routing, solution)
  return distance, exec_time


def test_tabu_search(model):
  """
  Returns routes, total distance and execution time of tabu search algorithm
  """
  start = time.perf_counter_ns()
  manager, routing, solution = tabu_search(model)
  end = time.perf_counter_ns()
  exec_time = (end - start) / 1000000000
  distance = calc_total_distance_ortools(model["num_vehicles"], routing, solution)

  return distance, exec_time


def test_small_map():
  """
  Test a series of small maps with 10 points and 2 vehicles with the same capacity
	"""
  model, coords = create_model(50,10,2,[5,10])

  nn_routes, nn_distance, nn_time = test_nearest_neighbour(model)
  to_routes, to_distance, to_time = test_two_opt(model, nn_routes, 1000)
  rand_routes, rand_distance, rand_time = test_random(model)
  to_rand_routes, to_rand_distance, to_rand_time = test_two_opt(model, rand_routes, 1000)
  gls_distance, gls_time = test_guided_local_search(model)
  ts_distance, ts_time = test_tabu_search(model)

  # temporary print mess, ideally we save to CSV or something?
  print("""
        Nearest Neighbour:
        \tDistance: {nndist}
        \tTime: {nntime}
        Two-Opt (NN):
        \tDistance: {todist}
        \tTime: {totime}
        Random:
        \tDistance: {randdist}
        \tTime: {randtime}
        Two-Opt (rand):
        \tDistance: {torandomdist}
        \tTime: {torandomtime}
        Guided Local Search:
        \tDistance: {glsdistance}
        \tTime: {glstime}
        Tabu Search:
        \tDistance: {tsdistance}
        \tTime: {tstime}
        """.format(
          nndist=nn_distance,
          nntime=nn_time,
          todist=to_distance,
          totime=to_time,
          randdist=rand_distance,
          randtime=rand_time,
          torandomdist=to_rand_distance,
          torandomtime=to_rand_time,
          glsdistance=gls_distance,
          glstime=gls_time,
          tsdistance=ts_distance,
          tstime=ts_time
        ))


def benchmark_suite():
  """
  Run a series of tests on each algorithm and save the results
  """
  print('starting benchmarks...')
  test_small_map()
  print('benchmark suite complete.')



benchmark_suite()