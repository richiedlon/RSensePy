import app.RSensePy as ic
import os

# bbox = [7.429504,10.925490,7.522202,10.981428]
bbox = [13.490206, 48.3355, 14.076421, 48.007881]
# minx, miny = 13.490206, 48.3355
# maxx, maxy = 14.076421, 48.007881



#os.chdir('C://Users//xeon//SoftwareDevProject_ope')
os.chdir('C://Studies//Copernicus Program//1_Semester 2//Software development practice//Final project')


shpLocation= "AOI/AOI.shp"
outputLocation1 = "NBR1.tif"



geopy = ic.L8("LC08_L2SP_191027_20220720_20220726_02_T1")
geopyS2 = ic.S2("S2A_MSIL1C_20230806T055641_N0509_R091_T50XML_20230806T063042.SAFE")
#print(geopy.meta())
print(geopyS2.meta())

#ic.help()

# geopy.norm_dif(cloud=True, save_location=outputLocation1,shp_location=shpLocation, band1= geopy.b4, band2=geopy.b5, visualise=True)
# geopy.norm_dif(cloud=True, save_location=outputLocation1, bbcoord=bbox, band1= geopy.b4, band2=geopy.b5, visualise=True)
# geopy.NDVI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=True)
# geopy.NDVI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)

# geopy.EVI(cloud=False, save_location=outputLocation1,shp_location=shpLocation, visualise=True)
# geopy.EVI(cloud=False, save_location=outputLocation1,bbcoord=bbox, visualise=True)
# geopy.NDWI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=True)

# geopy.NBR(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=True)
# geopy.NDBI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)
# geopy.GNDVI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)
# geopy.GLI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=True)
# geopy.SAVI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)
# geopy.GSAVI(cloud=True, save_location=outputLocation1,bbcoord=bbox, visualise=True)
# geopy.GCI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=True)
# geopy.RECI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=True)
# geopy.VARI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=True)
# geopy.meta()

