library(raster)

datasettext <- "GPW30AS"
versiontext <- "V0411"
sdstext <- "Density"

dggs <- data.frame(resolution = 5:12,
                   cellcount = c(2432, 7292, 21872, 65612, 196832, 590492, 1771472, 5314412))

tiles <- read.table(file = "/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/Working/Tile Definitions.txt",
                    header = TRUE,
                    sep = "\t",
                    stringsAsFactors = FALSE)

for (index in 5:5) {
  dgg <- dggs[index, ]

  hids <- data.frame(HID = 1:dgg$cellcount)

  for (year in c(2020)) {
    valueraster <- raster(paste("/Users/mechenic/Projects/Shared Datasets/Gridded Population of the World/",
                                "gpw_v4_population_density_rev11_", sprintf("%i", year), "_30_sec.tif", sep = ""))

    areavector <- rep(0.0, dgg$cellcount)
    productvector <- rep(0.0, dgg$cellcount)

    for (subindex in 1:nrow(tiles)) {
      tile <- tiles[subindex, ]

      hidraster <- raster(paste("/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/", substr(tile$Tile, 5, 7),
                                "/HID_ISEA3H", sprintf("%02i", dgg$resolution), "_", tile$Tile, "_Geodetic_0008D_WGS84.tif", sep = ""))

      subvalueraster <- crop(valueraster, hidraster)

      arearaster <- raster(paste("/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/", substr(tile$Tile, 5, 7),
                                 "/Area_", tile$Tile, "_Geodetic_0008D_WGS84.tif", sep = ""))
      arearaster <- mask(arearaster, subvalueraster)

      productraster <- subvalueraster * arearaster

      areamatrix <- zonal(arearaster, hidraster, fun = "sum")
      productmatrix <- zonal(productraster, hidraster, fun = "sum")

      areavector[areamatrix[, 1]] <- areavector[areamatrix[, 1]] + areamatrix[, 2]
      productvector[productmatrix[, 1]] <- productvector[productmatrix[, 1]] + productmatrix[, 2]

      print(paste("ISEA3H", sprintf("%02i", dgg$resolution), " - Y", sprintf("%i", year), " - ", sdstext, " - ", tile$Tile, " - ", Sys.time(), sep = ""))
    }

    meanvector <- productvector / areavector
    meanvector[is.na(meanvector)] <- -1.0

    hids[, paste(sdstext, "_Mean", sep = "")] <- sprintf("%0.6f", meanvector)

    tablename <- paste("/Users/mechenic/Ecosphere/ISEA3H", sprintf("%02i", dgg$resolution), "/", datasettext, "_", versiontext,
                       "/ISEA3H", sprintf("%02i", dgg$resolution), "_", datasettext, "_", versiontext, "_Y", sprintf("%i", year), "_", sdstext, "_Mean.txt", sep = "")

    write.table(hids, file = tablename, quote = FALSE, sep = "\t", row.names = FALSE)
  }
}

# x <- rep(0, 10)
# x[c(8, 4, 6)] <- c(1, 2, 3)
      