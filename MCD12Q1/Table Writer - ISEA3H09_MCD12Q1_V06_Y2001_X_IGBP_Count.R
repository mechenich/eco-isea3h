library(raster)

# ---------------------------------------------------------------------------------------
foldertext <- "/Users/mechenic/Ecosphere/"

datasettext <- "MCD12Q1"
subdatasettext <- "IGBP"
versiontext <- "V06"
yeartext <- "Y2001"

hextext <- "ISEA3H09"
gridtext <- "Sinusoidal_500M_WGS84"

# ---------------------------------------------------------------------------------------
ecofiles <- list.files(path = paste(foldertext, "Datasets/", datasettext, "_",
                                    versiontext, "_", yeartext, sep = ""),
                       pattern = ".*tif$",
                       full.names = TRUE)

tileindex <- nchar(foldertext) + 9 + 2 * (nchar(datasettext) + nchar(versiontext) +
             nchar(yeartext) + 2) + 4

tileframe <- data.frame(ECOFILE = ecofiles,
                        H = as.integer(substr(ecofiles, tileindex, tileindex + 1)),
                        V = as.integer(substr(ecofiles, tileindex + 3, tileindex + 4)),
                        stringsAsFactors = FALSE)

tileframe$HIDFILE <- paste(foldertext, "Grids/", gridtext, "/V", sprintf("%02i",
                     tileframe$V), "/HID_", hextext, "_H", sprintf("%02i", tileframe$H),
                     "V", sprintf("%02i", tileframe$V), "_", gridtext, ".tif", sep = "")

# ---------------------------------------------------------------------------------------
for (index in 1:nrow(tileframe)) {
  tile <- tileframe[index, ]

  ecoraster <- raster(tile$ECOFILE)
  hidraster <- raster(tile$HIDFILE)
  
  freqframe <- crosstab(hidraster, ecoraster,
                        long = TRUE)

  freqframe$HID <- sprintf("%i", freqframe[, 1])
  freqframe$Class <- sprintf("%i", freqframe[, 2])
  freqframe$Count <- sprintf("%i", freqframe[, 3])

  write.table(freqframe[, c("HID", "Class", "Count")],
              file = paste(foldertext, hextext, "/", datasettext, "_", versiontext,
                           "/Working/", hextext, "_", datasettext, "_", versiontext,
                           "_", yeartext, "_", subdatasettext, "_X/", hextext, "_",
                           datasettext, "_", versiontext, "_", yeartext, "_H",
                           sprintf("%02i", tile$H), "V", sprintf("%02i", tile$V), "_",
                           subdatasettext, "_Count.txt", sep = ""),
              quote = FALSE,
              sep = "\t",
              row.names = FALSE)
}