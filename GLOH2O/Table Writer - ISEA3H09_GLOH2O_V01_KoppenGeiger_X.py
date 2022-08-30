import os

# ------------------------------------------------------------------------------
areafolder = "/Users/mechenic/Ecosphere/ISEA3H09/GLOH2O_V01/Working/" + \
             "ISEA3H09_GLOH2O_V01_KoppenGeiger_X"

areafiles = []
for text in os.listdir(areafolder):
    if text[-3:].upper() == "TXT":
        areafiles.append("%s/%s" % (areafolder, text))

# ------------------------------------------------------------------------------
classlist = ["Af", "Am", "Aw", "BWh", "BWk", "BSh", "BSk", "Csa", "Csb", "Csc",
             "Cwa", "Cwb", "Cwc", "Cfa", "Cfb", "Cfc", "Dsa", "Dsb", "Dsc",
             "Dsd", "Dwa", "Dwb", "Dwc", "Dwd", "Dfa", "Dfb", "Dfc", "Dfd",
             "ET", "EF"]
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
outputfolder = "/Users/mechenic/Ecosphere/ISEA3H09/GLOH2O_V01"

fractionsfile = open("%s/ISEA3H09_GLOH2O_V01_KoppenGeiger_Fractions.txt"
                     % outputfolder, "w")
fractionsfile.write("HID")
for text in classlist:
    fractionsfile.write("\t%s" % text)

modefile = open("%s/ISEA3H09_GLOH2O_V01_KoppenGeiger_Mode.txt" % outputfolder,
                "w")
modefile.write("HID\tKoppenGeiger_Mode")

for hid in range(1, 196832 + 1):
    totalarea = sum(hids[hid])

    fractionsfile.write("\n%i" % hid)
    for area in hids[hid][1:]:
        fractionsfile.write("\t%0.4f" % (area / totalarea))

    modefile.write("\n%i" % hid)
    if hids[hid][0] / totalarea < 0.8:
        maxarea = max(hids[hid][1:])
        modefile.write("\t%s" % classlist[hids[hid][1:].index(maxarea)])
    else:
        modefile.write("\tNA")

fractionsfile.close()
modefile.close()
