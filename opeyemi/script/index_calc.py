import rasterio 
from rasterio import plot
import matplotlib.pyplot as plyt
import numpy as np


band4 = rasterio.open(r'relative\path\to\red\band') #red
band5 = rasterio.open(r'relative\path\tnir\band') #nir


## Check data type to confirm if it is float (Landsat values are originally in integer, but we need to calcluate ndvi in float)

# For band 4 
if band4.dtypes[0] != 'float64':
    red = band4.read(1).astype('float64') #Convert raster values from integer (int16) to float (float64)
else:
    red = band4.read(1)

#For band 5
if band5.dtypes[0] != 'float64':
    nir = band5.read(1).astype('float64') #Convert raster values from integer (int16) to float (float64)
else:
    nir = band5.read(1)


## NDVI caluclation using numpy

ndvi = np.where((nir+red)==0., 0, # if nir plus red gives a fraction (0.), tranfrom to 0 
                (nir-red)/(nir+red) #else, run this 
                )

#plot.show(ndvi) #plotting the final ndvi 


## Creating a geoimage from the calculated ndvi

ndviImage = rasterio.open(r'opeyemi\output\ndviImage.tiff', 'w', driver='Gtiff',
                        width= band4.width, height= band4.height, count=1, 
                        crs= band4.crs, transform= band4.transform, dtype='float64')

## Writing the image to file (writen to output folder as specifed above...this folder should be created prior to running the code)

ndviImage.write(ndvi,1)
ndviImage.close()


