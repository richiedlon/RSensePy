import os
import numpy as np
import cv2

from clip_withBB_function import clipRasterBB
from clip_withSHP_function import clipRasterSHP
from writeRasterFunction import writeRaster
from cloudMask_clip import cloud_mask_landsat8_clip
from get_filenames_Assign_Var import *
import matplotlib
import matplotlib.pyplot as plt
bbox = [13.490206, 48.3355,14.076421, 48.007881]

os.chdir('C://Studies//Copernicus Program//1_Semester 2//Software development practice//Final project')


geopy = L8("LC08_L2SP_191027_20220720_20220726_02_T1")
red_band = geopy.b4
nir_band = geopy.b5

shpLocation= "AOI/AOI.shp"
outputLocation1 = "output/NDVI4.tif"



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
geopy.NDVI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=False)
#geopy.NDVI(cloud=True, save_location=outputLocation1,bbcoord=bbox)