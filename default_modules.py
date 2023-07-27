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


	#Defining the metadata
		basename = os.path.basename(directory) #where directory is the path to teh L8 data folder
		namelist=[]

		for i in basename.split('_'):
			namelist.append(i)
			
	#Defining the individual metadata varaibles
		mss=namelist[0]

		def splitmss(mss):
			mission=mss[0]
			sensor=mss[1]
			satellite=mss[2:]

			return mission, sensor, satellite
		
		mmsR = splitmss(mss)

		self.mission=mmsR[0]
		self.sensor=mmsR[1]
		self.satellite=mmsR[2]
		self.corr_level=namelist[1]
		pr=namelist[2]

		def splitpr(pr):
			path=pr[:3]
			row=pr[3:]

			return path, row

		prR = splitpr(pr)

		self.path=prR[0]
		self.row=prR[1]
		self.acqui_date=namelist[3]
		self.process_date=namelist[4]
		self.coll_number=namelist[5]
		self.coll_category=namelist[6]  

	# METADATA
	def meta(self):
		print(f"""\n
	Mission = {self.mission}\n 
	Sensor = {self.sensor}\n
	Satellite= {self.satellite}\n
	Correction Level = {self.corr_level}\n
	Path = {self.path}\n
	Row = {self.row}\n
	Acquisition Date = {self.acqui_date}\n
	Processing Data = {self.process_date}\n
	Collection Number = {self.coll_number}\n
	Collection Category = {self.coll_category}\n""")
		

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
		self.norm_dif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, nir=self.b5, red=self.b4)


		

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
		self.normBuiltIn(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, swir=self.b6, nir=self.b5)


