z = "/home/ad/home/m/mechenic"

import os
from datetime import datetime

import sys
sys.path.append("%s/Projects/Shared Scripts" % z)

import shapefile
from shapely.geometry import LinearRing, Polygon

from geographiclib.geodesic import Geodesic
import math
geod = Geodesic.WGS84

# ------------------------------------------------------------------------------
resolution = 9

# family = "Cervidae"
# family = "Elephantidae"
# family = "Hominidae"
# family = "Hylobatidae"
# family = "Lorisidae"
# family = "Suidae"
family = "Tarsiidae"

globalgrid = "%s/Ecosphere/ISEA3H%02i/Spatial/Vectors/" + \
             "Hexagons_ISEA3H%02i_Geodetic_0008D_WGS84.shp"
globalgrid = globalgrid % (z, resolution, resolution)

inputfolder = "%s/Ecosphere/Datasets/IUCNRL_V201901/%s" % (z, family)

outputfolder = "%s/Ecosphere/ISEA3H%02i/IUCNRL_V201901/Working/" + \
               "ISEA3H%02i_IUCNRL_V201901_%s_Fractions"
outputfolder = outputfolder % (z, resolution, resolution, family)
os.mkdir(outputfolder)

reportfile = open(os.path.join(outputfolder, "Dataset Report - Intersect.txt"),
                  "w")
# ------------------------------------------------------------------------------
startstamp = datetime.now()
outtext = "Reading %s..." % globalgrid.split("/")[-1]
print outtext
reportfile.write("%s\n" % outtext)

globalgrid = shapefile.Reader(globalgrid)

fieldlist = []
for field in globalgrid.fields[1:]:
    fieldlist.append(field[0])

hidindex = fieldlist.index("GRIDCODE")

hexagons = {}
partscount = 0
for feature in globalgrid.shapeRecords():
    hid = feature.record[hidindex]
    if hid not in hexagons:
        hexagons[hid] = []

    partslist = list(feature.shape.parts)
    pointslist = feature.shape.points
    partslist.append(len(pointslist))
    for index in range(len(partslist) - 1):

        ringpointslist = pointslist[partslist[index]:
                                    partslist[index + 1]]

        hexagons[hid].append(Polygon(ringpointslist))
        partscount += 1

endstamp = datetime.now()
outtext = "Done. %i HID(s), %i hexagon part(s) read in %0.2f second(s).\n" % (
          len(hexagons), partscount, (endstamp - startstamp).total_seconds())
print outtext
reportfile.write("%s\n" % outtext)


hidlist = hexagons.keys()
hidlist.sort()

# ------------------------------------------------------------------------------
speciesfiles = []
for item in os.listdir(inputfolder):
    if item[-3:].upper() == "SHP":
        speciesfiles.append(item)

for species in speciesfiles:
    startstamp = datetime.now()
    outtext = "Reading %s..." % species
    print outtext
    reportfile.write("%s\n" % outtext)

    inputfile = shapefile.Reader(os.path.join(inputfolder, species))

    polygons = []
    for feature in inputfile.shapeRecords():
        exterior = []
        interior = []

        partslist = list(feature.shape.parts)
        pointslist = feature.shape.points
        partslist.append(len(pointslist))
        for index in range(len(partslist) - 1):

            ringpointslist = pointslist[partslist[index]:
                                        partslist[index + 1]]

            if LinearRing(ringpointslist).is_ccw:
                interior.append(ringpointslist)
            else:
                exterior.append(ringpointslist)

        if len(exterior) != 1:
            outtext = "Error - Feature w/ %i external rings!" % len(exterior)
            print outtext
            reportfile.write("%s\n" % outtext)
        else:
            polygons.append(Polygon(exterior[0], interior))

    endstamp = datetime.now()
    outtext = "Done. %i polygons(s) read in %0.2f second(s).\n" % (
              len(polygons), (endstamp - startstamp).total_seconds())
    print outtext
    reportfile.write("%s\n" % outtext)

    # --------------------------------------------------------------------------
    startstamp = datetime.now()
    outtext = "Intersecting %s..." % species
    print outtext
    reportfile.write("%s\n" % outtext)

    intersections = {}
    for hid in hidlist:
        intersections[hid] = [[], 0.0]

        for hpart in hexagons[hid]:
            for spolygon in polygons:

                if hpart.intersects(spolygon):
                    igeometry = hpart.intersection(spolygon)

                    ipolygonlist = []
                    if igeometry.geom_type == "Polygon":
                        ipolygonlist = [igeometry]
                    elif igeometry.geom_type == "MultiPolygon":
                        ipolygonlist = list(igeometry.geoms)

                    for ipolygon in ipolygonlist:
                        intersections[hid][0].append(ipolygon)

                        gpolygon = geod.Polygon()
                        for p in list(ipolygon.exterior.coords):
                            gpolygon.AddPoint(p[1], p[0])
                        intersections[hid][1] += abs(gpolygon.Compute()[2]) / 1000000.0

                        for ipart in list(ipolygon.interiors):
                            gpolygon = geod.Polygon()
                            for p in list(ipart.coords):
                                gpolygon.AddPoint(p[1], p[0])
                            intersections[hid][1] -= abs(gpolygon.Compute()[2]) / 1000000.0

        if hid % 10000 == 0:
            print "%i HIDs intersected..." % hid

    endstamp = datetime.now()
    outtext = "Done in %0.2f second(s).\n" % (endstamp - startstamp).total_seconds()
    print outtext
    reportfile.write("%s\n" % outtext)

    # --------------------------------------------------------------------------
    outputfile = os.path.join(outputfolder, "ISEA3H%02i_" + species)
    outputfile = outputfile % resolution

    shpwriter = shapefile.Writer(shapeType = shapefile.POLYGON)
    shpwriter.field("HID", "N", 9, 0)
    shpwriter.field("I_Area_G", "N", 16, 8)

    startstamp = datetime.now()
    outtext = "Writing %s..." % outputfile.split("/")[-1]
    print outtext
    reportfile.write("%s\n" % outtext)

    hidcount = 0
    for hid in hidlist:
        if intersections[hid][1] > 0.0:
            shpwriter.record(hid, intersections[hid][1])
            hidcount += 1

            outputlist = []
            for ipolygon in intersections[hid][0]:
                epart = list(ipolygon.exterior.coords)
                if LinearRing(epart).is_ccw:
                    epart.reverse()
                outputlist.append(epart)

                for iring in list(ipolygon.interiors):
                    ipart = list(iring.coords)
                    if iring.is_ccw == False:
                        ipart.reverse()
                    outputlist.append(ipart)

            shpwriter.poly(outputlist)

    shpwriter.save(outputfile)
    
    endstamp = datetime.now()
    outtext = "Done. %i multi-part polygon(s) written in %0.2f second(s).\n" % (
              hidcount, (endstamp - startstamp).total_seconds())
    print outtext
    reportfile.write("%s\n" % outtext)

reportfile.close()