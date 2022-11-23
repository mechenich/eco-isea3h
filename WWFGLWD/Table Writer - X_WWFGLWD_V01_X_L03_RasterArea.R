library(raster)

workpath <- "/Users/mechenic/Ecosphere/"
gridpath <- paste(workpath, "Grids/Geodetic_0008D_WGS84/", sep = "")

arguments <- commandArgs(trailingOnly = TRUE)
resolution <- sprintf("%02i", as.integer(arguments[1]))

valueraster <- raster(paste(workpath, "Datasets/WWFGLWD_V01/WWFGLWD_V01_L03.tif", sep = ""))

tileframe <- read.table(paste(gridpath, "Working/Tile Definitions.txt", sep = ""),
                        header = TRUE,
                        sep = "\t",
                        stringsAsFactors = FALSE)

for (index in 1:nrow(tileframe)) {
  tile <- tileframe[index, "Tile"]

  arearaster <- raster(paste(gridpath, substr(tile, 5, 8), "/Area_", tile,
                       "_Geodetic_0008D_WGS84.tif", sep = ""))
  hidraster <- raster(paste(gridpath, substr(tile, 5, 8), "/HID_ISEA3H", resolution,
                      "_", tile, "_Geodetic_0008D_WGS84.tif", sep = ""))
  tileraster <- crop(valueraster, hidraster)

  hidframe <- data.frame(HID = unique(hidraster))

  classvector <- unique(tileraster)
  for (subindex in classvector) {
    text <- sprintf("%i", subindex)

    classraster <- (tileraster == subindex) * arearaster

    classmatrix <- zonal(classraster, hidraster, fun = 'sum')
    colnames(classmatrix) <- c("HID", text)

    hidframe <- merge(hidframe, classmatrix, by = "HID")
    hidframe[, text] <- sprintf("%0.6f", hidframe[, text])
  }

  hidframe$HID <- sprintf("%i", hidframe$HID)
  write.table(hidframe,
              file = paste(workpath, "ISEA3H", resolution, "/WWFGLWD_V01/Working/ISEA3H",
                           resolution, "_WWFGLWD_V01_L03_X/ISEA3H", resolution, "_WWFGLWD_V01_",
                           tile, "_L03_RasterArea.txt", sep = ""),
              quote = FALSE,
              sep = "\t",
              row.names = FALSE)
}