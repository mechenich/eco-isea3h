z = "/home/ad/home/m/mechenic"

import os
import sys
sys.path.append("%s/Projects/Shared Scripts" % z)
import shapefile

from datetime import datetime
from shapely.geometry import LinearRing, Polygon

# -----------------------------------------------------------------------------
resolution = 9

# family = "Abrocomidae"
# family = "Acrobatidae"
# family = "Ailuridae"
# family = "Anomaluridae"
# family = "Antilocapridae"
# family = "Aotidae"
# family = "Aplodontiidae"
# family = "Atelidae"
# family = "Bathyergidae"
# family = "Bovidae"
# family = "Bradypodidae"
# family = "Burramyidae"
# family = "Caenolestidae"
# family = "Callitrichidae"
# family = "Calomyscidae"
# family = "Camelidae"
# family = "Canidae"
# family = "Capromyidae"
# family = "Castoridae"
# family = "Caviidae"
# family = "Cebidae"
# family = "Cercopithecidae"
# family = "Cervidae"
# family = "Cheirogaleidae"
# family = "Chinchillidae"
# family = "Chrysochloridae"
# family = "Craseonycteridae"
# family = "Cricetidae"
# family = "Ctenodactylidae"
# family = "Ctenomyidae"
# family = "Cuniculidae"
# family = "Cyclopedidae"
# family = "Cynocephalidae"
# family = "Dasypodidae"
# family = "Dasyproctidae"
# family = "Dasyuridae"
# family = "Daubentoniidae"
# family = "Diatomyidae"
# family = "Didelphidae"
# family = "Dinomyidae"
# family = "Dipodidae"
# family = "Echimyidae"
# family = "Elephantidae"
# family = "Emballonuridae"
# family = "Equidae"
# family = "Erethizontidae"
# family = "Erinaceidae"
# family = "Eupleridae"
# family = "Felidae"
# family = "Furipteridae"
# family = "Galagidae"
# family = "Geomyidae"
# family = "Giraffidae"
# family = "Gliridae"
# family = "Herpestidae"
# family = "Heteromyidae"
# family = "Hippopotamidae"
# family = "Hipposideridae"
# family = "Hominidae"
# family = "Hyaenidae"
# family = "Hylobatidae"
# family = "Hypsiprymnodontidae"
# family = "Hystricidae"
# family = "Indriidae"
# family = "Lemuridae"
# family = "Lepilemuridae"
# family = "Leporidae"
# family = "Lorisidae"
# family = "Macropodidae"
# family = "Macroscelididae"
# family = "Manidae"
# family = "Megadermatidae"
# family = "Megalonychidae"
# family = "Mephitidae"
# family = "Microbiotheriidae"
# family = "Miniopteridae"
# family = "Molossidae"
# family = "Mormoopidae"
# family = "Moschidae"
# family = "Muridae"
# family = "Mustelidae"
# family = "Myocastoridae"
# family = "Myrmecobiidae"
# family = "Myrmecophagidae"
# family = "Mystacinidae"
# family = "Myzopodidae"
# family = "Nandiniidae"
# family = "Natalidae"
# family = "Nesomyidae"
# family = "Noctilionidae"
# family = "Notoryctidae"
# family = "Nycteridae"
# family = "Ochotonidae"
# family = "Octodontidae"
# family = "Ornithorhynchidae"
# family = "Orycteropodidae"
# family = "Pedetidae"
# family = "Peramelidae"
# family = "Petauridae"
# family = "Petromuridae"
# family = "Phalangeridae"
# family = "Phascolarctidae"
# family = "Phyllostomidae"
# family = "Pitheciidae"
# family = "Platacanthomyidae"
# family = "Potoroidae"
# family = "Prionodontidae"
# family = "Procaviidae"
# family = "Procyonidae"
# family = "Pseudocheiridae"
# family = "Pteropodidae"
# family = "Ptilocercidae"
# family = "Rhinocerotidae"
# family = "Rhinolophidae"
# family = "Rhinopomatidae"
# family = "Sciuridae"
# family = "Solenodontidae"
# family = "Soricidae"
# family = "Spalacidae"
# family = "Suidae"
# family = "Tachyglossidae"
# family = "Talpidae"
# family = "Tapiridae"
family = "Tarsiidae"
# family = "Tarsipedidae"
# family = "Tayassuidae"
# family = "Tenrecidae"
# family = "Thryonomyidae"
# family = "Thylacomyidae"
# family = "Thyropteridae"
# family = "Tragulidae"
# family = "Tupaiidae"
# family = "Ursidae"
# family = "Vespertilionidae"
# family = "Viverridae"
# family = "Vombatidae"

# -----------------------------------------------------------------------------
hexagonpath = "%s/Ecosphere/ISEA3H%02i/Spatial/Vectors/" + \
              "Hexagons_ISEA3H%02i_Geodetic_0008D_WGS84.shp"

hexagons = shapefile.Reader(hexagonpath % (z, resolution, resolution))

fieldlist = []
for field in hexagons.fields[1:]:
    fieldlist.append(field[0])

hidindex = fieldlist.index("GRIDCODE")

# -----------------------------------------------------------------------------
units = {}
for feature in hexagons.shapeRecords():

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
inputpath = "%s/Ecosphere/ISEA3H%02i/IUCNRL_V201901/Working/" + \
            "ISEA3H%02i_IUCNRL_V201901_%s_Fractions"
inputpath = inputpath % (z, resolution, resolution, family)

reportfile = open(os.path.join(inputpath, "Dataset Report - Verify.txt"), "w")
reportfile.write("SID\tRings\tCWRings\tCCWRings\tSeconds")

speciesfiles = []
for item in os.listdir(inputpath):
    if item[-3:].upper() == "SHP":
        speciesfiles.append(os.path.join(inputpath, item))

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
    for feature in intersects.shapeRecords():
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

    outputtext = "%s\t%i\t%i\t%i\t%0.2f" % (int(species[-13:-4]), counts[0],
                 counts[1], counts[2], (endstamp - startstamp).total_seconds())
    reportfile.write("\n%s" % outputtext)
    print outputtext

reportfile.close()