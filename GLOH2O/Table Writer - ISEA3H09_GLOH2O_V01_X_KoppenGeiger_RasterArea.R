library(raster)

koppenraster <- raster("/Users/mechenic/Projects/Shared Datasets/GLOH2O/Beck_KG_V1_present_0p0083.tif")

tileframe <- read.table("/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/Working/Tile Definitions.txt",
                        header = TRUE,
                        sep = "\t",
                        stringsAsFactors = FALSE)

gridfolder <- "/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/"

for (index in 9:nrow(tileframe)) {
  tile <- tileframe[index, "Tile"]

  arearaster <- raster(paste(gridfolder, substr(tile, 5, 8), "/Area_", tile, "_Geodetic_0008D_WGS84.tif", sep = ""))

  hidraster <- raster(paste(gridfolder, substr(tile, 5, 8), "/HID_ISEA3H09_", tile, "_Geodetic_0008D_WGS84.tif", sep = ""))
  hidframe <- data.frame(HID = unique(hidraster))

  tilekoppenraster <- crop(koppenraster, hidraster)
  classvector <- unique(tilekoppenraster)
  for (subindex in classvector) {
    classraster <- (tilekoppenraster == subindex) * arearaster
    classmatrix <- zonal(classraster, hidraster, fun = 'sum')

    hidframe[, sprintf("%i", subindex)] <- sprintf("%0.6f", classmatrix[match(hidframe$HID, classmatrix[, 1]), 2])
  }

  hidframe$HID <- sprintf("%i", hidframe$HID)
  write.table(hidframe,
              file = paste("/Users/mechenic/Ecosphere/ISEA3H09/GLOH2O_V01/Working/ISEA3H09_GLOH2O_V01_KoppenGeiger_X/ISEA3H09_GLOH2O_V01_", tile, "_KoppenGeiger_RasterArea.txt", sep = ""),
              quote = FALSE,
              sep = "\t",
              row.names = FALSE)
}