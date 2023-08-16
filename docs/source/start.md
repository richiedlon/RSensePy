# Getting started


```python
# Import RSensePy package
import RSensePy

# You can also call following function and see the step by steps
RSensePy.help()

# Create RSensePy Image Object
RSensePyObj = RSensePy.L8("path//to//the//Landsat8//Image//Folder") # Landsat 8 or 9
RSensePyObj = RSensePy.L8("path//to//the//Sentinel2//Image//Folder") # Sentinel 2 image
```

### Getting Image Metadata
Once the RSensePy object created users can get meta data by calling the meta function.
```python
RSensePyObj.meta()
```

Check out the [example notebook](https://github.com/richiedlon/SoftwareDevProject/RSensePy_example.ipynb) to get started with vegetation index calculation and visualization. 

The notebook provides step-by-step guidance on loading satellite imagery, calculating vegetation indices, and generating informative visualizations.