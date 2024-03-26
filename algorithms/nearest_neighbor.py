"""
Nearest Neighbor Algorithm
"""

import numpy as np

def nearest_neighbor(model):
  distance_matrix = model["distance_matrix"]
  num_vehicles = model["num_vehicles"]
  depot_index = model["depot"]

  num_locations = len(distance_matrix)
  visited = [False] * num_locations
  routes = []

  while np.sum(visited) < num_locations:
    current_node = 0
    route = [current_node]
    visited[current_node] = True