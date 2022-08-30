import os

# directory = "ISEA3H08_ENVIREM30AS_V0100_Climate_Mean"
# directory = "ISEA3H08_ENVIREM30AS_V0100_Topography_Mean"
# directory = "ISEA3H09_ENVIREM30AS_V0100_Climate_Mean"
# directory = "ISEA3H09_ENVIREM30AS_V0100_Topography_Mean"
# directory = "ISEA3H06_WorldClim30AS_V02_BIO_Mean"
# directory = "ISEA3H07_WorldClim30AS_V02_BIO_Mean"
# directory = "ISEA3H08_WorldClim30AS_V02_BIO_Mean"
# directory = "ISEA3H09_WorldClim30AS_V02_BIO_Mean"
directory = "ISEA3H09_MOD44B_V06_Y2018_VCF_Mean"

# -----------------------------------------------------------------------------
directorylist = directory.split("_")
resolution = directorylist[0]
dataset = directorylist[1]
version = directorylist[2]
subdataset = directorylist[3]

workingfolder = "/home/ad/home/m/mechenic/Ecosphere/%s/%s_%s/Working/%s" % (
                resolution, dataset, version, directory)
outputfile = "/home/ad/home/m/mechenic/Ecosphere/%s/%s_%s/%s.txt" % (
                resolution, dataset, version, directory)
hids = {}

for inputfile in os.listdir(workingfolder):
    print inputfile
    inputfile = open("%s/%s" % (workingfolder, inputfile), "r")

    attributes = []
    header = inputfile.readline().strip("\n").split("\t")
    for head in header[1:]:
        attributes.append(head)

    # -------------------------------------------------------------------------    
    record = inputfile.readline()
    while record:
        record = record.strip("\n").split("\t")

        hid = int(record.pop(0))
        if hid not in hids:
            hids[hid] = {}

        for index in range(len(attributes)):
            hids[hid][attributes[index]] = record[index]

        record = inputfile.readline()

    inputfile.close()

# -----------------------------------------------------------------------------
hidlist = hids.keys()
hidlist.sort()

attributelist = hids[hidlist[0]].keys()
attributelist.sort()

outputfile = open(outputfile, "w")

outputfile.write("HID")
for attribute in attributelist:
    outputfile.write("\t%s" % attribute)

for hid in hidlist:
    outputfile.write("\n%i" % hid)
    for attribute in attributelist:
        outputfile.write("\t%s" % hids[hid][attribute])

outputfile.close()
    