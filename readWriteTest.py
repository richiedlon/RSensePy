from clip_withBB_function import clipRasterBB
from clip_withSHP_function import clipRasterSHP
from writeRasterFunction import writeRaster
import os
os.chdir('C://Studies//Copernicus Program//1_Semester 2//Software development practice//Final project')


rasterLocation = "LC08_L2SP_191027_20220720_20220726_02_T1/LC08_L2SP_191027_20220720_20220726_02_T1_ST_B10.TIF"
shpLocation= "AOI/AOI.shp"
outputLocation1 = "output/MaskedTest3.tif"
outputLocation2 = "output/MaskedTest4.tif"


minx, miny = 13.490206, 48.3355
maxx, maxy = 14.076421, 48.007881

result1=clipRasterSHP(rasterLocation,shpLocation)
writeRaster(result1[0],result1[1],outputLocation1)

result2=clipRasterBB(rasterLocation,minx,miny,maxx,maxy)
writeRaster(result2[0],result2[1],outputLocation2)