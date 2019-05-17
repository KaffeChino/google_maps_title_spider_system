#! C:\\Python27\\ArcGIS10.2\\
import os
import arcpy


def definePro(z):
    os.chmod("D:\\Program Files\\OneDrive\\Code\\python\\Artical\\temp\\")
    infc = r"Merge_{}.jpg".format(z)
    sr = arcpy.SpatialReference("WGS 1984")
    arcpy.DefineProjection_management(infc, sr)
