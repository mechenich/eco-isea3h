library(raster)

arguments <- commandArgs(trailingOnly = TRUE)
resolutionindex <- as.integer(arguments[1])
datasetindex <- as.integer(arguments[2])

datasettext <- "WorldClim30AS"
versiontext <- "V02"
sdstext <- "BIO"

dggs <- data.frame(resolution = 5:12,
                   cellcount = c(2432, 7292, 21872, 65612, 196832, 590492, 1771472, 5314412))

tiles <- read.table(file = "/Users/mechenic/Ecosphere/Grids/Geodetic_0008D_WGS84/Working/Tile Definitions.txt",
                    header = TRUE,
                    sep = "\t",
                    stringsAsFactors = FALSE)

for (index in resolutionindex:resolutionindex) {
  dgg <- dggs[index, ]

  hids <- data.frame(HID = 1:dgg$cellcount)

  for (subindex in datasetindex:datasetindex) {
    valueraster <- raster(paste("/Users/mechenic/Projects/Shared Datasets/WorldClim/BIO_30S/wc2.0_bio_30s_",
                                sprintf("%02i", subindex), ".tif", sep = ""))

    areavector <- rep(0.0, dgg$cellcount)
    productvector <- rep(0.0, dgg$cellcount)

    for (subsubindex in 1:nrow(tiles)) {
      tile <- tiles[subsubindex, ]

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

      print(paste("ISEA3H", sprintf("%02i", dgg$resolution), " - ", sdstext, sprintf("%02i", subindex), " - ", tile$Tile, " - ", Sys.time(), sep = ""))
    }

    meanvector <- productvector / areavector
    meanvector[is.na(meanvector)] <- -100.0

    hids[, paste(sdstext, sprintf("%02i", subindex), "_Mean", sep = "")] <- sprintf("%0.6f", meanvector)

    tablename <- paste("/Users/mechenic/Ecosphere/ISEA3H", sprintf("%02i", dgg$resolution), "/", datasettext, "_", versiontext,
                       "/ISEA3H", sprintf("%02i", dgg$resolution), "_", datasettext, "_", versiontext, "_", sdstext, sprintf("%02i", subindex), "_Mean.txt", sep = "")

    write.table(hids, file = tablename, quote = FALSE, sep = "\t", row.names = FALSE)
  }
}

# x <- rep(0, 10)
# x[c(8, 4, 6)] <- c(1, 2, 3)
      