# Example Usage

Clip the output from an external shapefile
```python
# Clip the Image with external shapefile
# If cloud masking is required, set the cloud parameter to True, else False
# If visualization is required, set the visualise parameter to True, else False
import RSensePy
RSensePyObj = RSensePy.L8("path//to//the//Landsat8//Image//Folder")
location_shapefile = "shapefile/location/path"

RSensePyObj.NDVI(cloud=True, save_location="output/Location/path", shp_location="location_shapefile", visualise=False)
```

Clip the output from a bounding box
```python
# Clip the Image with bounding box coordinated
# bbox = [minX, minY, maxX, maxY]
bbox = [13.490206, 48.3355,14.076421, 48.007881]
import RSensePy
RSensePyObj = RSensePy.L8("path//to//the//Landsat8//Image//Folder")
location_shapefile = "shapefile/location/path"

RSensePyObj.NDVI(cloud=True, save_location="output/Location/path", bbcoord=bbox, visualise=False)
```

## Additional usage

```python
import RSensePy

# Load image and initialize ImageObject (similar to previous example)
image = RSensePy.L8("path//to//the//Landsat8//Image//Folder")

# Calculate NDVI using RSensePy
image.NDVI(cloud=True, save_location=output_location, shp_location=shapefile_location, visualise=False)

# Calculate EVI using RSensePy
image.EVI(cloud=True, save_location=output_location, shp_location=shapefile_location, visualise=False)

# Calculate NDWI using RSensePy
image.NDWI(cloud=True, save_location=output_location, shp_location=shapefile_location, visualise=False)

# ... Repeat for other indices ...
```

## Normalised Difference between two bands
Below example shows how to calculate normalised difference between band 4 and band 5
```python
import RSensePy
# Access individual Landsat bands 
band1 = RSensePyObj.b1
band2 = RSensePyObj.b2
...
...
band6 = RSensePyObj.b6
band7 = RSensePyObj.b7

# Access individual Sentinel 2 bands 
band1 = RSensePyObj.B1
band2 = RSensePyObj.B2
...
...
band6 = RSensePyObj.B6
band7 = RSensePyObj.B7


RSensePyObj.norm_dif(cloud=True, save_location=output/Location/path,shp_location=shapefile/location/path, band1= RSensePyObj.b4, band2= RSensePyObj.b5, visualise=True)
```