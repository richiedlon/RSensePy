import os
import os.path
import sys
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
		try:
			for file in os.listdir(directory):
				if file.endswith(".TIF"):
					tif_files.append(file)
		except Exception:
			print ("Error - Image Collection directory path is invalid")
			sys.exit()
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

		# NDVI
	def normalized_difference(self, nir, red):

		"""
		*Normalized Difference Vegetation Index*
		args are nir (first position) and red(second position) values

		Formula
		ndvi = (nir-red)/(nir+red)

		"""

		nir = nir.astype(np.float32)
		red = red.astype(np.float32)
		normDifVal = (nir - red) / (nir + red) #why the error
		return normDifVal
	

	def visualiseNDVI(self, normDifVal):
		plt.figure(figsize=(10, 10))
		plt.imshow(normDifVal.squeeze(), cmap='gray')
		plt.title('NDVI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED NDVI
	def norm_dif(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, red=None, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			normDifVal = self.normalized_difference(nir_clipped[0], red_clipped[0])
			writeRaster(normDifVal,nir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			red_clipped=clipRasterBB(red,bbcoord)
			normDifVal = self.normalized_difference(nir_clipped[0], red_clipped[0])
			writeRaster(normDifVal,nir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			normDifVal = self.normalized_difference(nir_clipped[0], red_clipped[0])
			print("normDifVal calculation completed")
			normDifVal = np.multiply(normDifVal,cloudMask[0])
			writeRaster(normDifVal,nir_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			red_clipped=clipRasterBB(red,bbcoord)
			print("red_clipped calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			normDifVal = self.normalized_difference(nir_clipped[0], red_clipped[0])
			print("normDifVal calculation completed")
			normDifVal = np.multiply(normDifVal,cloudMask[0])
			writeRaster(normDifVal,nir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseNDVI(normDifVal)

	
	def NDVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.norm_dif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, nir=self.b4, red=self.b5)


		

		#EVI
	def evi(self, nir, red, blue, G = 2.5, L = 1, C1 = 6, C2 = 7.5):
    
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

		nir = nir.astype(np.float32)
		red = red.astype(np.float32)
		blue = blue.astype(np.float32)
		eviValue = G * ((nir - red)/(nir + C1 * red - C2 * blue + L))
		return eviValue
			
	def visualiseEVI(self, eviValue):
		plt.figure(figsize=(10, 10))
		plt.imshow(eviValue.squeeze(), cmap='gray')
		plt.title('EVI')
		plt.colorbar()
		plt.show()


		# PARAMETERIZED EVI
	def evi_para(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, red=None, blue=None, G = 2.5, L = 1, C1 = 6, C2 = 7.5, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			blue_clipped=clipRasterSHP(blue,shp_location)
			eviValue = self.evi(nir_clipped[0], red_clipped[0], blue_clipped[0], G, L, C1, C2)
			writeRaster(eviValue,red_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			red_clipped=clipRasterBB(red,bbcoord)
			blue_clipped=clipRasterBB(blue,bbcoord)
			eviValue = self.evi(nir_clipped[0], red_clipped[0], blue_clipped[0], G, L, C1, C2)
			writeRaster(eviValue,red_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			print("nir_clipped calculation completed")
			red_clipped=clipRasterSHP(red,shp_location)
			print("red_clipped calculation completed")
			blue_clipped=clipRasterSHP(blue,shp_location)
			print("blue_clipped calculation completed")
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			eviValue = self.evi(nir_clipped[0], red_clipped[0], blue_clipped[0], G, L, C1, C2)
			print("eviValue calculation completed")
			eviValue = np.multiply(eviValue,cloudMask[0])
			writeRaster(eviValue,red_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			red_clipped=clipRasterBB(red,bbcoord)
			print("_clipped calculation completed")
			blue_clipped=clipRasterBB(blue,bbcoord)
			print("_clipped calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			eviValue = self.evi(nir_clipped[0], red_clipped[0], blue_clipped[0], G, L, C1, C2)
			print("eviValue calculation completed")
			eviValue = np.multiply(eviValue,cloudMask[0])
			writeRaster(eviValue,red_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseEVI(eviValue)

	
	def EVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.evi_para(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, red=self.b4, nir=self.b5, blue=self.b2)


		#NDWI
	def normWaterDif(self, green, nir):

		"""
		*Normalized Difference Water Index*
		args are nir (first position) and green(second position) values

		Formula
		(green - nir)/(green + nir)

		"""

		green = green.astype(np.float32)
		nir = nir.astype(np.float32)
		nwdValue = (green - nir) / (green + nir)
		return nwdValue
	

	def visualiseNDWI(self, nwdValue):
		plt.figure(figsize=(10, 10))
		plt.imshow(nwdValue.squeeze(), cmap='gray')
		plt.title('NDWI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED NDWI
	def normWdif(self, cloud, save_location, shp_location=None, bbcoord=None, green=None, nir=None, visualise=False):		
		if cloud ==False and (bbcoord is None):
			green_clipped=clipRasterSHP(green,shp_location)
			nir_clipped=clipRasterSHP(nir,shp_location)
			nwdValue = self.normWaterDif(green_clipped[0], nir_clipped[0])
			writeRaster(nwdValue,green_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			green_clipped=clipRasterBB(green,bbcoord)
			nir_clipped=clipRasterBB(nir,bbcoord)
			nwdValue = self.normWaterDif(green_clipped[0], nir_clipped[0])
			writeRaster(nwdValue,green_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			green_clipped=clipRasterSHP(green,shp_location)
			nir_clipped=clipRasterSHP(nir,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			nwdValue = self.normWaterDif(green_clipped[0], nir_clipped[0])
			print("nwdValue calculation completed")
			nwdValue = np.multiply(nwdValue,cloudMask[0])
			writeRaster(nwdValue,green_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			green_clipped=clipRasterBB(green,bbcoord)
			print("green_clipped calculation completed")
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			nwdValue = self.normWaterDif(green_clipped[0], nir_clipped[0])
			print("nwdValue calculation completed")
			nwdValue = np.multiply(nwdValue,cloudMask[0])
			writeRaster(nwdValue,green_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseNDWI(nwdValue)

	
	def NDWI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.normWdif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, green=self.b3, nir=self.b5)



		# NBR
	def normBurn(self, nir, swir):

		"""
		*Normailized Burn Ratio*
		args are nir (first position) and green(second position) values

		Formula
		(nir - swir)/(nir + swir)

		"""

		nir = nir.astype(np.float32)
		swir = swir.astype(np.float32)
		nbrValue = (nir - swir) / (nir + swir) 
		return nbrValue
	

	def visualiseNBR(self, nbrValue):
		plt.figure(figsize=(10, 10))
		plt.imshow(nbrValue.squeeze(), cmap='gray')
		plt.title('NBR')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED NDVI
	def normBurnRat(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, swir=None, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			swir_clipped=clipRasterSHP(swir,shp_location)
			nbrValue = self.normBurn(nir_clipped[0], swir_clipped[0])
			writeRaster(nbrValue,nir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			swir_clipped=clipRasterBB(swir,bbcoord)
			nbrValue = self.normBurn(nir_clipped[0], swir_clipped[0])
			writeRaster(nbrValue,nir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			swir_clipped=clipRasterSHP(swir,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			nbrValue = self.normBurn(nir_clipped[0], swir_clipped[0])
			print("nbrValue calculation completed")
			nbrValue = np.multiply(nbrValue,cloudMask[0])
			writeRaster(nbrValue,nir_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			swir_clipped=clipRasterBB(swir,bbcoord)
			print("swir_clipped calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			nbrValue = self.normBurn(nir_clipped[0], swir_clipped[0])
			print("nbrValue calculation completed")
			nbrValue = np.multiply(nbrValue,cloudMask[0])
			writeRaster(nbrValue,nir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseNBR(nbrValue)

	
	def NBR(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.normBurnRat(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, nir=self.b5, swir=self.b6)



		# NDBR
	def normBuilt(self, swir, nir):

		"""
		*Normalized Difference Built-Up Index*
		args are swir (first position) and nir(second position) values

		Formula
		(swir - nir)/(swir + nir)
		
		"""
		swir = swir.astype(np.float32)
		nir = nir.astype(np.float32)
		nbutValue = (swir - nir) / (swir + nir) 
		return nbutValue
	

	def visualiseNDBI(self, nbutValue):
		plt.figure(figsize=(10, 10))
		plt.imshow(nbutValue.squeeze(), cmap='gray')
		plt.title('NDBI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED NDBI
	def normBuiltIn(self, cloud, save_location, shp_location=None, bbcoord=None, swir=None, nir=None, visualise=False):		
		if cloud ==False and (bbcoord is None):
			swir_clipped=clipRasterSHP(swir,shp_location)
			nir_clipped=clipRasterSHP(nir,shp_location)
			nbutValue = self.normBuilt(swir_clipped[0], nir_clipped[0])
			writeRaster(nbutValue,swir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			swir_clipped=clipRasterBB(swir,bbcoord)
			nir_clipped=clipRasterBB(nir,bbcoord)
			nbutValue = self.normBuilt(swir_clipped[0], nir_clipped[0])
			writeRaster(nbutValue,swir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			swir_clipped=clipRasterSHP(swir,shp_location)
			nir_clipped=clipRasterSHP(nir,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			nbutValue = self.normBuilt(swir_clipped[0], nir_clipped[0])
			print("nbutValue calculation completed")
			nbutValue = np.multiply(nbutValue,cloudMask[0])
			writeRaster(nbutValue,swir_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			swir_clipped=clipRasterBB(swir,bbcoord)
			print("swir_clipped calculation completed")
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			nbutValue = self.normBuilt(swir_clipped[0], nir_clipped[0])
			print("nbutValue calculation completed")
			nbutValue = np.multiply(nbutValue,cloudMask[0])
			writeRaster(nbutValue,swir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseNDBI(nbutValue)

	
	def NDBI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.normBuiltIn(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, swir=self.b5, nir=self.b6)


