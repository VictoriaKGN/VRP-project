"""
Guided Local Search Algorithm
Uses OR-Tools 
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def guided_local_search(data):
  manager = pywrapcp.RoutingIndexManager(len(data["distance_matrix"]), data["num_vehicles"], data["depot"])
  routing = pywrapcp.RoutingModel(manager)

  def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data["distance_matrix"][from_node][to_node]
  transit_callback_index = routing.RegisterTransitCallback(distance_callback)
  routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

  def demand_callback(from_index):
    from_node = manager.IndexToNode(from_index)
    return data["demands"][from_node]
  demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
  routing.AddDimensionWithVehicleCapacity(
    demand_callback_index,
    0,
    data["vehicle_capacities"],
    True,
    "Capacity"
  )

  search_parameters = pywrapcp.DefaultRoutingSearchParameters()
  search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
  )
  search_parameters.local_search_metaheuristic = (
    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
  )
  search_parameters.time_limit.FromSeconds(1)

  solution = routing.SolveWithParameters(search_parameters)
  return (manager, routing, solution)