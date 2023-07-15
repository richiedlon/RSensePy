from default_modules import *

os.chdir('C://Users//s1093356//OneDrive - Universität Salzburg//Documents//GitHub')

geopy = L8("LC08_L2SP_142055_20230529_20230607_02_T1") # Location of the landsat Image collection folder
red_band = geopy.b4
nir_band = geopy.b5


# minx, miny = 13.490206, 48.3355
# maxx, maxy = 14.076421, 48.007881
<<<<<<< HEAD
bbox = [13.490206, 48.3355,14.076421]
=======
bbox = [79.812069,6.896775,79.878330,6.967494]
>>>>>>> fcec42d001803c74d6f1991fbdbc8054b26f030e

shpLocation1= "AOI/AOI.shp"
shpLocation= "AOI/AOI.shp"
outputLocation1 = "output/NDVI4.tif"

#geopy.norm_dif(cloud=True, save_location=outputLocation1,shp_location=shpLocation, band1= geopy.b4, band2=geopy.b5, visualise=True)
<<<<<<< HEAD
#geopy.norm_dif(cloud=False, save_location=outputLocation1, bbcoord=bbox, band1= geopy.b4, band2=geopy.b5, visualise=True)
#geopy.NDVI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=True)
geopy.NDVI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=False)
=======
geopy.norm_dif(cloud=False, save_location=outputLocation1, bbcoord=bbox, band1= geopy.b4, band2=geopy.b5, visualise=True)
#geopy.NDVI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=False)
#geopy.NDVI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=False)
>>>>>>> fcec42d001803c74d6f1991fbdbc8054b26f030e
