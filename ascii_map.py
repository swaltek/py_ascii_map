import curses
from rasterio.transform import Affine
from rasterio import features

stdscr = curses.initscr()
curses.noecho()
stdscr.nodelay(True)

cols = curses.COLS
rows = curses.LINES

lngRes = (180 - -180) / cols
latRes = (-90 - 90) / rows
transform = Affine.translation(-180 - lngRes / 2, 90 - latRes / 2) * Affine.scale(lngRes, latRes) 

import geopandas as gpd
import numpy as np

geojson = gpd.read_file("./countries.geojson")
geom = [(shapes, 37) for (_ ,shapes) in enumerate(geojson.geometry)]

rasterized = features.rasterize(
        geom,
        out_shape = (rows,cols),
        fill = 32,
        out = None,
        transform = transform,
        all_touched = False,
        default_value = 31,
        dtype = np.dtype('i'))

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
                stdscr.addch(y, (x + offset) % cols, rasterized[y][x].item())
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

## Plot raster
#fig, ax = plt.subplots(1, figsize = (10, 10))
#show(rasterized, ax = ax)
##plt.gca().invert_yaxis()
#plt.show()
