import arcpy,json

feat = arcpy.GetParameterAsText(0)
where = arcpy.GetParameterAsText(1)

with arcpy.da.SearchCursor(feat,["Shape@JSON"],where) as cursor:
    for row in cursor:
        js = json.loads(row[0])
        arcpy.AddMessage("Point Count : {0}".format(len(js["rings"][0])))
        arcpy.AddMessage(js)
