import pickle

from geographiclib.geodesic import Geodesic
geod = Geodesic.WGS84

# -----------------------------------------------------------------------------
resolution = 5
spacing = 452.4920144495 * 1000

directory = "/home/ad/home/m/mechenic/Projects/Ecosphere Analysis/" + \
            "Spatial Statistics"
hidpath = "%s/ISEA3H%02i - Geodetic Coordinates - Centroids.txt" % (directory,
          resolution)

hidfile = open(hidpath, "r")

hids = {}
for record in hidfile.readlines()[1:]:
    record = record.strip("\n").split("\t")
    
    hids[int(record[0])] = [float(record[1]), float(record[2])]

hidfile.close()
print "%i HID(s) read.\n" % len(hids)

# -----------------------------------------------------------------------------
addresses = [[0.0, 90.0], [0.0, -90.0]]
for y in range(-875, 900, 25):
    for x in range(-1800, 1800, 25):
        addresses.append([(x / 10.0), (y / 10.0)])

# -----------------------------------------------------------------------------
outpath = "%s/Nearest Neighbors - ISEA3H%02i - ERA40.pkl" % (directory,
          resolution)
outfile = open(outpath, "wb")

hidlist = hids.keys()
hidlist.sort()

neighbors = {}
for hid in hidlist:

    distances = []
    for address in addresses:
        distance = geod.Inverse(hids[hid][1], hids[hid][0],
                                address[1], address[0])["s12"]
        distances.append([distance, "%0.1f %0.1f" % (address[0], address[1])])
    
    distances.sort()
    count = 20
    while distances[count - 1][0] < spacing:
        count += 1
    neighbors[hid] = list(distances[:count])

    print "HID %i - %i" % (hid, count)

pickle.dump(neighbors, outfile, -1)
outfile.close()
