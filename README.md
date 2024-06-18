
Occupancy Ratio Calculation Tool

Overview
This Python script uses the ArcPy library to calculate the occupancy ratio of built-up areas within given field areas using spatial analysis techniques in ArcGIS. The script performs several geoprocessing tasks, including intersection, dissolve, area calculation, field calculations, and kernel density estimation. The final output is a kernel density raster that represents the occupancy ratio of built-up areas within the specified fields.

Prerequisites
- ArcGIS Desktop or ArcGIS Pro: The script requires ArcPy, which is part of ArcGIS.
- Spatial Analyst Extension: This extension is necessary for performing the Kernel Density analysis.
- Data: The script works with two main datasets:
  - A feature class representing field areas.
  - A feature class representing built-up areas.

Setup

1. Set Environment Workspace: Modify the workspace path in the `set_env` function to the path where your geodatabase and layers are stored.

2. Input Parameters: The script takes five parameters:
   - `field`: Path to the field feature class.
   - `built`: Path to the built-up area feature class.
   - `search_Radius`: Search radius for Kernel Density calculation.
   - `cell_Size`: Cell size for Kernel Density calculation.
   - `boundry`: Optional boundary feature class to limit the Kernel Density output.

Running the Script
The script can be run directly from ArcGIS by setting the parameters through the tool interface. Alternatively, you can hard-code the paths and run the script as a standalone Python script.

Code Explanation

Functions

- `set_env(workspace)`: Sets the workspace environment and allows overwriting of output files.
  
- `print_message(msg)`: Prints and logs messages for both the console and ArcGIS messages.
  
- `get_arcpy_parameters()`: Retrieves parameters set in the ArcGIS tool interface.
  
- `occupancy_ratio(field, built, search_Radius, cell_Size, boundry)`: Main function to calculate the occupancy ratio.

  The function performs the following steps:
  
  1. Add Fields: Adds a new field `Id_Field` to uniquely identify each field area.
  
  2. Calculate ID Field: Calculates the `Id_Field` based on the `OBJECTID`.
  
  3. Intersect Analysis: Intersects the `field` and `built` layers to find overlapping areas.
  
  4. Dissolve: Dissolves the intersected features based on the `Id_Field` to handle multiple built-up areas within a single field.
  
  5. Calculate Geometry: Adds and calculates area fields (`Field_Area` and `Built_Area`) for both the original field and dissolved built-up areas.
  
  6. Join and Export: Joins the dissolved built-up areas back to the field layer and exports the result as a new feature class `Occupancy`.
  
  7. Calculate Occupancy Ratio: Adds a new field `Occupancy_Ratio` and calculates the ratio of built-up area to field area.
  
  8. Kernel Density: Converts the `Occupancy` feature to points and performs Kernel Density analysis to create a density raster.
  
  9. Print Completion Message: Prints a completion message.


Output
The script produces the following outputs:
- `Occupancy` Feature Class: Contains the original field areas with added fields for built-up area and occupancy ratio.
- Kernel Density Raster: Represents the density of the occupancy ratio across the study area.

Conclusion
This tool is useful for spatial analysis of built-up areas within defined fields, helping to understand the density and distribution of built-up regions. It can be adapted and expanded for various spatial analysis applications using ArcGIS and Python.
