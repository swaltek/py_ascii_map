from libpysal import weights
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gp
import numpy as np

gdf = gp.read_file("countries.geojson")

rep_p = gdf.representative_point()
centroids = np.column_stack((rep_p.x, rep_p.y))

neighbors = {}
for index, country in gdf.iterrows():
    touches = np.array(gdf[gdf.geometry.touches(country['geometry'])].index)
    overlaps = np.array(gdf[gdf.geometry.overlaps(country['geometry'])].index)
    n = np.union1d(touches, overlaps)
    neighbors[index] = n.tolist()

weights = weights.W(neighbors, silence_warnings=True)
graph = weights.to_networkx()

positions = dict(zip(graph.nodes, centroids))

colors_map = nx.coloring.greedy_color(graph)

color_map_s = [v for _, v in sorted(colors_map.items())]
colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF"]
node_colors = [colors[i] for i in color_map_s]

plot = gdf.plot(linewidth=1, edgecolor="grey", facecolor="lightblue")

#x, y = zip(*centroids)
#graph.scatter(x, y)
nx.draw(graph, positions, plot, node_size=5, node_color=node_colors)
plt.show()
