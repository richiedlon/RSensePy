import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from clip_withBB_function import clipRasterBB
from clip_withSHP_function import clipRasterSHP
from writeRasterFunction import writeRaster
from cloudMask_clip import cloud_mask_landsat8_clip
from get_filenames_Assign_Var import *

os.chdir('C://Studies//Copernicus Program//1_Semester 2//Software development practice//Final project')
geopy = L8("LC08_L2SP_191027_20220720_20220726_02_T1")

locationRasterQA=geopy.qa_pixel
print(os.path.isfile(geopy.qa_pixel))


locationRasterTest=geopy.b5
print(os.path.isfile(geopy.b5))

outputLocation1 = "output//FInalCloudMaskCliped.tif"

shpLocation= "AOI/AOI.shp"
bbox = [13.490206, 48.3355,14.076421, 48.007881]

cloudMask = cloud_mask_landsat8_clip(locationRasterQA, bbox)

#clippedArea = clipRasterSHP(locationRasterTest,shpLocation)

clippedArea = clipRasterBB(locationRasterTest,bbox)

a = cloudMask[0]
b = clippedArea[0]
multiplied = np.multiply(a,b)

writeRaster(multiplied,clippedArea[1],outputLocation1)

print(cloudMask[0].shape)
print(clippedArea[0].shape)
plt.figure(figsize=(10, 10))
plt.imshow(multiplied.squeeze(), cmap='gray')

plt.title('Cloud Mask')
plt.colorbar()
plt.show()





