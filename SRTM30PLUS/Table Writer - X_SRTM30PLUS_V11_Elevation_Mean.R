library(raster)

datasettext <- "SRTM30PLUS"
versiontext <- "V11"
sdstext <- "Elevation"

dggs <- data.frame(resolution = 5:12,
                   cellcount = c(2432, 7292, 21872, 65612, 196832, 590492, 1771472, 5314412))

tiles <- read.table(file = "/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/Working/Tile Definitions.txt",
                    header = TRUE,
                    sep = "\t",
                    stringsAsFactors = FALSE)

for (index in 6:6) {
  dgg <- dggs[index, ]

  hids <- data.frame(HID = sprintf("%i", 1:dgg$cellcount),
                     stringsAsFactors = FALSE)

  areavector <- rep(0.0, dgg$cellcount)
  productvector <- rep(0.0, dgg$cellcount)

  for (subindex in 1:nrow(tiles)) {
    tile <- tiles[subindex, ]

    hidraster <- raster(paste("/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/", substr(tile$Tile, 5, 7),
                              "/HID_ISEA3H", sprintf("%02i", dgg$resolution), "_", tile$Tile, "_Geodetic_0008D_WGS84.tif", sep = ""))

    valueraster <- raster(paste("/Users/mechenic/Projects/Shared Datasets/SRTM30-PLUS/", tile$Tile,
                                ".Bathymetry.srtm.ers", sep = ""))
    valueraster <- shift(valueraster, x = xres(valueraster), y = yres(valueraster) * -1.0)

    arearaster <- raster(paste("/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/", substr(tile$Tile, 5, 7),
                               "/Area_", tile$Tile, "_Geodetic_0008D_WGS84.tif", sep = ""))

    productraster <- valueraster * arearaster

    areamatrix <- zonal(arearaster, hidraster, fun = "sum")
    productmatrix <- zonal(productraster, hidraster, fun = "sum")

    areavector[areamatrix[, 1]] <- areavector[areamatrix[, 1]] + areamatrix[, 2]
    productvector[productmatrix[, 1]] <- productvector[productmatrix[, 1]] + productmatrix[, 2]

    print(paste("ISEA3H", sprintf("%02i", dgg$resolution), " - ", sdstext, " - ", tile$Tile, " - ", Sys.time(), sep = ""))
  }

  meanvector <- productvector / areavector

  hids[, paste(sdstext, "_Mean", sep = "")] <- sprintf("%0.6f", meanvector)

  tablename <- paste("/Users/mechenic/Ecosphere/ISEA3H", sprintf("%02i", dgg$resolution), "/", datasettext, "_", versiontext,
                       "/ISEA3H", sprintf("%02i", dgg$resolution), "_", datasettext, "_", versiontext, "_", sdstext, "_Mean.txt", sep = "")

  write.table(hids, file = tablename, quote = FALSE, sep = "\t", row.names = FALSE)
}

# x <- rep(0, 10)
# x[c(8, 4, 6)] <- c(1, 2, 3)
      