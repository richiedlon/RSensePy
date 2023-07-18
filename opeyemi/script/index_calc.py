''' 
This script is a preliminary version of index calculation python file for my final project
Currently contains 3 functions each implementing one index. 
Three indices currently represented are Normalized Vegetaion Index (ndvi), Enhanced Vegetation Index (evi), Normalised Water Index (ndwi)

It does not yet read the actual band values from actual imagery. It is just meant to show that the indices work.
Therefore, you only need specify the values either directly or assigned to variables.

Call the individual index functions, inputing the required args. 

e.g ndvi(nir, red)
    evi(nir, red, blue)
    ndwi(nir, green)

where,
	red: red band of your dataset
	nir: near infrared band of your dataset
	blue: blue band of your dataset	
	green: green band of your dataset

Dont forget to encase this in a print statement to actually see your results.

import this module to run the functions in any python enviroment

'''

import numpy as np
import rasterio
from rasterio import plot


# nir = 10
# red = 5
# blue = 2
# green = 4

##NDVI

def ndvi(nir, red):
    """
    *Normalized Difference Vegetation Index*
    args are nir (first position) and red(second position) values

	Formula
	ndvi = (nir-red)/(nir+red)
    """

    ndviVal = np.where((nir+red)==0., 0, # if nir plus red gives a fraction (0.), tranfrom to 0 
                    (nir-red)/(nir+red) #else, run this 
                    )
    return ndviVal


print(ndvi(nir, red))


##EVI

def evi(nir, red, blue, G = 2.5, L = 1, C1 = 6, C2 = 7.5 ):
    """
    *Enhance Vegetation Index*
    args are nir (first position) and red(second position) and blue (third position) values. 
    
	Optional params and default values
	G = 2.5,
	L = 1,
	C1 = 6,
	C2 = 7.5,

    Formula
	G * ((nir - red)/(nir + C1 * red - C2 * blue + L))
    
    """

    eviVal = np.where((nir+red)==0., 0,
                   G * ((nir - red)/(nir + C1 * red - C2 * blue + L))
                   )
    return eviVal

print(evi(nir, red, blue))


##NDWI

def ndwi(nir, green):
    """
    
    *Normalized Difference Water Index*
    args are nir (first position) and green(second position) values

	Formula
	(green - nir)/(green + nir)
    """

    ndwiVal = np.where((nir + green)==0., 0,
                    (green - nir)/(green + nir)
                    )
    return ndwiVal

print(ndwi(nir, green))



##NBR

def nbr(nir, swir):
    """
    *Normailized Burn Ratio*
    args are nir (first position) and green(second position) values

	Formula
	(nir - swir)/(nir + swir)
    """

    nbrVal = (nir - swir)/(nir + swir)
                    
    return nbrVal

print(nbr(nir, swir))



##NDBI

def ndbi(swir, nir):
    """
    *Normalized Difference Built-Up Index*
    args are swir (first position) and nir(second position) values

	Formula
	(swir - nir)/(swir + nir)
    
    """

    ndbiVal = (swir - nir)/(swir + nir)
                    
    return ndbiVal

print(nbr(swir, nir))



##GNDVI

def gndvi(nir, green):
    """
    *Normalized Difference Vegetation Index*
    args are nir (first position) and red(second position) values

	Formula
	ndvi = (nir-red)/(nir+red)
    """

    gndviVal = np.where((nir+green)==0., 0, # if nir plus green gives a fraction (0.), tranfrom to 0 
                    (nir-green)/(nir+green) #else, run this 
                    )
    return gndviVal


##GLI 

def gli(green, red, blue):
    """
    *Green Leaf Index*
    args are green (first position) and red(second position) and blue (thrid position) values

	Formula
	gli = (2*green - red - blue)/(2*green + red + blue)
    """

    gliVal = (2*green - red- blue)/(2*green + red + blue)
    
    return gliVal



##SAVI

def savi(nir, red, L=0.5):
    """
    *Soil Adjusted Vegetation Index*
    args are nir (first position) and red(second position) values

	Formula: ((1 + L) * (NIR - Red)) / (NIR + Red + L), 
    
    default L = 0.5
    """

    saviVal = ((1 + L) * (nir - red)) / (nir + red + L)

    return saviVal


##GSAVI

def gsavi(nir, green, L=0.5):
    """
    * Green Soil Adjusted Vegetation Index*
    args are nir (first position) and green(second position) values

	Formula: ((1 + L) * (NIR - Green)) / (NIR + Green + L), 
    
    L = 0.5
    """

    gsaviVal = ((1 + L) * (nir - green)) / (nir + green + L)

    return gsaviVal


##GCI 

def gci(nir, green, C=1):
    
    """
    *Green Chlorophyll Index (CI-green Or GCI)*
    args are nir (first position) and green(second position) values

    Formula:  nir / green-C.

    C = 1
    """

##R_ECI 

def r_eci(nir, redge, C=1):
    
    """
    Only for Sentinel 2

    *Red-Edge Chlorophyll Index (CI-Red_edge Or R-ECI)*
    args are nir (first position) and redge(second position) values

    Formula:  nir / redge-C.

    C = 1
    """




# ## Creating a geoimage from the calculated ndvi

# ndviImage = rasterio.open(r'opeyemi\output\ndviImage.tiff', 'w', driver='Gtiff',
#                         width= band4.width, height= band4.height, count=1, 
#                         crs= band4.crs, transform= band4.transform, dtype='float64')

# ## Writing the image to file (writen to output folder as specifed above...this folder should be created prior to running the code)

# ndviImage.write(ndvi,1)
# ndviImage.close()

