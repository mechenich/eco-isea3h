import os
import sys

resolution = int(sys.argv[1])

# ------------------------------------------------------------------------------
foldertext = "/Users/mechenic/Ecosphere"

datasettext = "WWFGLWD"
subdatasettext = "L03"
versiontext = "V01"

hextext = "ISEA3H%02i" % resolution
gridtext = "Geodetic_0008D_WGS84"

# ------------------------------------------------------------------------------
hids = {}

totalsfile = open("%s/%s/Spatial/%s_%s_RasterArea.txt" % (foldertext, hextext,
                  hextext, gridtext), "r")

for record in totalsfile.readlines()[1:]:
    record = record.strip("\n").split("\t")

    hids[int(record[0])] = {"T": float(record[1])}

totalsfile.close()

# ------------------------------------------------------------------------------
areafolder = "%s/%s/%s_%s/Working/%s_%s_%s_%s_X" % (foldertext, hextext,
             datasettext, versiontext, hextext, datasettext, versiontext,
             subdatasettext)

areafiles = []
for item in os.listdir(areafolder):
    if item[-3:].upper() == "TXT":
        areafiles.append(item)

values = []

for areafile in areafiles:
    print areafile
    areafile = open(os.path.join(areafolder, areafile), "r")

    header = areafile.readline().strip("\n").split("\t")[1:]
    headlist = []
    for head in header:
        head = int(head)
        headlist.append(head)

        if head not in values:
            values.append(head)

    record = areafile.readline()
    while record:
        record = record.strip("\n").split("\t")
        hid = int(record.pop(0))

        for index in range(len(headlist)):
            value = headlist[index]
            area = float(record[index])

            if value in hids[hid]:
                hids[hid][value] += area
            else:
                hids[hid][value] = area

        record = areafile.readline()

    areafile.close()

values.sort()

# ------------------------------------------------------------------------------
fractionfile = open("%s/%s/%s_%s/%s_%s_%s_%s_Fractions.txt" % (foldertext,
                    hextext, datasettext, versiontext, hextext, datasettext,
                    versiontext, subdatasettext), "w")

fractionfile.write("HID")
for value in values:
    fractionfile.write("\t%s_%02i_Fraction" % (subdatasettext, value))

featurefile = open("%s/%s/%s_%s/%s_%s_%s_%s_Feature.txt" % (foldertext, hextext,
                   datasettext, versiontext, hextext, datasettext, versiontext,
                   subdatasettext), "w")

featurefile.write("HID\t%s_Feature" % subdatasettext)

hidlist = hids.keys()
hidlist.sort()

for hid in hidlist:
    fractions = []

    for value in values:
        if value in hids[hid]:
            fractions.append([hids[hid][value] / hids[hid]["T"], value])
        else:
            fractions.append([0.0, value])

    fractionfile.write("\n%i" % hid)
    for fraction in fractions:
        fractionfile.write("\t%0.6f" % fraction[0])

    fractions.sort()
    if fractions[-1][0] >= 0.5:
        featurefile.write("\n%i\t%i" % (hid, fractions[-1][1]))
    else:
        featurefile.write("\n%i\t-1" % hid)

fractionfile.close()
featurefile.close()
