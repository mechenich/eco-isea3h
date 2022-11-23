resolution = 9

dataset = "CCSM4"
sdsgroup = "ETCCDI"

scenario = "RCP85"
year1 = "Y2061"
year2 = "Y2080"

neighbors = 10

# -----------------------------------------------------------------------------
import os
import pickle

z = "/home/ad/home/m/mechenic/"

weightspath = "%s/Projects/Ecosphere Analysis/Spatial Statistics/" + \
              "Nearest Neighbors - ISEA3H%02i - %s.pkl"
weightsfile = open(weightspath % (z, resolution, dataset), "rb")

weights = pickle.load(weightsfile)

weightsfile.close()

# -----------------------------------------------------------------------------
hidlist = weights.keys()
hidlist.sort()

sdsvalues = {}
for hid in hidlist:
    sdsvalues[hid] = {}

# -----------------------------------------------------------------------------
valuespath = "%s/Projects/Shared Datasets/%s/%s/Means" % (z, dataset, scenario)

for valuesfile in os.listdir(valuespath):
    sds = valuesfile.split("_")[0]
    print "Processing %s..." % sds

    valuesfile = open("%s/%s" % (valuespath, valuesfile), "r")

    values = []
    rows = []
    columns = valuesfile.readline().strip("\n").split("\t")

    record = valuesfile.readline()
    while record:
        record = record.strip("\n").split("\t")

        row = record[0]
        if float(row) > 179.9:
            row = "%0.6f" % (-360.0 + float(row))
        rows.append(row)
    
        rowlist = [float(value) for value in record[1:]]
        values.append(rowlist)

        record = valuesfile.readline()

    valuesfile.close()

    # -------------------------------------------------------------------------
    for hid in hidlist:
        index = 0
        numerator = 0.0
        denominator = 0.0

        while index < neighbors:
            address = weights[hid][index][1].split(" ")

            rowindex = rows.index(address[0])
            columnindex = columns.index(address[1])
            
            value = values[rowindex][columnindex]
            distance = weights[hid][index][0]

            numerator += value / distance
            denominator += 1.0 / distance
            
            index += 1
        
        sdsvalues[hid][sds] = numerator / denominator
    
# -----------------------------------------------------------------------------
outputpath = "%s/Projects/SDM Rewilding/%s_%s/ISEA3H%02i_%s_%s_%s_%s_IDW1N%i.txt"
outputfile = open(outputpath % (z, dataset, sdsgroup, resolution,
                                dataset, year1, year2, sdsgroup, neighbors), "w")

sdslist = sdsvalues[1].keys()
sdslist.sort()

outputfile.write("HID")
for sds in sdslist:
    outputfile.write("\t%s_IDW1N%i" % (sds, neighbors))

for hid in hidlist:
    outputfile.write("\n%i" % hid)

    for sds in sdslist:
        outputfile.write("\t%0.6f" % sdsvalues[hid][sds])

outputfile.close()