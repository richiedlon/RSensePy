import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from clip_withBB_function import clipRasterBB
from clip_withSHP_function import clipRasterSHP
from writeRasterFunction import writeRaster

os.chdir('C://Studies//Copernicus Program//1_Semester 2//Software development practice//Final project')
locationRaster="LC08_L2SP_191027_20220720_20220726_02_T1/LC08_L2SP_191027_20220720_20220726_02_T1_QA_PIXEL.TIF"
shpLocation= "AOI/AOI.shp"
outputLocation1 = "output/CloudMaskCliped.tif"
outputLocation2 = "output/CloudMaskFull.tif"

def cloud_mask_landsat8_clip(image_path, locationSHP):
    minx, miny = 13.490206, 48.3355
    maxx, maxy = 14.076421, 48.007881

    resultTest=clipRasterSHP(image_path,locationSHP)
    #resultTest=clipRasterBB(locationRaster,minx,miny,maxx,maxy)

    qa_bandTest = resultTest[0]
    #Extract cloud and cloud shadow bits
    cloud_bit = 3
    cloud_shadow_bit = 4



    # valuetoTest = 21824
    # print("cloudValue "+ str(valuetoTest))
    # print("binary of valuetoTest ="+str(bin(valuetoTest)))
    # test1= np.right_shift(valuetoTest, cloud_bit)
    # print("np.right_shift value ")
    # print(test1)
    # print("np.right_shift value binary value")
    # print(bin(test1))
    # print("np.bitwise_and(np.right_shift(valuetoTest, cloud_bit), 1) ")
    # print(np.bitwise_and(test1, 1))
    # print("binary np.bitwise_and(test1, 1) ")
    # print(bin(np.bitwise_and(test1, 1)))

    # Create cloud mask based on confidence thresholds
    cloud_mask = np.bitwise_and(np.right_shift(qa_bandTest, cloud_bit), 1)
    cloud_shadow_mask = np.bitwise_and(np.right_shift(qa_bandTest, cloud_shadow_bit), 1)
    


    """
    The function applies the confidence thresholds to the cloud and cloud shadow masks. 
    It uses the bitwise right shift operator to shift the value 1 by the cloud and cloud 
    shadow bits and compares it to the QA band values. If the QA band value is greater 
    than or equal to the shifted value, the pixel is considered to have sufficient confidence 
    for cloud or cloud shadow detection. Otherwise, the pixel is set to 0 in the respective mask.
    """
    cloud_mask = np.where(qa_bandTest >= (1 << cloud_bit), cloud_mask, 0)
    cloud_shadow_mask = np.where(qa_bandTest >= (1 << cloud_shadow_bit), cloud_shadow_mask, 0)
    
    # Combine cloud and cloud shadow masks
    
    combined_mask = np.logical_or(cloud_mask, cloud_shadow_mask)
    print("Clip cloud mask shape - before squeeze \n")
    # print(combined_mask.shape)
    print(resultTest[1])
    print(combined_mask.shape)
    writeRaster(combined_mask,resultTest[1],outputLocation1)  
        
    #Plot the cloud mask
    # Need to squeeze before plotting

    plt.figure(figsize=(10, 10))
    plt.imshow(combined_mask.squeeze(), cmap='gray')
    plt.title('Cloud Mask')
    plt.colorbar()
    plt.show()    
    return combined_mask

combined = cloud_mask_landsat8_clip(locationRaster, shpLocation)

# print(combined.ndim)
# print(combined.shape)
# print(combined.size)
# print(combined.itemsize)