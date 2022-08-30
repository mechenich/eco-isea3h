directory = "/home/ad/home/m/mechenic/Ecosphere"
# fractionfile = "ISEA3H05_WWFTE_V02_Realm_Fractions.txt"
# fractionfile = "ISEA3H06_WWFTE_V02_Realm_Fractions.txt"
# fractionfile = "ISEA3H07_WWFTE_V02_Realm_Fractions.txt"
# fractionfile = "ISEA3H08_WWFTE_V02_Realm_Fractions.txt"
# fractionfile = "ISEA3H09_WWFTE_V02_Realm_Fractions.txt"
# fractionfile = "ISEA3H05_DSMW_V36_SoilUnits_Fractions.txt"
# fractionfile = "ISEA3H06_DSMW_V36_SoilUnits_Fractions.txt"
# fractionfile = "ISEA3H07_DSMW_V36_SoilUnits_Fractions.txt"
fractionfile = "ISEA3H08_DSMW_V36_SoilUnits_Fractions.txt"
# fractionfile = "ISEA3H09_DSMW_V36_SoilUnits_Fractions.txt"

# -----------------------------------------------------------------------------
filelist = fractionfile.split("_")
resolution = filelist[0]
dataset = filelist[1]
version = filelist[2]
subdataset = filelist[-2]

inputpath = "%s/%s/%s_%s/%s" % (directory, resolution, dataset, version,
                                fractionfile)
inputfile = open(inputpath, "r")

outputpath = "%s_Mode.txt" % inputpath.rsplit("_", 1)[0]
outputfile = open(outputpath, "w")
outputfile.write("HID\t%s_Mode" % subdataset)

# -----------------------------------------------------------------------------
attributes = []
headerlist = inputfile.readline().strip("\n").split("\t")
for header in headerlist[1:]:
    attributes.append(header.split("_")[1])

record = inputfile.readline()
while record:
    record = record.strip("\n").split("\t")    
    values = []
    for value in record[1:]:
        values.append(float(value))
    
    if sum(values) >= 0.2:
        combolist = []
        for index in range(len(attributes)):
            combolist.append([values[index], attributes[index]])
        
        combolist.sort()
        outputfile.write("\n%s\t%s" % (record[0], combolist[-1][1]))
    else:
        outputfile.write("\n%s\t-1" % record[0])

    record = inputfile.readline()

inputfile.close()
outputfile.close()
