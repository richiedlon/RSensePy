import os
import os.path
import sys
import numpy as np
from RSensePy.clip_withBB_function import clipRasterBB
from RSensePy.clip_withSHP_function import clipRasterSHP
from RSensePy.writeRasterFunction import writeRaster
from RSensePy.cloudMask_clip import cloud_mask_landsat8_clip
from RSensePy.cloudMask_clip import cloud_mask_landsat8_clip_shp
import matplotlib
import matplotlib.pyplot as plt

def selectsensor():
    satellite=""
    answer= input("""
Hello there!
Welcome to RsensePy, your handy tool to compute a diverse range of optical remote-sensing based indices hitch free!
Please note that RsensePy currently surpports level 2A (surface reflectance) Landsat 8 and Sentinel 2 imagery only.
Select your satellite type below to get a list of available satellite-specific indices on RsensePy.

What imagery are you working with today? 
Please type 8 for Landsat8 Imagery or 2 for Sentinel 2 Imagery. 
""")
    if answer == "8":
        satellite = "Landsat 8"
        print(f"""With your Landsat {answer} imagery, you can run the following indices:
        Normalized Difference Vegetation Index (NDVI)
        Enhanced Vegetation Index(EVI)
        Normalized Differnce Water Index(NDWI)
        Normalized Burn Ratio(NBR)
        Normalized Difference Built-Up Index(NDBI)
        Green Normalised Difference Vegeation Index(GNDVI)
        Green Leaf Index(GLI)
        Soil Adjusted Vegetation Index (SAVI)
        Green Soild Adjusted Vegetation Index(GSAVI)
        Green Chlorophyll Index(GLI)
        Visible Atmospherically Resistant Index (VARI)
              """)
    elif answer == "2":
        satellite = "Sentinel 2"
        print(f"""With your Sentinel {answer} imagery, you can run the following indices:
        Normalized Difference Vegetation Index (NDVI)
        Enhanced Vegetation Index(EVI)
        Normalized Differnce Water Index(NDWI)
        Normalized Burn Ratio(NBR)
        Normalized Difference Built-Up Index(NDBI)
        Green Normalised Difference Vegeation Index(GNDVI)
        Green Leaf Index(GLI)
        Soil Adjusted Vegetation Index (SAVI)
        Green Soild Adjusted Vegetation Index(GSAVI)
        Green Chlorophyll Index(GCI)
        Red-Edge Chlorophyll Index(ReCI)
        Visible Atmospherically Resistant Index (VARI)
              """)
    else: 
        answer != "8" and "2"
        print("Please rerun and input the appropriate value")
    
    return satellite, answer

sat = selectsensor[1]

if sat == 8:
	print("""
       To initiate your Landsat8 imagery for use with RsensPy, please run the L8 class using the file name as input. 
       Then get the metadata by calling the meta() method
       """)
elif sat == 2:
	print("""
	   To initiate your Sentinel2 imagery for use with RsensPy, please run the S2 class using the file name as input
       Then get the metadata by calling the meta() method
       """)

### Defining the Landsat 8 Class and accompanying methods
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

