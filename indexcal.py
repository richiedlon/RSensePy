import os
import numpy as np
import cv2
from default_modules import *
from clip_withBB_function import clipRasterBB
from clip_withSHP_function import clipRasterSHP
from writeRasterFunction import writeRaster
from cloudMask_clip import cloud_mask_landsat8_clip
# from get_filenames_Assign_Var import *
import matplotlib
import matplotlib.pyplot as plt
bbox = [7.429504,10.925490,7.522202,10.981428]

os.chdir('C://Users//xeon//SoftwareDevProject_ope')

# # NDVI Test
# geopy = L8("LC09_L2SP_189053_20230412_20230414_02_T1")
# red_band = geopy.b4
# nir_band = geopy.b5

# shpLocation= "AOI/AOI.shp"
# outputLocation1 = "NDVI5.tif"

# # EVI Test
# geopy = L8("LC09_L2SP_189053_20230412_20230414_02_T1")
# red_band = geopy.b4
# nir_band = geopy.b5
# blue_band = geopy.b2

# shpLocation= "AOI/AOI.shp"
# outputLocation1 = "EVI1.tif"

# # NBR Test
# geopy = L8("LC09_L2SP_189053_20230412_20230414_02_T1")
# swir_band = geopy.b6
# nir_band = geopy.b5


# shpLocation= "AOI/AOI.shp"
# outputLocation1 = "NBR1.tif"


# NDBI Test
geopy = L8("LC09_L2SP_189053_20230412_20230414_02_T1")
swir_band = geopy.b6
nir_band = geopy.b5


shpLocation= "AOI/AOI.shp"
outputLocation1 = "NBDI1.tif"


# minx, miny = 13.490206, 48.3355
# maxx, maxy = 14.076421, 48.007881

# def calculate_ndvi(red_band, nir_band):
# 	red_band = red_band.astype(np.float32)
# 	nir_band = nir_band.astype(np.float32)
# 	numerator = nir_band - red_band
# 	denominator = nir_band + red_band
# 	ndvi = numerator / denominator
# 	return ndvi

# red=clipRasterSHP(red_band,shpLocation)
# nir=clipRasterSHP(nir_band,shpLocation)

# ndvi_result = calculate_ndvi(red[0], nir[0])


# print(red[1])
# print(nir[1])
# writeRaster(ndvi_result,nir[1],outputLocation1)

#geopy.norm_dif(cloud=True, save_location=outputLocation1,shp_location=shpLocation, band1= geopy.b4, band2=geopy.b5)
#geopy.norm_dif(cloud=False, save_location=outputLocation1, bbcoord=bbox, band1= geopy.b4, band2=geopy.b5)
#geopy.NDVI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=False)
#geopy.NDVI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)
#geopy.EVI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)
#geopy.NDWI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)
#geopy.NBR(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)
geopy.NDBI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)