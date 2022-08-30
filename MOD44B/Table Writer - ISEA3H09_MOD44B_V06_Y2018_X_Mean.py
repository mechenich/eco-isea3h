import os

# ------------------------------------------------------------------------------
foldertext = "/Users/mechenic/Ecosphere"

datasettext = "MCD12Q1"
subdatasettext = "IGBP"
versiontext = "V06"
yeartext = "Y2001"

hextext = "ISEA3H05"
gridtext = "Sinusoidal_500M_WGS84"

minimum = 1
maximum = 16

# ------------------------------------------------------------------------------
hids = {}

totalsfile = open("%s/%s/Spatial/%s_%s_Count.txt" % (foldertext, hextext,
                  hextext, gridtext), "r")

for record in totalsfile.readlines()[1:]:
    record = record.strip("\n").split("\t")

    hids[int(record[0])] = {"T": int(record[1])}

totalsfile.close()

# ------------------------------------------------------------------------------
countfolder = "%s/%s/%s_%s/Working/%s_%s_%s_%s_%s_X" % (foldertext, hextext,
              datasettext, versiontext, hextext, datasettext, versiontext,
              yeartext, subdatasettext)

countfiles = []
for item in os.listdir(countfolder):
    if item[-3:].upper() == "TXT":
        countfiles.append(item)

for countfile in countfiles:
    print countfile
    countfile = open(os.path.join(countfolder, countfile), "r")

    for record in countfile.readlines()[1:]:
        record = record.strip("\n").split("\t")

        hid = int(record[0])
        value = int(record[1])
        count = int(record[2])

        if hid != 0 and value >= minimum and value <= maximum:
            if value not in hids[hid]:
                hids[hid][value] = 0

            hids[hid][value] += count

    countfile.close()
    
# ------------------------------------------------------------------------------
fractionfile = open("%s/%s/%s_%s/%s_%s_%s_%s_%s_Fractions.txt" % (foldertext,
                    hextext, datasettext, versiontext, hextext, datasettext,
                    versiontext, yeartext, subdatasettext), "w")

fractionfile.write("HID")
for value in range(minimum, maximum + 1):
    fractionfile.write("\t%s_%02i_Fraction" % (subdatasettext, value))

modefile = open("%s/%s/%s_%s/%s_%s_%s_%s_%s_Mode.txt" % (foldertext, hextext,
                datasettext, versiontext, hextext, datasettext, versiontext,
                yeartext, subdatasettext), "w")

modefile.write("HID\t%s_Mode" % subdatasettext)

hidlist = hids.keys()
hidlist.sort()

for hid in hidlist:
    fractions = []
    total = 0

    for value in range(minimum, maximum + 1):
        if value in hids[hid]:
            fractions.append([hids[hid][value] / float(hids[hid]["T"]), value])
            total += hids[hid][value]
        else:
            fractions.append([0.0, value])

    fractionfile.write("\n%i" % hid)
    for fraction in fractions:
        fractionfile.write("\t%0.6f" % fraction[0])

    if (total / float(hids[hid]["T"])) >= 0.2:
        fractions.sort()
        modefile.write("\n%i\t%i" % (hid, fractions[-1][1]))
    else:
        modefile.write("\n%i\t-1" % hid)

fractionfile.close()
modefile.close()
