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

import pickle

# ------------------------------------------------------------------------------
resolution = 9
hidranges = [[     1, 100000],
             [100001, 196832]]
hidrange = 1

pickleresolution = 8

globalgrid = "%s/Ecosphere/ISEA3H%02i/Spatial/Vectors/" + \
             "Hexagons_ISEA3H%02i_Geodetic_0008D_WGS84.shp"
globalgrid = globalgrid % (z, resolution, resolution)

inputfolder = "%s/Ecosphere/Datasets/DSMW_V36" % (z)
inputfield = "DOMSOI"
speciesfiles = ["DSMW_V36_SoilUnits.shp"]

outputfolder = "%s/Ecosphere/ISEA3H%02i/DSMW_V36/Working"
outputfolder = outputfolder % (z, resolution)

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
for featureindex in range(globalgrid.numRecords):
    feature = globalgrid.shapeRecord(featureindex)
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

# ------------------------------------------------------------------------------
for species in speciesfiles:

    # --------------------------------------------------------------------------
    picklefile = "%s/Projects/Ecosphere Analysis/Spatial Statistics/HID " + \
                 "List - ISEA3H%02i > ISEA3H%02i_%s.pkl"
    picklefile = picklefile % (z, pickleresolution, resolution, species[:-4])

    picklefile = open(picklefile, "rb")
    hidlist = pickle.load(picklefile)
    picklefile.close()
    # --------------------------------------------------------------------------

    startstamp = datetime.now()
    outtext = "Reading %s..." % species
    print outtext
    reportfile.write("%s\n" % outtext)

    inputfile = shapefile.Reader(os.path.join(inputfolder, species))
    fieldlist = []
    for field in inputfile.fields[1:]:
        fieldlist.append(field[0])

    polygons = {}
    polygoncount = 0
    for featureindex in range(inputfile.numRecords):
        feature = inputfile.shapeRecord(featureindex)
        attribute = feature.record[fieldlist.index(inputfield)]
        if attribute not in polygons:
            polygons[attribute] = []

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
            polygons[attribute].append(Polygon(exterior[0], interior))
            polygoncount += 1

    endstamp = datetime.now()

    attributelist = polygons.keys()
    attributelist.sort()
    outtext = "%i unique attribute(s) found:" % len(attributelist)
    for attribute in attributelist:
        outtext += "\n%s" % attribute
    print outtext
    reportfile.write("%s\n" % outtext)

    outtext = "Done. %i polygons(s) read in %0.2f second(s).\n" % (
              polygoncount, (endstamp - startstamp).total_seconds())
    print outtext
    reportfile.write("%s\n" % outtext)

    # --------------------------------------------------------------------------
    outputfile = "%s/ISEA3H%02i_%s_Fractions"
    outputfile = outputfile % (outputfolder, resolution, species[:-4])

    if os.path.exists(outputfile) == False:
        os.mkdir(outputfile)

    outputfile = "%s/ISEA3H%02i_%s_HID%i.shp" % (outputfile, resolution, species[:-4],
                                                 hidranges[hidrange][0])
    startstamp = datetime.now()
    outtext = "Intersecting %s..." % species
    print outtext
    reportfile.write("%s\n" % outtext)

    intersections = {}
    for hid in range(hidranges[hidrange][0], hidranges[hidrange][1] + 1):
        intersections[hid] = {}
        for attribute in attributelist:
            intersections[hid][attribute] = [[], 0.0]

        # ----------------------------------------------------------------------
        if hid in hidlist:
        # ----------------------------------------------------------------------

            for hpart in hexagons[hid]:
                for attribute in attributelist:
                    for spolygon in polygons[attribute]:

                        if hpart.intersects(spolygon):
                            igeometry = hpart.intersection(spolygon)

                            ipolygonlist = []
                            if igeometry.geom_type == "Polygon":
                                ipolygonlist = [igeometry]
                            elif igeometry.geom_type == "MultiPolygon":
                                ipolygonlist = list(igeometry.geoms)

                            for ipolygon in ipolygonlist:
                                intersections[hid][attribute][0].append(ipolygon)

                                gpolygon = geod.Polygon()
                                for p in list(ipolygon.exterior.coords):
                                    gpolygon.AddPoint(p[1], p[0])
                                intersections[hid][attribute][1] += abs(gpolygon.Compute()[2]) / 1000000.0

                                for ipart in list(ipolygon.interiors):
                                    gpolygon = geod.Polygon()
                                    for p in list(ipart.coords):
                                        gpolygon.AddPoint(p[1], p[0])
                                    intersections[hid][attribute][1] -= abs(gpolygon.Compute()[2]) / 1000000.0

        if hid % 1000 == 0:
            print "%i HIDs intersected..." % hid

    endstamp = datetime.now()
    outtext = "Done in %0.2f second(s).\n" % (endstamp - startstamp).total_seconds()
    print outtext
    reportfile.write("%s\n" % outtext)

    # --------------------------------------------------------------------------
    shpwriter = shapefile.Writer(shapeType = shapefile.POLYGON)
    shpwriter.field("HID", "N", 9, 0)
    shpwriter.field(*inputfile.fields[fieldlist.index(inputfield) + 1])
    shpwriter.field("I_Area_G", "N", 16, 8)

    startstamp = datetime.now()
    outtext = "Writing %s..." % outputfile.split("/")[-1]
    print outtext
    reportfile.write("%s\n" % outtext)

    hidcount = 0
    for hid in range(hidranges[hidrange][0], hidranges[hidrange][1] + 1):
        hidtf = False
        for attribute in attributelist:
            if intersections[hid][attribute][1] > 0.0:
                shpwriter.record(hid, attribute, intersections[hid][attribute][1])
                hidtf = True

                outputlist = []
                for ipolygon in intersections[hid][attribute][0]:
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

        if hidtf:
            hidcount += 1

    shpwriter.save(outputfile)

    endstamp = datetime.now()
    outtext = "Done. %i multi-part polygon(s) written in %0.2f second(s).\n" % (
              hidcount, (endstamp - startstamp).total_seconds())
    print outtext
    reportfile.write("%s\n" % outtext)

reportfile.close()