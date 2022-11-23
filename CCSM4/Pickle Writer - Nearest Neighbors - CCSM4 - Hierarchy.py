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
neighborspath = "%s/Nearest Neighbors - ISEA3H%02i - CCSM4.pkl" % (directory,
                resolution - 1)
neighborsfile = open(neighborspath, "rb")

neighborlookup = pickle.load(neighborsfile)

neighborsfile.close()

# -----------------------------------------------------------------------------
ylist = [-89.057592, -88.115183, -87.172775, -86.230366, -85.287958,
         -84.345550, -83.403141, -82.460733, -81.518325, -80.575916,
         -79.633508, -78.691099, -77.748691, -76.806283, -75.863874,
         -74.921466, -73.979058, -73.036649, -72.094241, -71.151832,
         -70.209424, -69.267016, -68.324607, -67.382199, -66.439791,
         -65.497382, -64.554974, -63.612565, -62.670157, -61.727749,
         -60.785340, -59.842932, -58.900524, -57.958115, -57.015707,
         -56.073298, -55.130890, -54.188482, -53.246073, -52.303665,
         -51.361257, -50.418848, -49.476440, -48.534031, -47.591623,
         -46.649215, -45.706806, -44.764398, -43.821990, -42.879581,
         -41.937173, -40.994764, -40.052356, -39.109948, -38.167539,
         -37.225131, -36.282723, -35.340314, -34.397906, -33.455497,
         -32.513089, -31.570681, -30.628272, -29.685864, -28.743455,
         -27.801047, -26.858639, -25.916230, -24.973822, -24.031414,
         -23.089005, -22.146597, -21.204188, -20.261780, -19.319372,
         -18.376963, -17.434555, -16.492147, -15.549738, -14.607330,
         -13.664921, -12.722513, -11.780105, -10.837696, -9.895288,
         -8.952880, -8.010471, -7.068063, -6.125654, -5.183246, -4.240838,
         -3.298429, -2.356021, -1.413613, -0.471204, 0.471204, 1.413613,
         2.356021, 3.298429, 4.240838, 5.183246, 6.125654, 7.068063,
         8.010471, 8.952880, 9.895288, 10.837696, 11.780105, 12.722513,
         13.664921, 14.607330, 15.549738, 16.492147, 17.434555, 18.376963,
         19.319372, 20.261780, 21.204188, 22.146597, 23.089005, 24.031414,
         24.973822, 25.916230, 26.858639, 27.801047, 28.743455, 29.685864,
         30.628272, 31.570681, 32.513089, 33.455497, 34.397906, 35.340314,
         36.282723, 37.225131, 38.167539, 39.109948, 40.052356, 40.994764,
         41.937173, 42.879581, 43.821990, 44.764398, 45.706806, 46.649215,
         47.591623, 48.534031, 49.476440, 50.418848, 51.361257, 52.303665,
         53.246073, 54.188482, 55.130890, 56.073298, 57.015707, 57.958115,
         58.900524, 59.842932, 60.785340, 61.727749, 62.670157, 63.612565,
         64.554974, 65.497382, 66.439791, 67.382199, 68.324607, 69.267016,
         70.209424, 71.151832, 72.094241, 73.036649, 73.979058, 74.921466,
         75.863874, 76.806283, 77.748691, 78.691099, 79.633508, 80.575916,
         81.518325, 82.460733, 83.403141, 84.345550, 85.287958, 86.230366,
         87.172775, 88.115183, 89.057592]

addresses = {"0.000000 90.000000": [0.0, 90.0],
             "0.000000 -90.000000": [0.0, -90.0]}

for y in ylist:
    for x in range(-18000, 18000, 125):
        xfloat = x / 100.0
        addresses["%0.6f %0.6f" % (xfloat, y)] = [xfloat, y]

# -----------------------------------------------------------------------------
outpath = "%s/Nearest Neighbors - ISEA3H%02i - CCSM4.pkl" % (directory,
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