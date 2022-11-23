library(dggridR)
library(raster)

dggs <- data.frame(resolution = 5:12,
                   cellcount = c(2432, 7292, 21872, 65612, 196832, 590492, 1771472, 5314412))

sdss <- data.frame(code   = c(           "BIO",            "PREC",            "SRAD",            "TAVG",            "TMAX",            "TMIN",            "VAPR",            "WIND"),
                   fname  = c("wc2.0_bio_30s_", "wc2.0_30s_prec_", "wc2.0_30s_srad_", "wc2.0_30s_tavg_", "wc2.0_30s_tmax_", "wc2.0_30s_tmin_", "wc2.0_30s_vapr_", "wc2.0_30s_wind_"),
                   vcount = c(              19,                12,                12,                12,                12,                12,                12,                12),
                   nullv  = c(            -100,                -1,                -1,              -100,              -100,              -100,                -1,                -1),
                   ftext  = c(         "%0.6f",              "%i",              "%i",           "%0.1f",           "%0.1f",           "%0.1f",           "%0.2f",           "%0.1f"),
                   stringsAsFactors = FALSE)

for (index in 5:5) {
  hids <- 1:dggs[index, ]$cellcount

  dgg <- dgconstruct(projection = "ISEA",
                     aperture = 3,
                     topology = "HEXAGON",
                     res = dggs[index, ]$resolution)
  
  xylist <- dgSEQNUM_to_GEO(dgg, hids)

  centroids <- SpatialPointsDataFrame(coords = cbind(xylist$lon_deg, xylist$lat_deg),
                                      data = data.frame(HID = hids),
                                      proj4string = CRS("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"),
                                      match.ID = FALSE)

  for (subindex in 5:8) {
    sds <- sdss[subindex, ]
    sdsfields <- paste(sds$code, sprintf("%02i", 1:sds$vcount), "_Centroid", sep = "")

    for (subsubindex in 1:sds$vcount) {
      rastername <- paste("/Users/mechenic/Projects/Shared Datasets/WorldClim/",
                          sds$code, "_30S/",
                          sds$fname, sprintf("%02i", subsubindex), ".tif", sep = "")

      valueraster <- raster(rastername)
      values <- extract(valueraster, centroids, method = "simple")
      values[is.na(values)] <- sds$nullv

      centroids@data[, sdsfields[subsubindex]] <- sprintf(sds$ftext, values)
    }
    
    tablename <- paste("/Users/mechenic/Ecosphere/",
                       "ISEA3H", sprintf("%02i", dggs[index, ]$resolution), "/",
                       "WorldClim30AS_V02/",
                       "ISEA3H", sprintf("%02i", dggs[index, ]$resolution), "_",
                       "WorldClim30AS_V02_", sds$code, "_Centroid.txt", sep = "")

    write.table(centroids@data[, append(c("HID"), sdsfields)],
                file = tablename, quote = FALSE, sep = "\t", row.names = FALSE)
  }
}
    