# Getting started


```python
# Import RSensePy package
import RSensePy

# Call the function below to get a list of available indices for your imagery (Indices available for Landast 8/9 and Sentinel 2 imagery)
RSensePy.getCapabillities()

# Call the function below to get step by step guidiance on setup and index calculation
RSensePy.help()

# Create RSensePy Image Object
RSensePyObj = RSensePy.L8("path//to//the//Landsat8//Image//Folder") # Landsat 8 or 9
RSensePyObj = RSensePy.L8("path//to//the//Sentinel2//Image//Folder") # Sentinel 2 image
```

### Getting Image Metadata
Once the RSensePy object has been created, users can get metadata by calling the meta function.
```python
RSensePyObj.meta()
```

Check out the [example notebook](https://github.com/richiedlon/RSensePy/blob/main/RSensePy_test.ipynb) to get started with vegetation index calculation and visualization. 


The notebook provides step-by-step guidance on loading satellite imagery, calculating vegetation indices, and generating informative visualizations.
