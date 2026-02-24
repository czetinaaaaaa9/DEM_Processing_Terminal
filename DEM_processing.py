#### DEM Processing Script ####

### These are the dependencies: Python3, osgeo, numpy and matlib. ###

from osgeo import gdal
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
gdal.UseExceptions()

dem = input("Please Enter the DEM you wish to access: ")
ds = gdal.Open(dem)
band = ds.GetRasterBand(1)
array = band.ReadAsArray()
stats = band.ComputeStatistics(False)

### User is asked if information on the DEM is to be displayed. ###

while True:
    try:
        info_bool = int(input("Do you wish to view information on the DEM? [1 for YES, 2 for NO]: "))
        if info_bool in (1,2):
            break
    except ValueError:
        pass
    print("Invalid Input. Please enter 1 or 2: ")
if info_bool == 1:
    proj = ds.GetProjection()
    print(f"Width: {ds.RasterXSize}")
    print(f"Height: {ds.RasterYSize}")
    print(f"Number of Bands: {ds.RasterCount}")
    print(f"""
          Min: {stats[0]}
          Max: {stats[1]}
          Mean: {stats[2]}
          SD: {stats[3]}   
          """)
    print(f"Projection: {proj}")
    
### User is asked if the DEM is to be processed or not. ###   
    
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
    options = gdal.DEMProcessingOptions(computeEdges=True)
    while True:
        try:
            processing = int(input("Please press 1 for hillshade, 2 for slope, 3 for aspect, 4 for color-relief, 5 for TRI, 6 for TPI or 7 Roughness: "))
            if processing in range(1,8):
                break
        except ValueError:
            pass
        print("Valid Inputs 1 to 7 (Inclusive). Try again. ")
    if processing == 1:
        hillshade = gdal.DEMProcessing(out_dem, ds, "hillshade", format="GTiff", options=options)
        hillshade.FlushCache()
        hillshade = None
        print(f"{out_dem} is now saved to you computer.")
        hillshadeDS = gdal.Open(out_dem)
        hillshadeArray = hillshadeDS.GetRasterBand(1).ReadAsArray()
        plt.figure()
        plt.axis("off")
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
        plt.axis("off")
        plt.imshow(slopeArray, cmap='viridis')
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
        plt.axis("off")
        plt.imshow(aspectArray, cmap="twilight", vmin=0, vmax=360)
        plt.title("Aspect")
    elif processing == 4:
        color_config = f"""
        {stats[0]}   green
        {(stats[0]+ stats[1])/2:.2f}   brown
        {stats[1]}   white
        nv           0 0 0 0
        """
        with open("my_colors.txt", "w") as f:
            f.write(color_config)
        options = gdal.DEMProcessingOptions(computeEdges=True, colorFilename="my_colors.txt")
        colorRelief = gdal.DEMProcessing(out_dem, ds, "color-relief", format="GTiff", options=options)
        colorRelief.FlushCache()
        colorRelief = None
        print(f"{out_dem} is now saved to you computer.")
        colorReliefDS = gdal.Open(out_dem)
        r = colorReliefDS.GetRasterBand(1).ReadAsArray()
        g = colorReliefDS.GetRasterBand(2).ReadAsArray()
        b = colorReliefDS.GetRasterBand(3).ReadAsArray()
        rgb_array = np.dstack((r, g, b))
        plt.figure()
        plt.axis("off")
        plt.imshow(rgb_array)
        plt.title("Elevation")
    elif processing == 5:
        tRI = gdal.DEMProcessing(out_dem, ds, "TRI", format="GTiff",options=options)
        tRI.FlushCache()
        tRI = None
        print(f"{out_dem} is now saved to you computer.")
        triDS = gdal.Open(out_dem)
        triArray = triDS.GetRasterBand(1).ReadAsArray()
        plt.figure()
        plt.axis("off")
        plt.imshow(triArray, cmap="magma")
        plt.title("Terrain Ruggedness Index")
    elif processing == 6:
        tPI = gdal.DEMProcessing(out_dem, ds, "TPI", format="GTiff", options=options)
        tPI.FlushCache()
        tPI = None
        tpiDS = gdal.Open(out_dem)
        tpiArray = tpiDS.GetRasterBand(1).ReadAsArray()
        abs_max = np.max(np.abs(tpiArray))
        plt.figure()
        plt.axis("off")
        plt.imshow(tpiArray, cmap="RdBu", vmin=-abs_max, vmax=abs_max)
        plt.title("Topographic Position Index")
    elif processing == 7:
        roughness = gdal.DEMProcessing(out_dem, ds, "Roughness", format="GTiff", options=options)
        roughness.FlushCache()
        roughness = None
        print(f"{out_dem} is now saved to you computer.")
        roughnessDS = gdal.Open(out_dem)
        roughnessArray = roughnessDS.GetRasterBand(1).ReadAsArray()
        plt.figure()
        plt.axis("off")
        plt.imshow(roughnessArray, cmap="cividis")
        plt.title("Surface Roughness")
        
### In the terminal, the script stops runnning until the user exits the output display. ###
        
print('Thank You! Goodbye!')
plt.show()