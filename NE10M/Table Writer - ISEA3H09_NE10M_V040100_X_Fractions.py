z = "/home/ad/home/m/mechenic"

import os
import sys
sys.path.append("%s/Projects/Shared Scripts" % z)
import shapefile

# -----------------------------------------------------------------------------
resolution = 9
attributefield = "featurecla"

workingpath = "%s/Ecosphere/ISEA3H%02i/NE10M_V040100/Working" % (z, resolution)

datasetpath = "%s/Ecosphere/Datasets/NE10M_V040100" % z

reportfile = open("%s/Dataset Report - Table.txt" % workingpath, "w")

# -----------------------------------------------------------------------------
hexagons = {}

hexagonpath = "%s/Ecosphere/ISEA3H%02i/Spatial/Vectors/" + \
              "Hexagons_ISEA3H%02i_Geodetic_0008D_WGS84.shp"
hexagonpath = hexagonpath % (z, resolution, resolution)
hexagonfile = shapefile.Reader(hexagonpath)

fieldlist = []
for field in hexagonfile.fields[1:]:
    fieldlist.append(field[0])
hidindex = fieldlist.index("GRIDCODE")
areaindex = fieldlist.index("Area_G")

for feature in hexagonfile.records():
    hid = feature[hidindex]

    if hid not in hexagons:
        hexagons[hid] = {"HTotal": 0.0}
    
    hexagons[hid]["HTotal"] += feature[areaindex]

hids = hexagons.keys()
hids.sort()

# -----------------------------------------------------------------------------
intersectfiles = []
for item in os.listdir(workingpath):
    if os.path.isdir(os.path.join(workingpath, item)):
        intersectfiles.append("%s/%s/%s.shp" % (workingpath, item, item.rsplit("_", 1)[0]))

for intersectfile in intersectfiles:
    datasettext = intersectfile.rsplit("/", 1)[1].split("_", 1)[1][:-4]

    datasetfile = "%s/%s.shp" % (datasetpath, datasettext)
    fractionsfile = "%s/ISEA3H%02i_%s_Fractions.txt" % (workingpath.rsplit("/", 1)[0], resolution, datasettext)

    # -------------------------------------------------------------------------
    if os.path.exists(fractionsfile) == False:
        attributetotals = {}

        datasetfile = shapefile.Reader(datasetfile)

        fieldlist = []
        for field in datasetfile.fields[1:]:
            fieldlist.append(field[0])
        areaindex = fieldlist.index("S_Area_G")
        attributeindex = fieldlist.index(attributefield)

        for feature in datasetfile.records():
            attribute = feature[attributeindex]

            if attribute not in attributetotals:
                attributetotals[attribute] = [0.0, 0.0]

            attributetotals[attribute][0] += feature[areaindex]

        # ---------------------------------------------------------------------
        intersectfile = shapefile.Reader(intersectfile)

        fieldlist = []
        for field in intersectfile.fields[1:]:
            fieldlist.append(field[0])
        hidindex = fieldlist.index("HID")
        attributeindex = fieldlist.index(attributefield)
        areaindex = fieldlist.index("I_Area_G")

        for feature in intersectfile.records():
            hid = feature[hidindex]
            attribute = feature[attributeindex]

            if attribute not in hexagons[hid]:
                hexagons[hid][attribute] = 0.0

            hexagons[hid][attribute] += feature[areaindex]
            attributetotals[attribute][1] += feature[areaindex]

        outtext = "%s:" % datasettext

        attributelist = attributetotals.keys()
        attributelist.sort()
        for attribute in attributelist:
            outtext += "\n%s:\t%0.6f" % (attribute, attributetotals[attribute][0] / attributetotals[attribute][1])

        print outtext
        reportfile.write("%s\n" % outtext)

        # ---------------------------------------------------------------------
        fractionsfile = open(fractionsfile, "w") 
        fractionsfile.write("HID")
        for attribute in attributelist:
            fractionsfile.write("\t%s_%s_Fraction" % (datasettext.rsplit("_", 1)[1], attribute))

        for hid in hids:
            fractionsfile.write("\n%i" % hid)

            for attribute in attributelist:
                if attribute in hexagons[hid]:
                    value = hexagons[hid][attribute] / hexagons[hid]["HTotal"]
                    if value > 1.0000001:
                        outtext = "Error:\t%i:\t%s:\t%0.6f" % (hid, attribute, value)
                        print outtext
                        reportfile.write("%s\n" % outtext) 
                else:
                    value = 0.0

                fractionsfile.write("\t%0.6f" % value)

        fractionsfile.close()

reportfile.close()