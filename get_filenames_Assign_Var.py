import os
a = os.chdir('C://Studies//Copernicus Program//1_Semester 2//Software development practice//Final project//LC08_L2SP_191027_20220720_20220726_02_T1')

def get_tif_files(directory):
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
	return QA_PIXEL,B1, B2, B3, B4, B5, B6, B7

	#for item in tif_files:#if item[-9:]=='PIXEL.TIF'
	return tif_files


filelist = get_tif_files(a)
print (filelist[4])
