resolution = 9
dataset = "ECMWF"
version = "ERA40"
sdsgroup = "ETCCDI"

year1 = "Y1958"
year2 = "Y2001"

neighbors = 10

# -----------------------------------------------------------------------------
import os
import pickle

z = "/home/ad/home/m/mechenic/"

weightspath = "%s/Projects/Ecosphere Analysis/Spatial Statistics/" + \
              "Nearest Neighbors - ISEA3H%02i - %s.pkl"
weightsfile = open(weightspath % (z, resolution, version), "rb")

weights = pickle.load(weightsfile)

weightsfile.close()

# -----------------------------------------------------------------------------
hidlist = weights.keys()
hidlist.sort()

sdsvalues = {}
for hid in hidlist:
    sdsvalues[hid] = {}

# -----------------------------------------------------------------------------
valuespath = "%s/Projects/Shared Datasets/%s/%s/Means" % (z, dataset, version)

for valuesfile in os.listdir(valuespath):
    sds = valuesfile.split("_")[0][:-1 * len(sdsgroup)].upper()
    print "Processing %s..." % sds

    valuesfile = open("%s/%s" % (valuespath, valuesfile), "r")

    values = []
    rows = []
    columns = valuesfile.readline().strip("\n").split("\t")[1:]

    record = valuesfile.readline()
    while record:
        record = record.strip("\n").split("\t")

        row = record[0]
        if float(row) > 179.9:
            row = "%0.1f" % (-360.0 + float(row))
        rows.append(row)
    
        rowlist = []
        for value in record[1:]:
            if value != "NaN":
                rowlist.append(float(value))
            else:
                rowlist.append(value)
        values.append(rowlist)

        record = valuesfile.readline()

    valuesfile.close()

    # -------------------------------------------------------------------------
    for hid in hidlist:
        count = 0
        index = 0
        numerator = 0.0
        denominator = 0.0

        while count < neighbors:
            address = weights[hid][index][1].split(" ")

            rowindex = rows.index(address[0])
            columnindex = columns.index(address[1])
            
            value = values[rowindex][columnindex]
            distance = weights[hid][index][0]

            if value != "NaN":
                numerator += value / distance
                denominator += 1.0 / distance
                count += 1
            
            index += 1
        
        sdsvalues[hid][sds] = numerator / denominator
    
# -----------------------------------------------------------------------------
outputpath = "%s/Ecosphere/ISEA3H%02i/%s_%s/" + \
             "ISEA3H%02i_%s_%s_%s_%s_%s_IDW1N%i.txt"
outputfile = open(outputpath % (z, resolution, dataset, version, resolution,
                  dataset, version, year1, year2, sdsgroup, neighbors), "w")

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