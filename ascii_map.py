from rasterio.transform import Affine
from rasterio import features
from rasterio.plot import show
cols = 80
rows = 60

lngRes = (180 - -180) / cols
latRes = (-90 - 90) / rows
transform = Affine.translation(-180 - lngRes / 2, 90 - latRes / 2) * Affine.scale(lngRes, latRes) 

import matplotlib.pyplot as plt
import geopandas as gpd

geojson = gpd.read_file("./countries.geojson")
geom = [shapes for shapes in geojson.geometry]

rasterized = features.rasterize(geom,
                                out_shape = (rows,cols),
                                fill = 0,
                                out = None,
                                transform = transform,
                                all_touched = False,
                                default_value = 1,
                                dtype = None)

# Plot raster
fig, ax = plt.subplots(1, figsize = (10, 10))
show(rasterized, ax = ax)
#plt.gca().invert_yaxis()
plt.show()
