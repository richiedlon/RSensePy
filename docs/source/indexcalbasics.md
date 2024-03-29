# Index calculation basics
### Features

- **Cloud Masking:** RSensePy incorporates cloud masking capabilities, allowing accurate NDVI computation by accounting for cloudy regions within satellite imagery.

- **Save Location:** Users can conveniently specify the directory where computed NDVI outputs will be saved, promoting organized data management and easy access for further analysis.

- **AOI Integration:** The package seamlessly integrates shapefiles or Bounding box for targeted analysis. By providing a shapefile location, users can focus computation on specific geographic regions, enhancing analysis precision.

- **Optional Visualization:** RSensePy provides an optional visualization feature, enabling users to visualize the calculated NDVI outputs spatially and gain insights into vegetation health distribution in grayscale.

- **Custom normalized difference calculation:** RSensePy provides an optional visualization feature, enabling users to visualize the calculated NDVI outputs spatially and gain insights into vegetation health distribution in grayscale.

### Supported Indices and Object Methods
Landsat 8/9 and Sentinel 2
- **Normalized Difference Vegetation Index (NDVI):** `NDVI()`
- **Enhanced Vegetation Index (EVI):** `EVI()`
- **Normalized Difference Water Index (NDWI):** `NDWI()`
- **Normalized Burn Ratio (NBR):** `NBR()`
- **Normalized Difference Built-Up Index (NDBI):** `NDBI()`
- **Green Normalized Difference Vegetation Index (GNDVI):** `GNDVI()`
- **Green Leaf Index (GLI):** `GLI()`
- **Soil Adjusted Vegetation Index (SAVI):** `SAVI()`
- **Green Soil Adjusted Vegetation Index (GSAVI):** `GSAVI()`
- **Green Chlorophyll Index (GCI):** `GCI()`
- **Visible Atmospherically Resistant Index (VARI):** `VARI()`

Sentinel 2 only
- **Red-Edge Chlorophyll Index (RECI):** `RECI()`

### Notes on using Sentinel 2 imagery

- **The imagery files are located within the current working directory**
- **The Sentinel 2 product folder contains only the relevant resolution folder (e.g. if 20m resolution is being used, delete the other 10 and 60 meter folders)**.
 or
- **Extract just the relevant resolution folder into a parent folder with the same name as the downloaded sentinel 2 product**.
