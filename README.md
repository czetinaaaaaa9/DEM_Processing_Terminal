# DEM Processing Script

**An interactive command-line tool to explore and process Digital Elevation Models (DEMs) using GDAL.**

This script lets you load any GeoTIFF DEM, view its metadata and statistics, and instantly generate and visualize 7 common terrain products.
---

## Features

- Load any GDAL-supported DEM (GeoTIFF recommended)
- Display raster information (dimensions, bands, min/max/mean/SD, projection)
- One-click generation of 7 terrain derivatives:
  1. **Hillshade**
  2. **Slope** (in degrees)
  3. **Aspect** (0–360°, using Zevenbergen & Thorne algorithm)
  4. **Color-relief** (custom green → brown → white elevation ramp)
  5. **TRI** (Terrain Ruggedness Index)
  6. **TPI** (Topographic Position Index)
  7. **Roughness**
- Automatically saves the result as a new GeoTIFF (make sure the output DEM name ends with .tif!!!!)
- Instantly displays the output using Matplotlib (with appropriate colormaps)
- No configuration files needed (temporary color table is auto-generated)

---

## Requirements

- **Python 3.8+**
- `osgeo` (GDAL Python bindings)
- `numpy`
- `matplotlib`

### Recommended Installation (conda - easiest)

```bash
conda create -n dem-processing python=3.11
conda activate dem-processing
conda install -c conda-forge gdal numpy matplotlib
```

---

## Usage 

1. Save the script
2. Run it on your terminal
   ```bash
   python3 savedScriptName.py
   ```
3. Follow on screen prompts:
   - Enter the path to your DEM file
   - Choose whether to view DEM information
   - Choose whether to process the DEM
   - Enter desired output filename (e.g. rockies_hillshade.tif)
   - Select processing type (1–7)
The file is saved in the current folder and a plot window opens.
Close the plot window to exit the script.

---

## Notes

- The script uses matplotlib.use("TkAgg") for reliable GUI display.
- For color-relief, a temporary file my_colors.txt is created in the working directory (automatically overwritten).
- Best results for slope, aspect, TRI, TPI, and roughness are obtained when the DEM is in a projected coordinate system (meters) rather than geographic (degrees).
- The script will wait for you to close the Matplotlib window before exiting.

--- 

## Future Imporvements

- Add argument parsing for non-interactive use (--input, --output, --process 1)
- Add option to reproject
- Support batch processing of multiple DEMs
- Option to save the plot as PNG/PDF
- Better error handling for invalid DEMs or missing GDAL drivers


