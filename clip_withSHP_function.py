import rasterio
from rasterio.plot import show
import os
import numpy as np
import matplotlib
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
import fiona
from fiona.crs import from_epsg
# import pycrs
from rasterio.crs import CRS
from writeRasterFunction import writeRaster

def clipRasterSHP(locationRaster,locationSHP):
	with fiona.open(locationSHP, "r") as shapefile:
		shapes = [feature["geometry"] for feature in shapefile]	
	with rasterio.open(locationRaster) as src:
		out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
		out_meta = src.meta
		epsg_code = int(src.crs.data['init'][5:])
	out_meta.update({"driver": "GTiff",
	                 "height": out_image.shape[1],
	                 "width": out_image.shape[2],
	                 "transform": out_transform,
	                 "count":1,
	                 "dtype":'float32',
	                 "crs": CRS.from_epsg(epsg_code)})

	return out_image,out_meta,epsg_code
