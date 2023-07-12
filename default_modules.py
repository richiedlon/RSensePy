import os
import numpy as np
import cv2
from clip_withBB_function import clipRasterBB
from clip_withSHP_function import clipRasterSHP
from writeRasterFunction import writeRaster
from cloudMask_clip import cloud_mask_landsat8_clip
from cloudMask_clip import cloud_mask_landsat8_clip_shp
import matplotlib
import matplotlib.pyplot as plt

class L8:
	def __init__(self,directory):
		BandNum = None
		QA_PIXEL, B1, B2, B3, B4, B5, B6, B7 = None, None,None,None,None,None,None, None
		tif_files = []

		for file in os.listdir(directory):
			if file.endswith(".TIF"):
				tif_files.append(file)
		for item in tif_files:
			BandNum = item[-9:-4]
			if BandNum=='PIXEL':
				QA_PIXEL =item
			elif BandNum=='SR_B1':
				B1=item
			elif BandNum=='SR_B2':
				B2=item
			elif BandNum=='SR_B3':
				B3=item
			elif BandNum=='SR_B4':
				B4=item
			elif BandNum=='SR_B5':
				B5=item
			elif BandNum=='SR_B6':
				B6=item
			elif BandNum=='SR_B7':
				B7=item
		self.qa_pixel=directory+"//"+QA_PIXEL
		self.b1=directory+"//"+B1
		self.b2=directory+"//"+B2
		self.b3=directory+"//"+B3
		self.b4=directory+"//"+B4
		self.b5=directory+"//"+B5
		self.b6=directory+"//"+B6
		self.b7=directory+"//"+B7
	def normalized_difference(self, band1, band2):
		band1 = band1.astype(np.float32)
		band2 = band2.astype(np.float32)
		numerator = band1 - band2
		denominator = band1 + band2
		normDifVal = numerator / denominator
		return normDifVal
	#def meta_data()

	def visualiseFunc(self, normDifVal):
		plt.figure(figsize=(10, 10))
		plt.imshow(normDifVal.squeeze(), cmap='gray')
		plt.title('Cloud Mask')
		plt.colorbar()
		plt.show()

	def norm_dif(self, cloud, save_location, shp_location=None, bbcoord=None, band1=None, band2=None, visualise=False):		
		if cloud ==False and (bbcoord is None):
			band1_clipped=clipRasterSHP(band1,shp_location)
			band2_clipped=clipRasterSHP(band2,shp_location)
			normDifVal = self.normalized_difference(band1_clipped[0], band2_clipped[0])
			writeRaster(normDifVal,band1_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			band1_clipped=clipRasterBB(band1,bbcoord)
			band2_clipped=clipRasterBB(band2,bbcoord)
			normDifVal = self.normalized_difference(band1_clipped[0], band2_clipped[0])
			writeRaster(normDifVal,band1_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			band1_clipped=clipRasterSHP(band1,shp_location)
			band2_clipped=clipRasterSHP(band2,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			normDifVal = self.normalized_difference(band1_clipped[0], band2_clipped[0])
			print("normDifVal calculation completed")
			normDifVal = np.multiply(normDifVal,cloudMask[0])
			writeRaster(normDifVal,band1_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			band1_clipped=clipRasterBB(band1,bbcoord)
			print("band1_clipped calculation completed")
			band2_clipped=clipRasterBB(band2,bbcoord)
			print("band2_clipped calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			normDifVal = self.normalized_difference(band1_clipped[0], band2_clipped[0])
			print("normDifVal calculation completed")
			normDifVal = np.multiply(normDifVal,cloudMask[0])
			writeRaster(normDifVal,band1_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseFunc(normDifVal)


	def NDVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.norm_dif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, band1 = self.b4, band2=self.b5)



