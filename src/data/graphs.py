import matplotlib.pyplot as plt

def draw_solution(coords, routes, title):
  x, y = zip(*coords)
  plt.scatter(x[:1], y[:1], marker = 's', color = 'red', label='depot')
  plt.scatter(x[1:],y[1:], label='location')
  plt.title(title)
  plt.legend()
  # routes have location index, the graph location is x[loc_index], y[loc_index]
  # i have several plot calls to make (each route), but it looks like multiple things can be plotted at once
  for route in routes:
    route_coords = [[x[index], y[index]] for index in route]
    route_x, route_y = zip(*route_coords)
    plt.plot(route_x, route_y)
  plt.show()