import os

# ------------------------------------------------------------------------------
hids = {}

totalsfile = open("/Users/mechenic/Ecosphere/ISEA3H09/Spatial/" +
                  "ISEA3H09_Sinusoidal_500M_WGS84_Count.txt", "r")

for record in totalsfile.readlines()[1:]:
    record = record.strip("\n").split("\t")

    hids[int(record[0])] = {"T": int(record[1])}

totalsfile.close()

# ------------------------------------------------------------------------------
countfolder = "/Users/mechenic/Ecosphere/ISEA3H09/MCD12Q1_V06/Working/" + \
              "ISEA3H09_MCD12Q1_V06_Y2001_IGBP_X"

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

        if hid != 0 and value >= 1 and value <= 16:
            if value not in hids[hid]:
                hids[hid][value] = 0

            hids[hid][value] += count

    countfile.close()
    
# ------------------------------------------------------------------------------
fractionfile = open("/Users/mechenic/Ecosphere/ISEA3H09/MCD12Q1_V06/" +
                    "ISEA3H09_MCD12Q1_V06_Y2001_IGBP_Fractions.txt", "w")

fractionfile.write("HID")
for value in range(1, 17):
    fractionfile.write("\tIGBP_%02i_Fraction" % value)

modefile = open("/Users/mechenic/Ecosphere/ISEA3H09/MCD12Q1_V06/" +
                "ISEA3H09_MCD12Q1_V06_Y2001_IGBP_Mode.txt", "w")

modefile.write("HID\tIGBP_Mode")

hidlist = hids.keys()
hidlist.sort()

for hid in hidlist:
    fractions = []
    total = 0

    for value in range(1, 17):
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
