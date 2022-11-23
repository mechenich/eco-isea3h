import pickle

from geographiclib.geodesic import Geodesic
geod = Geodesic.WGS84

# -----------------------------------------------------------------------------
# resolution = 6
# spacing = 261.2463863485 * 1000
# resolution = 7
# spacing = 150.8306714832 * 1000
# resolution = 8
# spacing = 87.0821287828 * 1000
resolution = 9
spacing = 50.2768904944 * 1000

directory = "/home/ad/home/m/mechenic/Projects/Ecosphere Analysis/" + \
            "Spatial Statistics"

# -----------------------------------------------------------------------------
centroidpath = "%s/ISEA3H%02i - Geodetic Coordinates - Centroids.txt" % (
               directory, resolution)
centroidfile = open(centroidpath, "r")

hids = {}
for record in centroidfile.readlines()[1:]:
    record = record.strip("\n").split("\t")
    
    hids[int(record[0])] = [float(record[1]), float(record[2])]

centroidfile.close()
print "%i HID(s) read.\n" % len(hids)

# -----------------------------------------------------------------------------
referencepath = "%s/HID Reference - ISEA3H%02i > ISEA3H%02i.pkl" % (directory,
                resolution, resolution - 1)
referencefile = open(referencepath, "rb")

reference = pickle.load(referencefile)

referencefile.close()

# -----------------------------------------------------------------------------
neighborspath = "%s/Nearest Neighbors - ISEA3H%02i - ERA40.pkl" % (directory,
                resolution - 1)
neighborsfile = open(neighborspath, "rb")

neighborlookup = pickle.load(neighborsfile)

neighborsfile.close()

# -----------------------------------------------------------------------------
addresses = {"0.0 90.0": [0.0, 90.0],
             "0.0 -90.0": [0.0, -90.0]}

for y in range(-875, 900, 25):
    for x in range(-1800, 1800, 25):
        xfloat = x / 10.0
        yfloat = y / 10.0
        addresses["%0.1f %0.1f" % (xfloat, yfloat)] = [xfloat, yfloat]

# -----------------------------------------------------------------------------
outpath = "%s/Nearest Neighbors - ISEA3H%02i - ERA40.pkl" % (directory,
          resolution)
outfile = open(outpath, "wb")

hidlist = hids.keys()
hidlist.sort()

neighbors = {}
for hid in hidlist:
    
    if len(reference[hid]) == 1:
        neighbors[hid] = neighborlookup[reference[hid][0]]

    elif len(reference[hid]) == 3:
        addresslist = []
        for rhid in reference[hid]:
            for address in neighborlookup[rhid]:
                if address[1] not in addresslist:
                    addresslist.append(address[1])

        distances = []
        for address in addresslist:
            distance = geod.Inverse(hids[hid][1],
                                    hids[hid][0],
                                    addresses[address][1],
                                    addresses[address][0])["s12"]
            distances.append([distance, address])

        distances.sort()
        count = 20
        while distances[count - 1][0] < spacing:
            count += 1
        neighbors[hid] = list(distances[:count])

        print "HID %i - %i" % (hid, count)
    
    else:
        print "Error - HID %i - %i" % (hid, len(reference[hid]))
        break

pickle.dump(neighbors, outfile, -1)
outfile.close()