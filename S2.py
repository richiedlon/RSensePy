import os
import os.path
import sys
import numpy as np
from clip_withBB_function import clipRasterBB
from clip_withSHP_function import clipRasterSHP
from writeRasterFunction import writeRaster
from cloudMask_clip import cloud_mask_landsat8_clip
from cloudMask_clip import cloud_mask_landsat8_clip_shp
import matplotlib
import matplotlib.pyplot as plt


# SENTINEL 2 IMAGERY CLASS

class S2:
    def __init__(self, directory):
        BandNum = None
        QA_PIXEL, B1, B2, B3, B4, B5, B6, B7 = None, None,None,None,None,None,None, None

        directory = "C:\\Users\\xeon\\SoftwareDevProject_ope\\S2A_MSIL2A_20230715T135711_N0509_R067_T21LWD_20230715T212203.SAFE\\GRANULE\\L2A_T21LWD_A042106_20230715T140007\\IMG_DATA\\R20m"
        tif_files = []

        try:
            for file in os.listdir(directory):
                if file.endswith(".jp2"):
                    tif_files.append(file)
        except Exception:
            print("Image Collection directory path is invalid")
            sys.exit()

        print(tif_files)

        # assign the appropriate files to their respective band variables

        for item in tif_files:
            BandNum = item[-11:-8]
            if BandNum == "BO1":
                B1=item
            elif BandNum=='BO2':
                B2=item
            elif BandNum=='BO3':
                B3=item
            elif BandNum=='BO4':
                B4=item
            elif BandNum=='BO5':
                B5=item
            elif BandNum=='BO6':
                B6=item
            elif BandNum=='BO7':
                B7=item
            elif BandNum=='B8A':
                B8A=item
            elif BandNum=='B11':
                B11=item
            elif BandNum=='B12':
                B12=item
            elif BandNum=='SCL':
                SCL=item
            elif BandNum=='TCI':
                TCI=item
            elif BandNum=='WVP':
                WVP=item
    
        self.B1= directory+"\\"+B1
        self.B2= directory+"\\"+B2
        self.B3= directory+"\\"+B3
        self.B4= directory+"\\"+B4
        self.B5= directory+"\\"+B5
        self.B6= directory+"\\"+B6
        self.B7= directory+"\\"+B7
        self.B8A= directory+"\\"+B8A
        self.B11= directory+"\\"+B11
        self.B12= directory+"\\"+B12
        self.SCL= directory+"\\"+SCL
        self.TCI= directory+"\\"+TCI
        self.WVP= directory+"\\"+WVP

