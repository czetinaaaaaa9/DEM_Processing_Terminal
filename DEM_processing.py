from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
#Read & Write raster files with GDAL in Python Tutorial
gdal.UseExceptions()
dem = input("Please Enter the DEM you wish to access: ")
ds = gdal.Open(dem)
band = ds.GetRasterBand(1)
array = band.ReadAsArray()
options = gdal.DEMProcessingOptions(computeEdges=True)
gt = ds.GetGeoTransform()
proj = ds.GetProjection()
while True:
    try:
        info_bool = int(input("Do you wish to view information on the DEM? [1 for YES, 2 for NO]: "))
        if info_bool in (1,2):
            break
    except ValueError:
        pass
    print("Invalid Input. Please enter 1 or 2: ")
if info_bool == 1:
    print(f"Width: {ds.RasterXSize}")
    print(f"Height: {ds.RasterYSize}")
    print(f"Number of Bands: {ds.RasterCount}")
    print(f"Statistics: {band.ComputeStatistics(False)}")
    print(f"Projection: {proj}")
while True:
    try:
        processing_bool = int(input("Do you wish to process your DEM? [1 for YES, 2 for NO]: "))
        if processing_bool in (1,2):
            break
    except ValueError:
        pass
    print("Invalid Input. Please enter 1 or 2: ")
if processing_bool == 1:
    out_dem = input("Please enter the output dataset name: ")
    while True:
        try:
            processing = int(input("Please press 1 for hillshade, 2 for slope, 3 for aspect, 4 for color-relief, 5 for TRI, 6 for TPI or 7 Roughness: "))
            if processing in range(1,8):
                break
        except ValueError:
            pass
        print("Valid Inputs 1 to 6 (Inclusive). Try again. ")
    if processing == 1:
        hillshade = gdal.DEMProcessing(out_dem, ds, "hillshade", format="GTiff", options=options)
        hillshade.FlushCache()
        hillshade = None
        print(f"{out_dem} is now saved to you computer.")
        hillshadeDS = gdal.Open(out_dem)
        hillshadeArray = hillshadeDS.GetRasterBand(1).ReadAsArray()
        plt.figure()
        plt.imshow(hillshadeArray, cmap='gray')
        plt.title("Hillshade")
    elif processing == 2:
        slope = gdal.DEMProcessing(out_dem, ds, "slope", format="GTiff",options=options)
        slope.FlushCache()
        slope = None
        print(f"{out_dem} is now saved to you computer.")
        slopeDS = gdal.Open(out_dem)
        slopeArray = slopeDS.GetRasterBand(1).ReadAsArray()
        plt.figure()
        plt.imshow(slopeArray, cmap='viridis')
        plt.colorbar(label="Slope (degrees)")
        plt.title("Slope")
    elif processing == 3:
        options = gdal.DEMProcessingOptions(computeEdges=True, alg="ZevenbergenThorne")
        aspect = gdal.DEMProcessing(out_dem, ds, "aspect", format="GTiff" ,options=options)
        aspect.FlushCache()
        aspect = None
        print(f"{out_dem} is now saved to you computer.")
        aspectDS = gdal.Open(out_dem)
        aspectArray = aspectDS.GetRasterBand(1).ReadAsArray()
        plt.figure()
        plt.imshow(aspectArray, cmap="twilight", vmin=0, vmax=360)
        plt.colorbar(label="Aspect (degrees)")
        plt.title("Aspect")
    elif processing == 4:
        colorRelief = gdal.DEMProcessing(out_dem, ds, "color-relief", format="GTiff", options=options)
        colorRelief.FlushCache()
        colorRelief = None
        print(f"{out_dem} is now saved to you computer.")
        colorReliefDS = gdal.Open(out_dem)
        colorReliefArray = colorReliefDS.GetRasterBand(1).ReadAsArray()
        plt.figure()
        plt.imshow(colorReliefArray, cmap="terrain")
        plt.colorbar(label="Elevation (m)")
        plt.title("Elevation")
    elif processing == 5:
        tRI = gdal.DEMProcessing(out_dem, ds, "TRI", format="GTiff",options=options)
        tRI.FlushCache()
        tRI = None
        print(f"{out_dem} is now saved to you computer.")
        triDS = gdal.Open(out_dem)
        triArray = triDS.GetRasterBand(1).ReadAsArray()
        plt.figure()
        plt.imshow(triArray, cmap="magma")
        plt.colorbar(label="TRI")
        plt.title("Terrain Ruggedness Index")
    elif processing == 6:
        tPI = gdal.DEMProcessing(out_dem, ds, "TPI", format="GTiff", options=options)
        tPI.FlushCache()
        tPI = None
        tpiDS = gdal.Open(out_dem)
        tpiArray = tpiDS.GetRasterBand(1).ReadAsArray()
        abs_max = np.max(np.abs(tpiArray))
        plt.figure()
        plt.imshow(tpiArray, cmap="RdBu", vmin=-abs_max, vmax=abs_max)
        plt.colorbar(label="TPI")
        plt.title("Topographic Position Index")
    elif processing == 7:
        roughness = gdal.DEMProcessing(out_dem, ds, "Roughness", format="GTiff", options=options)
        roughness.FlushCache()
        roughness = None
        print(f"{out_dem} is now saved to you computer.")
        roughnessDS = gdal.Open(out_dem)
        roughnessArray = roughnessDS.GetRasterBand(1).ReadAsArray()
        plt.figure()
        plt.imshow(roughnessArray, cmap="cividis")
        plt.colorbar(label="Roughness")
        plt.title("Surface Roughness")
print('Thank You! Goodbye!')
plt.axis("off")
plt.show()
#plt.figure()
#plt.imshow(array)