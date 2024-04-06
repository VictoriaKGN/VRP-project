from models import create_simple_data_model
import random

# solving VRP using Tabu search, a metaheuristic local search approximation algorithm.

def tabu_search():
	data = create_simple_data_model()
	init_sol = initial_solution(data)
	print("init random solution:\t", init_sol)

	

# provides the starting point for tabu search – a randomly chosen solution
# output: a 2d list, each vehicle has a list of locations visited
def initial_solution(data):
	distance_matrix = data["distance_matrix"]
	num_locations = len(distance_matrix) - 1
	remaining_locations = list(range(1,num_locations+1))
	locations_per_vehicle = num_locations // data["num_vehicles"]
	solution_matrix = []

	# randomly assign each vehicle an equal number of locations
	for i in range(data["num_vehicles"]):
		for j in range(locations_per_vehicle):
			# randomly sample an amount of the remaining locations to be visited by this vehicle
			visits = random.sample(remaining_locations, 1)
			# remove chosen locations from the list for next vehicles
			remaining_locations = [x for x in remaining_locations if x not in visits]
			solution_matrix.append(visits)
	
	return solution_matrix

def main():
	tabu_search()

if __name__ == "__main__":
	main()