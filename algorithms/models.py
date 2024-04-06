"""
Data models - serve as inputs to routing algorithms.
Each model contains a distance matrix, number of vehicles, and the depot location.
"""

import math
import random
from scipy.spatial import distance_matrix
import matplotlib.pyplot as plt
import numpy

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

def create_model(distance_scale, num_locations, num_vehicles, vehicle_capacities):
  """
  Returns a capacitated data model of n randomized locations and demands
  The vehicle count and capacities are passed as input, as these are commonly known ahead of time.
  Gets the distance matrix from random coordinates using Manhatthan distance (Minkowski distance with p-norm = 1)
  see: https://en.wikipedia.org/wiki/Minkowski_distance
  and https://en.wikipedia.org/wiki/Taxicab_geometry
  """
  data = {}
  data['num_vehicles'] = num_vehicles
  data['vehicle_capacities'] = vehicle_capacities
  data['depot'] = 0
  data['demands'] = assign_demand(num_locations, numpy.sum(vehicle_capacities))
  coords = generate_random_coordinates(distance_scale, num_locations)
  data['distance_matrix'] = distance_matrix(coords, coords, p=1, threshold=1000000)
  return data, coords

def generate_random_coordinates(distance_scale, num_locations):
  """
  Returns a list of num_locations coordinates
  """
  coords = []
  for _ in range(0,num_locations):
    x = random.randint(0,distance_scale)
    y = random.randint(0,distance_scale)
    coords.append([x,y])
  return coords

def assign_demand(num_locations, total_capacity):
  """
  Returns a list of demands corresponding to each location, equal to total vehicle capacity.
  Each location is guaranteed to have 1 demand, the rest are assigned at random
  """
  demand = [1]*num_locations
  if total_capacity > num_locations:
    for _ in range(num_locations, total_capacity):
      index = random.randint(0,num_locations-1)
      demand[index] += 1
  return demand


if __name__ == '__main__':
  print('quick test')
  data, coords = create_model(10,5,5,[1,2,3,4,5])
  print(data['distance_matrix'])
  # get the coordinate arrays and show them on a graph
  x, y = zip(*coords)
  plt.scatter(x,y)
  plt.show()