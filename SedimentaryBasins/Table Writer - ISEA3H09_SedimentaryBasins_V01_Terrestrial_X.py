import os

# ------------------------------------------------------------------------------
areafolder = "/Users/mechenic/Ecosphere/ISEA3H09/SedimentaryBasins_V01/" + \
             "Working/ISEA3H09_SedimentaryBasins_V01_Terrestrial_X"

areafiles = []
for text in os.listdir(areafolder):
    if text[-3:].upper() == "TXT":
        areafiles.append("%s/%s" % (areafolder, text))

# ------------------------------------------------------------------------------
classlist = ["Terrestrial"]

hids = {}
for index in range(1, 196832 + 1):
    hids[index] = []

    for subindex in range(len(classlist) + 1):
        hids[index].append(0.0)

# ------------------------------------------------------------------------------
for areafile in areafiles:
    areafile = open(areafile, "r")

    header = []
    for text in areafile.readline().strip("\n").split("\t")[1:]:
        header.append(int(text))

    record = areafile.readline()
    while record:
        record = record.strip("\n").split("\t")

        hid = int(record[0])
        record = record[1:]

        for index in range(len(header)):
            hids[hid][header[index]] += float(record[index])

        record = areafile.readline()

    areafile.close()

# ------------------------------------------------------------------------------
outputfolder = "/Users/mechenic/Ecosphere/ISEA3H09/SedimentaryBasins_V01"

fractionsfile = open("%s/ISEA3H09_SedimentaryBasins_V01_Terrestrial_Fractions.txt"
                     % outputfolder, "w")
fractionsfile.write("HID")
for text in classlist:
    fractionsfile.write("\t%s_Fraction" % text)

for hid in range(1, 196832 + 1):
    totalarea = sum(hids[hid])

    fractionsfile.write("\n%i" % hid)
    for area in hids[hid][1:]:
        fractionsfile.write("\t%0.6f" % (area / totalarea))

fractionsfile.close()
