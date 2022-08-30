library(raster)

basinraster <- raster("/Users/mechenic/Ecosphere/Datasets/SedimentaryBasins_V01/SedimentaryBasins_V01_Terrestrial.tif")
basinraster <- reclassify(basinraster, cbind(NA, 0))

tileframe <- read.table("/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/Working/Tile Definitions.txt",
                        header = TRUE,
                        sep = "\t",
                        stringsAsFactors = FALSE)

gridfolder <- "/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/"

for (index in 1:nrow(tileframe)) {
  tile <- tileframe[index, "Tile"]

  arearaster <- raster(paste(gridfolder, substr(tile, 5, 8), "/Area_", tile, "_Geodetic_0008D_WGS84.tif", sep = ""))

  hidraster <- raster(paste(gridfolder, substr(tile, 5, 8), "/HID_ISEA3H09_", tile, "_Geodetic_0008D_WGS84.tif", sep = ""))
  hidframe <- data.frame(HID = unique(hidraster))

  tilebasinraster <- crop(basinraster, hidraster)
  classvector <- unique(tilebasinraster)
  for (subindex in classvector) {
    classraster <- (tilebasinraster == subindex) * arearaster
    classmatrix <- zonal(classraster, hidraster, fun = 'sum')

    hidframe[, sprintf("%i", subindex)] <- sprintf("%0.6f", classmatrix[match(hidframe$HID, classmatrix[, 1]), 2])
  }

  hidframe$HID <- sprintf("%i", hidframe$HID)
  write.table(hidframe,
              file = paste("/Users/mechenic/Ecosphere/ISEA3H09/SedimentaryBasins_V01/Working/ISEA3H09_SedimentaryBasins_V01_Terrestrial_X/ISEA3H09_SedimentaryBasins_V01_", tile, "_Terrestrial_RasterArea.txt", sep = ""),
              quote = FALSE,
              sep = "\t",
              row.names = FALSE)
}