import arcpy
from arcpy import env
from arcpy.sa import *

def set_env(workspace):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = workspace

def print_message(msg):
    print(msg)
    arcpy.AddMessage(msg)

def get_arcpy_parameters():
    field = arcpy.GetParameterAsText(0)
    built = arcpy.GetParameterAsText(1)
    search_Radius = arcpy.GetParameterAsText(2)
    cell_Size = arcpy.GetParameterAsText(3)
    boundry = arcpy.GetParameterAsText(4)

    return field, built, search_Radius, cell_Size, boundry


def occupancy_ratio(field, built, search_Radius, cell_Size, boundry):
    if field == "":
        field = r"D:\Advanced Spatial Analysis\GDB\Layers\Layers\Overlay.gdb\Arse_1"

    if built == "":
        built = r"D:\Advanced Spatial Analysis\GDB\Layers\Layers\Overlay.gdb\Ayan_1"


    #Create new field in attribute table of Field layer labeling "Id_Field" and calculate it
    arcpy.AddField_management(field, "Id_Field", "LONG")
    arcpy.CalculateField_management(field, "Id_Field", "!OBJECTID! + 1", "PYTHON3")

    arcpy.Intersect_analysis([field, built], "Built_Intersect")

    #Perform Dissovle to solve multiple Built in one Field
    arcpy.Dissolve_management("Built_Intersect", "Built_Intersect_Dissolve", "Id_Field")

    #Create new field for both Field and Built layer to calculate the geometry of them
    arcpy.AddField_management(field, "Field_Area", "DOUBLE")
    arcpy.AddField_management("Built_Intersect_Dissolve", "Built_Area", "DOUBLE")
    arcpy.CalculateGeometryAttributes_management(field, [["Field_Area", "AREA"]], "METERS")
    arcpy.CalculateGeometryAttributes_management("Built_Intersect_Dissolve", [["Built_Area", "AREA"]], "METERS")

    #Join the attribute table of Built_Intersect_Dissolve layer to Field layer and export a new layer from it
    field_join_table = arcpy.AddJoin_management(field, "Id_Field", "Built_Intersect_Dissolve", "Id_Field")
    arcpy.ExportFeatures_conversion(field_join_table, "Occupancy")

    #Create a field name Occupancy Ratio then Calculate the Occupancy Ratio based on the formula
    arcpy.AddField_management("Occupancy", "Occupancy_Ratio", "DOUBLE")
    arcpy.CalculateField_management("Occupancy", "Occupancy_Ratio", "!Built_Area! / !Field_Area! * 100", "PYTHON3")

    arcpy.FeatureToPoint_management("Occupancy", "Occupancy_Points")
    arcpy.KernelDensity.sa('Occupancy_Ratio_Points', 'Occupancy_Ratio', cell_Size, search_Radius, 'HECTARES', 'DENSITIES', 'PLANAR', boundry)

    print_message ("Script Completed!")



if __name__ == '__main__':
    set_env(r"D:\Advanced Spatial Analysis\Advanced Spatial Analysis\Advanced Spatial Analysis.gdb")
    field, built, search_Radius, cell_Size, boundry = get_arcpy_parameters()
    occupancy_ratio(field, built, search_Radius, cell_Size, boundry)