# GNDVI
	def gnormalized_difference(self, nir, green):

		"""
		*Green Normalized Difference Vegetation Index*
		args are nir (first position) and green(second position) values

		Formula
		ndvi = (nir-green)/(nir+green)

		"""

		nir = nir.astype(np.float32)
		green= green.astype(np.float32)
		gnormDifVal = (nir - green) / (nir + green) #why the error
		return gnormDifVal
	

	def visualiseGNDVI(self, gnormDifVal):
		plt.figure(figsize=(10, 10))
		plt.imshow(gnormDifVal.squeeze(), cmap='gray')
		plt.title('GNDVI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED GNDVI
	def gnorm_dif(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, green=None, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			green_clipped=clipRasterSHP(green,shp_location)
			gnormDifVal = self.gnormalized_difference(nir_clipped[0], green_clipped[0])
			writeRaster(gnormDifVal,nir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			green_clipped=clipRasterBB(green,bbcoord)
			gnormDifVal = self.gnormalized_difference(nir_clipped[0], green_clipped[0])
			writeRaster(gnormDifVal,nir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			green_clipped=clipRasterSHP(green,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			gnormDifVal = self.gnormalized_difference(nir_clipped[0], green_clipped[0])
			print("gnormDifVal calculation completed")
			gnormDifVal = np.multiply(gnormDifVal,cloudMask[0])
			writeRaster(gnormDifVal,nir_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			green_clipped=clipRasterBB(green,bbcoord)
			print("green_clipped calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			gnormDifVal = self.gnormalized_difference(nir_clipped[0], green_clipped[0])
			print("gnormDifVal calculation completed")
			gnormDifVal = np.multiply(gnormDifVal,cloudMask[0])
			writeRaster(gnormDifVal,nir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseGNDVI(gnormDifVal)

	
	def GNDVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.gnorm_dif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, nir=self.b5, green=self.b3)



# GLI
	def gli(self, green,red,blue):
		
		"""
		*Green Leaf Index*
		args are green (first position) and red(second position) and blue (thrid position) values

		Formula
		gli = (2*green - red - blue)/(2*green + red + blue)
		
		"""

		green = green.astype(np.float32)
		red = red.astype(np.float32)
		blue = blue.astype(np.float32)

		gliValue = (2*green - red- blue)/(2*green + red + blue)
		return gliValue
	

	def visualiseGLI(self, gliValue):
		plt.figure(figsize=(10, 10))
		plt.imshow(gliValue.squeeze(), cmap='gray')
		plt.title('GLI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED GLI
	def gLeafIn(self, cloud, save_location, shp_location=None, bbcoord=None, green=None, red=None, blue=None, visualise=False):		
		if cloud ==False and (bbcoord is None):
			green_clipped=clipRasterSHP(green,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			blue_clipped=clipRasterSHP(blue,shp_location)
			gliValue = self.gli(green_clipped[0], red_clipped[0], blue_clipped[0])
			writeRaster(gliValue,green_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			green_clipped=clipRasterBB(green,bbcoord)
			red_clipped=clipRasterBB(red,bbcoord)
			blue_clipped=clipRasterBB(blue,bbcoord)
			gliValue = self.gli(green_clipped[0], red_clipped[0], blue_clipped[0])
			writeRaster(gliValue,green_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			green_clipped=clipRasterSHP(green,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			blue_clipped=clipRasterSHP(blue,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			gliValue = self.gli(green_clipped[0], red_clipped[0], blue_clipped[0])
			print("gliValue calculation completed")
			gliValue = np.multiply(gliValue,cloudMask[0])
			writeRaster(gliValue,green_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			green_clipped=clipRasterBB(green,bbcoord)
			red_clipped=clipRasterBB(red,bbcoord)
			blue_clipped=clipRasterBB(blue,bbcoord)
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			gliValue = self.gli(green_clipped[0], red_clipped[0], blue_clipped[0])
			print("gliValue calculation completed")
			gliValue = np.multiply(gliValue,cloudMask[0])
			writeRaster(gliValue,green_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseGLI(gliValue)

	
	def GLI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.gLeafIn(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, green=self.b3, red=self.b4, blue=self.b2)



# SAVI
	def savi(self, nir, red, L=0.5):
		
		"""
		*Soil Adjusted Vegetation Index*
		args are nir (first position) and red(second position) values

		Formula: ((1 + L) * (NIR - Red)) / (NIR + Red + L), 

		default L = 0.5
		"""
		red = red.astype(np.float32)
		nir = nir.astype(np.float32)

		saviVal = ((1 + L) * (nir - red)) / (nir + red + L)
		return saviVal

	def visualiseSAVI(self, saviVal):
		plt.figure(figsize=(10, 10))
		plt.imshow(saviVal.squeeze(), cmap='gray')
		plt.title('SAVI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED SAVI
	def soilAvi(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, red=None, L=0.5, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			saviVal = self.savi(nir_clipped[0], red_clipped[0], L)
			writeRaster(saviVal,nir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			red_clipped=clipRasterBB(red,bbcoord)
			saviVal = self.savi(nir_clipped[0], red_clipped[0], L)
			writeRaster(saviVal,nir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			saviVal = self.savi(nir_clipped[0], red_clipped[0], L)
			print("saviVal calculation completed")
			saviVal = np.multiply(saviVal,cloudMask[0])
			writeRaster(saviVal,nir_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			red_clipped=clipRasterBB(red,bbcoord)
			print("red calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			saviVal = self.savi(nir_clipped[0], red_clipped[0], L)
			print("saviVal calculation completed")
			saviVal = np.multiply(saviVal,cloudMask[0])
			writeRaster(saviVal,nir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseSAVI(saviVal)

	
	def SAVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.soilAvi(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, nir=self.b5, red=self.b4)



# GSAVI
	def gsavi(self, nir, green, L=0.5):
		
		"""
		*Soil Adjusted Vegetation Index*
		args are nir (first position) and green(second position) values

		Formula: ((1 + L) * (NIR - green)) / (NIR + green + L), 

		default L = 0.5
		"""
		green = green.astype(np.float32)
		nir = nir.astype(np.float32)

		gsaviVal = ((1 + L) * (nir - green)) / (nir + green + L)
		return gsaviVal

	def visualiseGSAVI(self, gsaviVal):
		plt.figure(figsize=(10, 10))
		plt.imshow(gsaviVal.squeeze(), cmap='gray')
		plt.title('GSAVI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED GSAVI
	def gsoilAvi(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, green=None, L=0.5, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			green_clipped=clipRasterSHP(green,shp_location)
			gsaviVal = self.gsavi(nir_clipped[0], green_clipped[0], L)
			writeRaster(gsaviVal,nir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			green_clipped=clipRasterBB(green,bbcoord)
			gsaviVal = self.gsavi(nir_clipped[0], green_clipped[0], L)
			writeRaster(gsaviVal,nir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			green_clipped=clipRasterSHP(green,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			gsaviVal = self.gsavi(nir_clipped[0], green_clipped[0], L)
			print("gsaviVal calculation completed")
			gsaviVal = np.multiply(gsaviVal,cloudMask[0])
			writeRaster(gsaviVal,nir_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			green_clipped=clipRasterBB(green,bbcoord)
			print("green calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			gsaviVal = self.gsavi(nir_clipped[0], green_clipped[0], L)
			print("gsaviVal calculation completed")
			gsaviVal = np.multiply(gsaviVal,cloudMask[0])
			writeRaster(gsaviVal,nir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseGSAVI(gsaviVal)

	
	def GSAVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.gsoilAvi(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, nir=self.b5, green=self.b4)



# GCI
	def gci(self, nir, green, C=1):

		"""
		*Green Chlorophyll Index (CI-green Or GCI)*
		args are nir (first position) and green(second position) values

		Formula: nir / (green - C).

		C = 1
		"""
   
		nir = nir.astype(np.float32)
		green = green.astype(np.float32)

		gciVal = nir / (green - C)
		return gciVal

	def visualiseGCI(self, gciVal):
		plt.figure(figsize=(10, 10))
		plt.imshow(gciVal.squeeze(), cmap='gray')
		plt.title('GCI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED GCI
	def gChloIn(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, green=None, C=1, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			green_clipped=clipRasterSHP(green,shp_location)
			gciVal = self.gci(nir_clipped[0], green_clipped[0], C)
			writeRaster(gciVal,nir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			green_clipped=clipRasterBB(green,bbcoord)
			gciVal = self.gci(nir_clipped[0], green_clipped[0], C)
			writeRaster(gciVal,nir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			green_clipped=clipRasterSHP(green,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			gciVal = self.gci(nir_clipped[0], green_clipped[0], C)
			print("gciVal calculation completed")
			gciVal = np.multiply(gciVal,cloudMask[0])
			writeRaster(gciVal,nir_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			green_clipped=clipRasterBB(green,bbcoord)
			print("green calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			gciVal = self.gci(nir_clipped[0], green_clipped[0], C)
			print("gciVal calculation completed")
			gciVal = np.multiply(gciVal,cloudMask[0])
			writeRaster(gciVal,nir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseGCI(gciVal)

	
	def GCI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.gChloIn(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, nir=self.b5, green=self.b4)



# R_ECI
	def redgeCI(self, nir, redge, C=1):

		"""
		Only for Sentinel 2 (red_edge band is only available in Sentinel 2)

		##rework reCI 

		*Red-edge Chlorophyll Index (CI-Red_edge Or R-ECI)*
		args are nir (first position) and redge(second position) values

    	Formula:  nir / (redge - C).

		C = 1
		"""
   
		nir = nir.astype(np.float32)
		redge = redge.astype(np.float32)

		reCiVal = nir / (redge - C)
		return reCiVal

	def visualiseRECI(self, reCiVal):
		plt.figure(figsize=(10, 10))
		plt.imshow(reCiVal.squeeze(), cmap='gray')
		plt.title('Red-Edge CI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED R_ECI
	def reCInd(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, redge=None, C=1, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			redge_clipped=clipRasterSHP(redge,shp_location)
			reCiVal = self.redgeCI(nir_clipped[0], redge_clipped[0], C)
			writeRaster(reCiVal,nir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			redge_clipped=clipRasterBB(redge,bbcoord)
			reCiVal = self.redgeCI(nir_clipped[0], redge_clipped[0], C)
			writeRaster(reCiVal,nir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			redge_clipped=clipRasterSHP(redge,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			reCiVal = self.redgeCI(nir_clipped[0], redge_clipped[0], C)
			print("reCiVal calculation completed")
			reCiVal = np.multiply(reCiVal,cloudMask[0])
			writeRaster(reCiVal,nir_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			redge_clipped=clipRasterBB(redge,bbcoord)
			print("red edge calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			reCiVal = self.redgeCI(nir_clipped[0], redge_clipped[0], C)
			print("reCiVal calculation completed")
			reCiVal = np.multiply(reCiVal,cloudMask[0])
			writeRaster(reCiVal,nir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseRECI(reCiVal)

	
	def RECI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.reCInd(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, nir=self.b5, redge=self.b4)


# VARI
	def v_ari(self, green, red, blue):
		
		"""
		*Visible Atmospherically Resistant Index (VARI)*
		args are green (first position) and red (second position) and blue(third position) values

		Similar to NDVI but useful when you only have RGB imagery. 

		Formula:  (green - red) / (green + red - blue)
		"""

		green = green.astype(np.float32)
		red = red.astype(np.float32)
		blue = blue.astype(np.float32)

		variVal = (green - red) / (green + red -blue)
		return variVal

	def visualiseVARI(self, variVal):
		plt.figure(figsize=(10, 10))
		plt.imshow(variVal.squeeze(), cmap='gray')
		plt.title('VARI')
		plt.colorbar()
		plt.show()

		# PARAMETERIZED VARI
	def visibleARI(self, cloud, save_location, shp_location=None, bbcoord=None, green=None, red=None, blue=None, visualise=False):		
		if cloud ==False and (bbcoord is None):
			green_clipped=clipRasterSHP(green,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			blue_clipped=clipRasterSHP(blue,shp_location)
			variVal = self.v_ari(green_clipped[0], red_clipped[0], blue_clipped[0])
			writeRaster(variVal,green_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			green_clipped=clipRasterBB(green,bbcoord)
			red_clipped=clipRasterBB(red,bbcoord)
			blue_clipped=clipRasterBB(blue,bbcoord)
			variVal = self.v_ari(green_clipped[0], red_clipped[0], blue_clipped[0])
			writeRaster(variVal,green_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			green_clipped=clipRasterSHP(green,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			blue_clipped=clipRasterSHP(blue,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			variVal = self.v_ari(green_clipped[0], red_clipped[0], blue_clipped[0])
			print("reCiVal calculation completed")
			variVal = np.multiply(variVal,cloudMask[0])
			writeRaster(variVal,green_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			green_clipped=clipRasterBB(green,bbcoord)
			red_clipped=clipRasterBB(red,bbcoord)
			blue_clipped=clipRasterBB(blue,bbcoord)
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			variVal = self.v_ari(green_clipped[0], red_clipped[0], blue_clipped[0])
			print("reCiVal calculation completed")
			variVal = np.multiply(variVal,cloudMask[0])
			writeRaster(variVal,green_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseVARI(variVal)

	
	def VARI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.visibleARI(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, green=self.b3, red=self.b4, blue=self.b2)