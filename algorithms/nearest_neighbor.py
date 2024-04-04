"""
Nearest Neighbor Algorithm
"""

import numpy as np

def nearest_neighbor(model):
  distance_matrix = model["distance_matrix"]
  num_vehicles = model["num_vehicles"]
  demands = model["demands"]
  vehicle_capacities = model["vehicle_capacities"]
  depot_index = model["depot"]

  num_locations = len(distance_matrix)
  visited = np.zeros(num_locations, dtype=bool)
  routes = []
  
  for vehicle in range(num_vehicles):
    curr_location = depot_index
    capacity = vehicle_capacities[vehicle]
    curr_capacity = 0
    route = [curr_location]
    visited[curr_location] = True
    
    while curr_capacity +demands[curr_location] <= capacity:
      min_dist = float('inf')
      nearest = None
      
      for neighbor in np.where(~visited)[0]:
        if demands[neighbor] + curr_capacity <= capacity and distance_matrix[curr_location][neighbor] < min_dist:
          nearest = neighbor
          min_dist = distance_matrix[curr_location][neighbor]
          
      if nearest is None:
        break
      
      route.append(nearest)
      visited[nearest] = True
      curr_capacity += demands[nearest]
      
    routes.append(route)
    
  return routes