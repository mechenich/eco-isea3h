z = "/home/ad/home/m/mechenic"

import os
import sys
sys.path.append("%s/Projects/Shared Scripts" % z)
import shapefile

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
consolefile = open("%s/Working/Console Output.txt" % z, "w")

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

# -----------------------------------------------------------------------------
stotals = {}

intersectpath = "%s/Ecosphere/ISEA3H%02i/IUCNRL_V201901/Working/" + \
                "ISEA3H%02i_IUCNRL_V201901_%s_Fractions"
intersectpath = intersectpath % (z, resolution, resolution, family)

intersectfiles = []
for item in os.listdir(intersectpath):
    if item[-3:].upper() == "SHP":
        intersectfiles.append(item)

for intersectfile in intersectfiles:
    sid = intersectfile.split("_")[3].split(".")[0]
    stotals[sid] = [0.0, 0.0]

    # --------------------------------------------------------------------------
    speciespath = "%s/Ecosphere/Datasets/IUCNRL_V201901/%s/%s" % (z, family,
                  intersectfile[9:])
    speciesfile = shapefile.Reader(speciespath)

    fieldlist = []
    for field in speciesfile.fields[1:]:
        fieldlist.append(field[0])
    areaindex = fieldlist.index("S_Area_G")

    for feature in speciesfile.records():
        stotals[sid][0] += feature[areaindex]

    # --------------------------------------------------------------------------
    intersectfile = shapefile.Reader("%s/%s" % (intersectpath, intersectfile))

    fieldlist = []
    for field in intersectfile.fields[1:]:
        fieldlist.append(field[0])

    hidindex = fieldlist.index("HID")
    areaindex = fieldlist.index("I_Area_G")

    for feature in intersectfile.records():
        hid = feature[hidindex]
        if sid not in hexagons[hid]:
            hexagons[hid][sid] = 0.0

        hexagons[hid][sid] += feature[areaindex]
        stotals[sid][1] += feature[areaindex]

    outtext = "%s - %0.6f" % (sid, stotals[sid][0] / stotals[sid][1])
    print outtext
    consolefile.write("%s\n" % outtext)

# -----------------------------------------------------------------------------
hids = hexagons.keys()
hids.sort()

sids = stotals.keys()
sids.sort()

fractionspath = "%s/Ecosphere/ISEA3H%02i/IUCNRL_V201901/" + \
                "ISEA3H%02i_IUCNRL_V201901_%s_Fractions.txt"
fractionsfile = open(fractionspath % (z, resolution, resolution, family), "w")

fractionsfile.write("HID")
for sid in sids:
    fractionsfile.write("\t%s_Fraction" % sid)

for hid in hids:
    fractionsfile.write("\n%i" % hid)

    for sid in sids:
        if sid in hexagons[hid]:
            value = hexagons[hid][sid] / hexagons[hid]["HTotal"]
            if value > 1.0000001:
                outtext = "Error - %s - %i - %0.6f" % (sid, hid, value)
                print outtext
                consolefile.write("%s\n" % outtext) 
        else:
            value = 0.0

        fractionsfile.write("\t%0.6f" % value)

fractionsfile.close()
consolefile.close()