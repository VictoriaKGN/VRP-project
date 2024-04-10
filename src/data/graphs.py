import matplotlib.pyplot as plt

def draw_solution(coords, routes, title):
  """
  Draw the map with routes taken by vehicles as determined by a routing algorithm
  """
  x,y = draw_map(coords, title, False)
  # routes have location index, the graph location is x[loc_index], y[loc_index]
  # i have several plot calls to make (each route), but it looks like multiple things can be plotted at once
  if routes:
    for route in routes:
      route_coords = [[x[index], y[index]] for index in route]
      route_x, route_y = zip(*route_coords)
      plt.plot(route_x, route_y)
  plt.savefig('./src/data/figures/' + title + '.png')
  plt.close()


def draw_map(coords, title, save):
  """
  Draw the empty map showing the depot and locations. Saves to png if save parameter is True
  """
  x, y = zip(*coords)
  plt.scatter(x[:1], y[:1], marker = 's', color = 'red', label='depot')
  plt.scatter(x[1:],y[1:], label='location')
  plt.title(title)
  plt.legend()
  if save:
    plt.savefig('./src/data/figures/' + title + '_map.png')
    plt.close()
  return x, y