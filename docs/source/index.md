% RSensePy documentation master file, created by
% sphinx-quickstart on Wed Aug 16 11:03:22 2023.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# Satellite Image Index Calculation

![Vegetation Index Calculation](https://i.ibb.co/mHsrnRt/package-logo.png)

Welcome to the Vegetation Index Calculation Python Package! This package provides advanced features for calculating various vegetation indices from satellite imagery, allowing users to efficiently analyze vegetation patterns and dynamics. Whether you are a researcher, a data scientist, or an environmental enthusiast, this package will empower you to gain valuable insights into vegetation health and distribution.

## Primary features

- **Wide Range of Vegetation Indices:** The package offers a comprehensive selection of popular vegetation indices, including NDVI (Normalized Difference Vegetation Index), EVI (Enhanced Vegetation Index), SAVI (Soil Adjusted Vegetation Index), and more. Each index has been carefully implemented to ensure accurate and reliable results.


- **Batch Processing:** The package is designed for efficiency, allowing you to process large batches of satellite images in parallel. This feature significantly speeds up the analysis and enhances productivity.


- **Visualization Tools:** Visualize the calculated vegetation indices using built-in plotting functions. These visualizations aid in understanding the spatial distribution and temporal changes of vegetation in the study area.


- **Data Preprocessing:** The package offers data preprocessing utilities, including AOI masking and cloud masking, to ensure the quality of input satellite imagery before index calculation.

```{warning}
The library is still under development. Cloud masking of Sentinel 2 is not yet implemented.
```


```{toctree}
:caption: 'Contents:'
:maxdepth: 2

installation
start
indexcalbasics
examples
contribute
license
```