### Defining Indices for Landsat 8 processing

	def normalized_difference(self, band1, band2):
		band1 = band1.astype(np.float32)
		band2 = band2.astype(np.float32)
		numerator = band1 - band2
		denominator = band1 + band2
		normDifVal = numerator / denominator
		return normDifVal

	def visualiseFunc(self, normDifVal, title):
		plt.figure(figsize=(10, 10))
		plt.imshow(normDifVal.squeeze(), cmap='gray')
		plt.title(title)
		plt.colorbar()
		plt.show()

	def norm_dif(self, cloud, save_location, shp_location=None, bbcoord=None, band1=None, band2=None, visualise=False, title = "Visualization of Normalized Difference"):		
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
			self.visualiseFunc(normDifVal, title)

	def NDVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.norm_dif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, band1=self.b5, band2=self.b4, title="Normalized Difference Vegetation Index")


		#EVI
	def EVIcal(self, nir, red, blue, G = 2.5, L = 1, C1 = 6, C2 = 7.5):    
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

		# PARAMETERIZED EVI
	def evi_para(self, cloud, save_location,  nir, red, blue, shp_location=None, bbcoord=None, visualise=False, title = 'Enhanced Vegetation Index'):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			red_clipped=clipRasterSHP(red,shp_location)
			blue_clipped=clipRasterSHP(blue,shp_location)
			#eviValue = self.normalized_difference(red_clipped[0], nir_clipped[0])
			eviValue = self.EVIcal(nir_clipped[0], red_clipped[0], blue_clipped[0])
			writeRaster(eviValue,red_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			red_clipped=clipRasterBB(red,bbcoord)
			blue_clipped=clipRasterBB(blue,bbcoord)
			eviValue = self.EVIcal(nir_clipped[0], red_clipped[0], blue_clipped[0])
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
			eviValue = self.EVIcal(nir_clipped[0], red_clipped[0], blue_clipped[0])
			print("eviValue calculation completed")
			eviValue = np.multiply(eviValue,cloudMask[0])
			writeRaster(eviValue,red_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			print("nir_clipped calculation completed")
			red_clipped=clipRasterBB(red,bbcoord)
			print("Red_clipped calculation completed")
			blue_clipped=clipRasterBB(blue,bbcoord)
			print("Red_clipped calculation completed")
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			eviValue = self.EVIcal(nir_clipped[0], red_clipped[0], blue_clipped[0])
			print("eviValue calculation completed")
			eviValue = np.multiply(eviValue,cloudMask[0])
			writeRaster(eviValue,red_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseFunc(eviValue, title)

	
	def EVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.evi_para(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, red=self.b4, nir=self.b5, blue=self.b2)
	
	def NDWI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.norm_dif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, band1=self.b3, band2=self.b5, title="Normalized Difference Water Index")

	def NBR(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		"""
		*Normailized Burn Ratio*
		args are nir (first position) and green(second position) values

		Formula
		(nir - swir)/(nir + swir)

		"""
		self.norm_dif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, band1=self.b5, band2=self.b6, title="Normalized Burn Ratio")

	
	def NDBI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		"""
		*Normalized Difference Built-Up Index*
		args are swir (first position) and nir(second position) values

		Formula
		(swir - nir)/(swir + nir)
		"""		
		self.norm_dif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, band1=self.b6, band2=self.b5, title ="Normalized Difference Built-Up Index")

	
	def GNDVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		"""
		*Green Normalized Difference Vegetation Index*
		args are nir (first position) and green(second position) values

		Formula
		GNDVI = (nir-green)/(nir+green)

		"""
		self.norm_dif(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, band1=self.b5, band2=self.b3, title ="Green Normalized Difference Vegetation Index")


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
			self.visualiseFunc(gliValue, 'Green Leaf Index')

	
	def GLI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		"""
		*Green Leaf Index*
		args are green (first position) and red(second position) and blue (thrid position) values

		Formula
		gli = (2*green - red - blue)/(2*green + red + blue)
		"""
		self.gLeafIn(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, green=self.b3, red=self.b4, blue=self.b2)



# SAVI

	def savi(self, band1, band2, L=0.5):
		band1 = band1.astype(np.float32)
		band2 = band2.astype(np.float32)

		saviVal = ((1 + L) * (band1 - band2)) / (band1 + band2 + L)

		return saviVal

		# PARAMETERIZED SAVI
	def soilAvi(self, cloud, save_location, title, shp_location=None, bbcoord=None, band1=None, band2=None, L=0.5, visualise=False):		
		if cloud ==False and (bbcoord is None):
			band1_clipped=clipRasterSHP(band1,shp_location)
			band2_clipped=clipRasterSHP(band2,shp_location)
			saviVal = self.savi(band1_clipped[0], band2_clipped[0])
			writeRaster(saviVal,band1_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			band1_clipped=clipRasterBB(band1,bbcoord)
			band2_clipped=clipRasterBB(band2,bbcoord)
			saviVal = self.savi(band1_clipped[0], band2_clipped[0])
			writeRaster(saviVal,band1_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			band1_clipped=clipRasterSHP(band1,shp_location)
			band2_clipped=clipRasterSHP(band2,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			saviVal = self.savi(band1_clipped[0], band2_clipped[0])
			print("saviVal calculation completed")
			saviVal = np.multiply(saviVal,cloudMask[0])
			writeRaster(saviVal,band1_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			band1_clipped=clipRasterBB(band1,bbcoord)
			band2_clipped=clipRasterBB(band2,bbcoord)
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			saviVal = self.savi(band1_clipped[0], band2_clipped[0])
			print("saviVal calculation completed")
			saviVal = np.multiply(saviVal,cloudMask[0])
			writeRaster(saviVal,band1_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseFunc(saviVal, title)

	
	def SAVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.soilAvi(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, band1=self.b5, band2=self.b4, title = 'Soil Adjusted Vegetation Index')



# GSAVI

	def GSAVI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None, L=0.5):
		"""
		*Soil Adjusted Vegetation Index*
		args are nir (first position) and green(second position) values

		Formula: ((1 + L) * (NIR - green)) / (NIR + green + L), 

		default L = 0.5
		"""
		self.soilAvi(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, band1=self.b5, band2=self.b3, title = 'Green Soil Adjusted Vegetation Index')
		gsaviVal = ((1 + L) * (nir - green)) / (nir + green + L)
		return gsaviVal


# GCI

	def gci(self,nir, green, C=1):

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

		# PARAMETERIZED GCI
	def gChloIn(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, green=None, C=1, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			green_clipped=clipRasterSHP(green,shp_location)
			gciVal = self.gci(nir_clipped[0], green_clipped[0])
			writeRaster(gciVal,nir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			green_clipped=clipRasterBB(green,bbcoord)
			gciVal = self.gci(nir_clipped[0], green_clipped[0])
			writeRaster(gciVal,nir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			green_clipped=clipRasterSHP(green,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			gciVal = self.gci(nir_clipped[0], green_clipped[0])
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
			gciVal = self.gci(nir_clipped[0], green_clipped[0])
			print("gciVal calculation completed")
			gciVal = np.multiply(gciVal,cloudMask[0])
			writeRaster(gciVal,nir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseFunc(gciVal, "Green Chlorophyll Index")

	
	def GCI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.gChloIn(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, nir=self.b5, green=self.b4)



# R_ECI
	def redgeCI(self, nir, redge, C=1):

		"""
		Only for Sentinel 2 (red_edge band is only available in Sentinel 2)
		
		*Red-edge Chlorophyll Index (CI-Red_edge Or R-ECI)*
		args are nir (first position) and redge(second position) values

    	Formula:  nir / (redge - C).

		C = 1
		"""

		nir = nir.astype(np.float32)
		redge = redge.astype(np.float32)

		reCiVal = nir / (redge - C)
		return reCiVal


		# PARAMETERIZED R_ECI
	def reCInd(self, cloud, save_location, shp_location=None, bbcoord=None, nir=None, redge=None, C=1, visualise=False):		
		if cloud ==False and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			redge_clipped=clipRasterSHP(redge,shp_location)
			reCiVal = self.redgeCI(nir_clipped[0], redge_clipped[0])
			writeRaster(reCiVal,nir_clipped[1],save_location)
		elif cloud ==False and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			redge_clipped=clipRasterBB(redge,bbcoord)
			reCiVal = self.redgeCI(nir_clipped[0], redge_clipped[0])
			writeRaster(reCiVal,nir_clipped[1],save_location)
		elif cloud ==True and (bbcoord is None):
			nir_clipped=clipRasterSHP(nir,shp_location)
			redge_clipped=clipRasterSHP(redge,shp_location)
			cloudMask = cloud_mask_landsat8_clip_shp(self.qa_pixel,shp_location)
			print("cloudMask calculation completed")
			reCiVal = self.redgeCI(nir_clipped[0], redge_clipped[0])
			print("reCiVal calculation completed")
			reCiVal = np.multiply(reCiVal,cloudMask[0])
			writeRaster(reCiVal,nir_clipped[1],save_location)
			print("Writing raster completed")
		elif cloud ==True and (shp_location is None):
			nir_clipped=clipRasterBB(nir,bbcoord)
			redge_clipped=clipRasterBB(redge,bbcoord)
			cloudMask = cloud_mask_landsat8_clip(self.qa_pixel,bbcoord)
			print("cloudMask calculation completed")
			reCiVal = self.redgeCI(nir_clipped[0], redge_clipped[0])
			print("reCiVal calculation completed")
			reCiVal = np.multiply(reCiVal,cloudMask[0])
			writeRaster(reCiVal,nir_clipped[1],save_location)
			print("Writing raster completed")

		if visualise==True:
			self.visualiseFunc(reCiVal, "Red-edge Chlorophyll Index")

	
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
			self.visualiseFunc(variVal, "Visible Atmospherically Resistant Index (VARI)")

	def VARI(self, cloud, save_location, visualise, shp_location=None, bbcoord=None):
		self.visibleARI(visualise=visualise, cloud=cloud, save_location=save_location, shp_location=shp_location, bbcoord=bbcoord, green=self.b3, red=self.b4, blue=self.b2)


### Defining Sentinel 2 class and accompanying methods

class S2:
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
		self.mission=namelist[0]
		self.product_level=namelist[1]
		self.sensing_date=namelist[2]
		self.base_number=namelist[3]
		self.ron=namelist[4]  
		self.tnf=namelist[5]  
		pd_pf=namelist[6]

		def splitpd_pf(pd_pf):
			list=[]
			for i in pd_pf.split('.'):
				list.append(i)
			return list[0], list[1]
		
		self.prod_descript=splitpd_pf[0]
		self.prod_format=splitpd_pf[1]  

	# METADATA
	def meta(self):
		print(f"""\n
					Mission = {self.mission}\n 
					Product Level = {self.product_level}\n
					Sensing Date= {self.sensing_date}\n
					Base Number = {self.base_number}\n
					Relative Orbit Number = {self.ron}\n
					Tile Number Field = {self.tnf}\n
					Product Descriptor = {self.prod_descript}\n
					Product Format = {self.prod_format}\n""")