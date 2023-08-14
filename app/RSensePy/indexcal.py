import RSensePy
import os

os.chdir('C://Studies//Copernicus Program//1_Semester 2//Software development practice//Final project')

geopy = RSensePy.L8("LC08_L2SP_191027_20220720_20220726_02_T1") # Location of the landsat Image collection folder
red_band = geopy.b4
nir_band = geopy.b5


# minx, miny = 13.490206, 48.3355
# maxx, maxy = 14.076421, 48.007881
bbox = [13.490206, 48.3355,14.076421,48.007881]

shpLocation1= "AOI/AOI.shp"
shpLocation= "AOI/AOI.shp"
outputLocation1 = "output/NDVI4.tif"

#geopy.norm_dif(cloud=True, save_location=outputLocation1,shp_location=shpLocation, band1= geopy.b4, band2=geopy.b5, visualise=True)
#geopy.norm_dif(cloud=False, save_location=outputLocation1, bbcoord=bbox, band1= geopy.b4, band2=geopy.b5, visualise=True)
#geopy.NDVI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=False)
geopy.NDVI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)
geopy.meta()


"""S2 test code....no cloud masking function, and make sure your bbox is within your S2 image"""
# geopy.NDVI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.EVI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.NDRE(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.NDWI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.NBR(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.GNDVI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.GLI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.SAVI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.GSAVI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.GCI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.RECI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
# geopy.VARI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)