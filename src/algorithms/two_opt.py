"""
Two-Opt Optimization Algorithm
"""

import numpy as np

def two_opt(model, routes, num_iterations):
  def calc_total_distance(route, dist_matrix):
    total_dist = 0
    num_locations = len(route)
    
    for i in range(num_locations - 1):
      curr_location = route[i]
      next_location = route[i + 1]
      total_dist += dist_matrix[curr_location][next_location]
      
    return total_dist
  
  def two_opt_solver(model, routes, num_iterations):
    distance_matrix = model["distance_matrix"]
    best_routes = routes.copy()
    
    for _ in range(num_iterations):
      selected_route_index = np.random.randint(0, len(routes))
      selected_route = routes[selected_route_index]
      
      i, j = np.random.randint(1, len(selected_route) - 1, size=2)
      if j < i:
        i, j = j, i
        
      new_route = selected_route.copy()
      new_route[i:j] = selected_route[j - 1: i - 1: -1]
      
      new_routes = routes.copy()
      new_routes[selected_route_index] = new_route
      
      if calc_total_distance(new_routes[selected_route_index], distance_matrix) < calc_total_distance(best_routes[selected_route_index], distance_matrix):
        best_routes = new_routes
        
    return best_routes
  
  for i in range(len(routes)):
    route = routes[i]
    optimized_route = two_opt_solver(model, [route], num_iterations)[0]
    routes[i] = optimized_route
    
  return routes