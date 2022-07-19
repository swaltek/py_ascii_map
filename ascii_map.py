from rasterio import features
from rasterio.transform import Affine
import curses
import geopandas as gpd
import libpysal as lps
import networkx as nx
import numpy as np

def calc_colors( gdf: gpd.GeoDataFrame ):

    neighbors = {}
    for index, country in gdf.iterrows():
        touches = np.array(gdf[gdf.geometry.touches(country['geometry'])].index)
        overlaps = np.array(gdf[gdf.geometry.overlaps(country['geometry'])].index)
        n = np.union1d(touches, overlaps)
        neighbors[index] = n.tolist()

    weights = lps.weights.W(neighbors, silence_warnings=True)
    graph = weights.to_networkx()

    colors_map = nx.coloring.greedy_color(graph)

    color_map_s = [v for _, v in sorted(colors_map.items())]
    colors = ["@", "%", "#", "&","$"]
    return [colors[i] for i in color_map_s]


stdscr = curses.initscr()
curses.noecho()
stdscr.nodelay(True)

cols = curses.COLS
rows = curses.LINES

lngRes = (180 - -180) / cols
latRes = (-90 - 90) / rows
transform = Affine.translation(-180 - lngRes / 2, 90 - latRes / 2) * Affine.scale(lngRes, latRes) 


gdf = gpd.read_file("./countries.geojson")
geom = [(shapes, index) for (index ,shapes) in enumerate(gdf.geometry)]

rasterized = features.rasterize(
        geom,
        out_shape = (rows,cols),
        fill = 255,
        out = None,
        transform = transform,
        all_touched = False,
        default_value = 0,
        dtype = np.dtype('i'))

colors = calc_colors( gdf )

offset = 0
while True:
    #check for escape key
    c = stdscr.getch()
    if c == ord('q'):
        break

    #place map on screen
    stdscr.clear()

    for y in range(0, rows):
        for x in range(0, cols):
            try:
                val = rasterized[y][x].item()
                char = ' ' if val == 255 else colors[rasterized[y][x].item()]
                stdscr.addch(y, (x + offset) % cols, char)
            except curses.error as _:
                #curses throws error when advancing character past end
                #lets ignore this error
                pass
    stdscr.refresh()


    # roll the map forward
    from time import sleep
    sleep(0.02)

    offset += 1

curses.endwin()
