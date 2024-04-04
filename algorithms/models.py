"""
Data models - serve as inputs to routing algorithms.
Each model contains a distance matrix, number of vehicles, and the depot location.
"""

import math

def create_simple_data_model():
  """ 
  Returns a simple data model with 4 locations and 1 vehicle 
  The locations form a square with the depot in the center, each location is 1 distance from the depot
  """

  dist = math.sqrt(2)

  data = {}
  data["distance_matrix"] = [
    [0, 1, 1, 1, 1],          # depot
    [1, 0, dist, dist, 2],    # location 1
    [1, dist, 0, 2, dist],    # location 2
    [1, dist, 2, 0, dist],    # location 3
    [1, 2, dist, dist, 0],    # location 4
  ]
  data["num_vehicles"] = 1
  data["depot"] = 0
  return data


def create_simple_capacity_data_model():
  """ 
  Returns a simple capacitated data model with 4 locations and 1 vehicle with a capacity
  The locations form a square with the depot in the center, each location is 1 distance from the depot
  """
  
  dist = math.sqrt(2)

  data = {}
  data["distance_matrix"] = [
    [0, 1, 1, 1, 1],          # depot
    [1, 0, dist, dist, 2],    # location 1
    [1, dist, 0, 2, dist],    # location 2
    [1, dist, 2, 0, dist],    # location 3
    [1, 2, dist, dist, 0],    # location 4
  ]
  data["num_vehicles"] = 1
  data["demands"] = [0, 1, 2, 3]
  data["vehicle_capacities"] = [4]
  data["depot"] = 0
  return data