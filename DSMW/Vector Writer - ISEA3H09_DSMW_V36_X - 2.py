z = "/home/ad/home/m/mechenic"

import os
import sys
sys.path.append("%s/Projects/Shared Scripts" % z)
import shapefile

from datetime import datetime
from shapely.geometry import LinearRing, Polygon

# -----------------------------------------------------------------------------
resolution = 9

inputpath = "%s/Ecosphere/ISEA3H%02i/DSMW_V36/Working" % (z, resolution)

hexagonpath = "%s/Ecosphere/ISEA3H%02i/Spatial/Vectors/" + \
              "Hexagons_ISEA3H%02i_Geodetic_0008D_WGS84.shp"

hexagons = shapefile.Reader(hexagonpath % (z, resolution, resolution))

fieldlist = []
for field in hexagons.fields[1:]:
    fieldlist.append(field[0])

hidindex = fieldlist.index("GRIDCODE")

# -----------------------------------------------------------------------------
units = {}
for featureindex in range(hexagons.numRecords):
    feature = hexagons.shapeRecord(featureindex)

    hid = feature.record[hidindex]
    if hid not in units:
        units[hid] = []

    # -------------------------------------------------------------------------
    partslist = list(feature.shape.parts)
    pointslist = feature.shape.points
    partslist.append(len(pointslist))
    for index in range(len(partslist) - 1):

        ringpointslist = pointslist[partslist[index]:
                                    partslist[index + 1]]

        units[hid].append(Polygon(ringpointslist).buffer(0.0001))

print "Done. %i HID(s) found.\n" % len(units)
print "SID\tRings\tCWRings\tCCWRings\tSeconds"

# -----------------------------------------------------------------------------
reportfile = open(os.path.join(inputpath, "Dataset Report - Verify.txt"), "w")
reportfile.write("SID\tRings\tCWRings\tCCWRings\tSeconds")

speciesfiles = []
for item in os.listdir(inputpath):
    if os.path.isdir(os.path.join(inputpath, item)):
        speciesfiles.append("%s/%s/%s.shp" % (inputpath, item, item.rsplit("_", 1)[0]))

for species in speciesfiles:
    startstamp = datetime.now()
    counts = [0, 0, 0]

    # -------------------------------------------------------------------------
    intersects = shapefile.Reader(species)

    fieldlist = []
    for field in intersects.fields[1:]:
        fieldlist.append(field[0])

    hidindex = fieldlist.index("HID")

    # -------------------------------------------------------------------------
    for featureindex in range(intersects.numRecords):
        feature = intersects.shapeRecord(featureindex)
        hid = feature.record[hidindex]

        partslist = list(feature.shape.parts)
        pointslist = feature.shape.points
        partslist.append(len(pointslist))

        # ---------------------------------------------------------------------
        for index in range(len(partslist) - 1):
            ringpointslist = pointslist[partslist[index]:
                                        partslist[index + 1]]

            if len(ringpointslist) > 2:
                ipolygon = Polygon(ringpointslist)

                valid = False
                for hpolygon in units[hid]:
                    if hpolygon.contains(ipolygon):
                        valid = True

                if not valid:
                    if LinearRing(ringpointslist).is_ccw:
                        counts[2] += 1
                    else:
                        counts[1] += 1

            else:
                counts[0] += 1

    # -------------------------------------------------------------------------
    endstamp = datetime.now()

    outputtext = "%s\t%i\t%i\t%i\t%0.2f" % (species.rsplit("_", 1)[1][:-4], counts[0],
                 counts[1], counts[2], (endstamp - startstamp).total_seconds())
    reportfile.write("\n%s" % outputtext)
    print outputtext

reportfile.close()