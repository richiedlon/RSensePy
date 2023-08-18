import os
import app.RSensePy as rp


bboxs2 = [-56.963013,-15.392013,-56.783112,-15.225825]
# bbox = [7.429504,10.925490,7.522202,10.981428]
# bbox = [13.490206, 48.3355, 14.076421, 48.007881]
# minx, miny = 13.490206, 48.3355
# maxx, maxy = 14.076421, 48.007881

os.chdir('C://Users//xeon//SoftwareDevProject_ope')
# os.chdir('C://Studies//Copernicus Program//1_Semester 2//Software development practice//Final project')



# shpLocation= "AOI/AOI.shp"
outputLocation1 = "output/L8EVI.tif"


# geopy = rp.L8("LC09_L2SP_189053_20230412_20230414_02_T1")
geopy = rp.S2("S2A_MSIL2A_20230715T135711_N0509_R067_T21LWD_20230715T212203.SAFE")
# geopy = S2("S2A_MSIL2A_20230715T135711_N0509_R067_T21LWD_20230715T212203.SAFE")


# geopy.NDVI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
geopy.EVI(save_location=outputLocation1,bbcoord=bboxs2, visualise=True)
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

# geopy.norm_dif(cloud=True, save_location=outputLocation1,shp_location=shpLocation, band1= geopy.b4, band2=geopy.b5, visualise=True)
# geopy.norm_dif(cloud=True, save_location=outputLocation1, bbcoord=bbox, band1= geopy.b4, band2=geopy.b5, visualise=True)
# geopy.NDVI(cloud=True, save_location=outputLocation1,shp_location=shpLocation, visualise=True)z
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
# print(geopy.B1)

