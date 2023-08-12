**Satellite Image Index Calculation Python Package**

![Vegetation Index Calculation](https://github.com/richiedlon/SoftwareDevProject/blob/main/package_logo.png)

Welcome to the Vegetation Index Calculation Python Package! This package provides advanced features for calculating various vegetation indices from satellite imagery, allowing users to efficiently analyze vegetation patterns and dynamics. Whether you are a researcher, a data scientist, or an environmental enthusiast, this package will empower you to gain valuable insights into vegetation health and distribution.

## Features

- **Wide Range of Vegetation Indices:** The package offers a comprehensive selection of popular vegetation indices, including NDVI (Normalized Difference Vegetation Index), EVI (Enhanced Vegetation Index), SAVI (Soil Adjusted Vegetation Index), and more. Each index has been carefully implemented to ensure accurate and reliable results.

- **Batch Processing:** The package is designed for efficiency, allowing you to process large batches of satellite images in parallel. This feature significantly speeds up the analysis and enhances productivity.

- **Visualization Tools:** Visualize the calculated vegetation indices using built-in plotting functions. These visualizations aid in understanding the spatial distribution and temporal changes of vegetation in the study area.

- **Data Preprocessing:** The package offers data preprocessing utilities, including AOI masking and cloud masking, to ensure the quality of input satellite imagery before index calculation.

## Installation

To install the Vegetation Index Calculation package, you can use pip:

```bash
pip install -i https://test.pypi.org/pypi/ --extra-index-url https://pypi.org/simple RSensePy
```

## Getting Started

Once the package is installed, check out the [example notebook](https://github.com/richiedlon/SoftwareDevProject/RSensePy_example.ipynb) to get started with vegetation index calculation and visualization. The notebook provides step-by-step guidance on loading satellite imagery, calculating vegetation indices, and generating informative visualizations.

```bash
import RSensePy
RSensePy.help()

# Create RSensePy Image Object
RSensePyObj = RSensePy.L8("path//to//the//Landsat8//Image//Folder")
```
## Getting Image Metadata
Once the RSensePy object created users can get meta data by calling the meta function.
```bash
imgobj.meta()
```

## Index calculation basics
# Features

- **Cloud Masking:** RSensePy incorporates cloud masking capabilities, allowing accurate NDVI computation by accounting for cloudy regions within satellite imagery.

- **Save Location:** Users can conveniently specify the directory where computed NDVI outputs will be saved, promoting organized data management and easy access for further analysis.

- **AOI Integration:** The package seamlessly integrates shapefiles or Bounding box for targeted analysis. By providing a shapefile location, users can focus computation on specific geographic regions, enhancing analysis precision.

- **Optional Visualization:** RSensePy provides an optional visualization feature, enabling users to visualize the calculated NDVI outputs spatially and gain insights into vegetation health distribution in grayscale.

```bash
# Clip the Image with external shapefile
RSensePyObj.NDVI(cloud=True, save_location=output/Location/path, shp_location=shapefile/location/path, visualise=False)
```
```bash
# Clip the Image with bounding box coordinated
bbox = [13.490206, 48.3355,14.076421, 48.007881]
RSensePyObj.NDVI(cloud=True, save_location=output/Location/path, bbcoord=bbox, visualise=False)
```

## Get capabilities of the RSensePy
Provide information about which Indexes can be calculated. Note - At the moment only Landsat 8 images are supported.
```bash
RSensePy.getCapabilities()
```



## Contributing

We welcome contributions from the community! If you would like to contribute to the package, please contact the developers for more information.

## Bug Reports and Support

If you encounter any issues or have questions regarding the package, please submit a bug report or question in the [Issues](https://github.com/richiedlon/SoftwareDevProject/issues) section of this repository.

## License

This package is licensed under the [MIT License](https://github.com/your_username/vegetation_index_calculation/blob/main/LICENSE). You are free to use, modify, and distribute the package according to the terms of this license.

We hope that this Python package will be a valuable asset to your vegetation analysis endeavors. Happy coding and exploring the wonders of vegetation using the Vegetation Index Calculation package!
