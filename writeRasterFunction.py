import rasterio
def writeRaster(out_img,out_meta,out_tif): # Input numpy array of the biophysical output, metadata of clipped raster, output location
	with rasterio.open(out_tif, "w", **out_meta) as dest:
		dest.write(out_img)