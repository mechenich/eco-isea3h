# -------------------------------------------------------------------------------------------------
# Script to sample PHYLACINE v1.2.1 species range raster datasets at ISEA3H cell centroids.

# The 'rgdal' and 'raster' packages are required. We recommend saving script in a 'Scripts' folder,
# at the root of the Eco-ISEA3H directory structure.

# Command-line arguments:
# (1) ISEA3H resolution at which to sample.
# (2) PHYLACINE scenario, either 'P' for present or 'PN' for present natural (not case sensitive).
# (3) Taxonomic rank of the group of species to sample, either 'O' for order or 'F' for family (not
#     case sensitive).
# (4) Name of the order or family.
# (5) Full path to the PHYLACINE database; files in this folder must be exactly as extracted from
#     the PHYLACINE v1.2.1 ZIP file.

# Command-line example:
# Rscript PHYLACINE_V010201_Centroid.R 9 PN O Proboscidea /Projects/Datasets/PHYLACINE

# -------------------------------------------------------------------------------------------------
library(rgdal)
library(raster)

arguments <- commandArgs(trailingOnly = TRUE)
resolution <- as.numeric(arguments[1])
scenario <- toupper(arguments[2])
rank <- toupper(arguments[3])
taxon <- arguments[4]
phypath <- arguments[5]

# -------------------------------------------------------------------------------------------------
coordinates <- read.table(paste("../Spatial/Text/Centroids_ISEA3H", sprintf("%02i", resolution),
                                "_Geodetic_V_WGS84.txt", sep = ""),
                          header = TRUE, sep = "\t")

xymatrix <- project(as.matrix(coordinates[, c("X", "Y")]),
                    proj = paste("+proj=cea +lon_0=0 +lat_ts=30 +x_0=0 +y_0=0 +datum=WGS84 ",
                                 "+units=m +no_defs +ellps=WGS84 +towgs84=0,0,0", sep = ""))

# -------------------------------------------------------------------------------------------------
taxa <- read.table(paste(phypath, "/Taxonomy/Synonymy_table_valid_species_only.csv", sep = ""),
                   header = TRUE, sep = ',', stringsAsFactors = FALSE)

taxafield <- c("O" = "Order.1.2", "F" = "Family.1.2")[rank]

species <- taxa[taxa[, taxafield] == taxon, "Binomial.1.2"]
  
textframe <- data.frame(HID = sprintf('%i', coordinates$HID))

for (s in sort(species)) {
  rangeraster <- raster(paste(phypath, "/Ranges/",
                              c("P" = "Current", "PN" = "Present_natural")[scenario],
                              "/", s, '.tif', sep = ''))

  rangepoints <- extract(rangeraster, xymatrix)
  rangepoints[is.na(rangepoints)] <- 0

  textframe[, paste(s, "_Centroid", sep = "")] <- sprintf("%i", rangepoints)

  print(paste(taxon, "-", gsub("_", " ", s), sep = " "))
}

write.table(textframe,
            paste("../ISEA3H", sprintf("%02i", resolution), "/PHYLACINE_V010201/ISEA3H",
                  sprintf("%02i", resolution), "_PHYLACINE_V010201_",
                  c("P" = "Present", "PN" = "PresentNatural")[scenario], "_", taxon,
                  "_Centroid.txt", sep = ""),
            quote = FALSE, sep = "\t", row.names = FALSE)

