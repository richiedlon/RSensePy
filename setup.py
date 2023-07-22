from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
	long_description = f.read()

setup(
	name = "indexcalculator",
	version = "0.0.3",
	description = "Biophysical parameter calculator for Landsat 8 data",
	package_dir ={"":"app"},
	packages = find_packages(where="app"),
	long_description=long_description,
	long_description_content_type="text/markdown",
	url = "https://github.com/richiedlon/SoftwareDevProject",
	author = "richiedlon/opeyami",
	license="MIT",
	cliassifiers=[
		"License :: MIT License",
		"Programming Language :: Python :: 3.9"
	],
	# install_requires = ["affine>=2.4.0",
	# 					"attrs>=23.1.0",
	# 					"certifi>=2023.5.7",
	# 					"click>=8.1.5",
	# 					"click-plugins>=1.1.1",
	# 					"cligj>=0.7.2",
	# 					"colorama>=0.4.6",
	# 					"contourpy>=1.1.0",
	# 					"cycler>=0.11.0",
	# 					"Fiona>=1.9.4.post1",
	# 					"fonttools>=4.41.0",
	# 					"geopandas>=0.13.2",
	# 					"importlib-metadata>=6.8.0",
	# 					"importlib-resources>=6.0.0",
	# 					"kiwisolver>=1.4.4",
	# 					"matplotlib>=3.7.2",
	# 					"numpy>=1.25.1",
	# 					"packaging>=23.1",
	# 					"pandas>=2.0.3",
	# 					"Pillow>=10.0.0",
	# 					"pyparsing>=3.0.9",
	# 					"pyproj>=3.6.0",
	# 					"python-dateutil>=2.8.2",
	# 					"pytz>=2023.3",
	# 					"rasterio>=1.3.6",
	# 					"shapely>=2.0.1",
	# 					"six>=1.16.0",
	# 					"snuggs>=1.4.7",
	# 					"tzdata>=2023.3",
	# 					"zipp>=3.16.2"],
	install_requires = ["rasterio>=1.3.0","matplotlib>=3.7.0","shapely>=2.0.0","Fiona>=1.9.4.post1","geopandas>=0.13.0"],
	extras_requires={
		"dev":["pytest>=7.0","twine>=4.0.2"],
	},
	python_requires=">=3.9.16",


	)