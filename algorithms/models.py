"""
Data models - serve as inputs to routing algorithms.
Each model contains a distance matrix, number of vehicles, and the depot location.
"""

import math

def create_4L1V_data_model():
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


def create_4L1V_capacity_data_model():
  """ 
  Returns a capacitated data model with 4 locations and 1 vehicle with a capacity
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
  data["demands"] = [0, 1, 2, 3, 4]
  data["vehicle_capacities"] = [10]
  data["depot"] = 0
  return data

def create_6L2V_capacity_data_model():
  """ 
  Returns a capacitated data model with 6 locations and 2 vehicles with a capacities
  """
  
  data = {}
  data["distance_matrix"] = [
    [0,   2,   4,   6,   8,   10,  12],  # Depot
    [2,   0,   3,   5,   7,   9,   11],  # Location 1
    [4,   3,   0,   2,   4,   6,   8],   # Location 2
    [6,   5,   2,   0,   3,   5,   7],   # Location 3
    [8,   7,   4,   3,   0,   2,   4],   # Location 4
    [10,  9,   6,   5,   2,   0,   3],   # Location 5
    [12,  11,  8,   7,   4,   3,   0],   # Location 6
  ]
  data["num_vehicles"] = 2
  data["demands"] = [0, 2, 3, 6, 4, 5, 1]
  data["vehicle_capacities"] = [10, 15]
  data["depot"] = 0
  return data