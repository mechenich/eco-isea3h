library(raster)

# -------------------------------------------------------------------------------------------------
directorytext <- '/home/ad/home/m/mechenic/Ecosphere/'

datasettext <- 'MOD44B_V06'
yeartext <- 'Y2018'
sdsindexvector <- c(0, 1, 2)

hexagontext <- 'ISEA3H09'
rastertext <- 'Sinusoidal_250M_WGS84'

# -------------------------------------------------------------------------------------------------
filevector <- list.files(paste(directorytext, 'Datasets/', datasettext, '_', yeartext, sep = ''))
tilevector <- unique(sapply(filevector, function(filetext) strsplit(filetext, '_')[[1]][4]))

for(tiletext in tilevector) {
  hidraster <- raster(paste(directorytext, 'Grids/', rastertext, '/', hexagontext,
                            '/HID_', hexagontext, '_', tiletext, '_', rastertext, '.tif', sep = ''))

  for (sdsindex in sdsindexvector) {
    tabletext <- paste(directorytext, hexagontext, '/', datasettext, '/Working/',
                       hexagontext, '_', datasettext, '_', yeartext, '_X_Mean/',
                       hexagontext, '_', datasettext, '_', yeartext, '_', tiletext, '_SDS', sprintf('%02i', sdsindex), '_Count.txt', sep = '')

    if (!file.exists(tabletext)) {
      sdsraster <- raster(paste(directorytext, 'Datasets/', datasettext, '_', yeartext, '/',
                                datasettext, '_', yeartext, '_', tiletext, '_SDS', sprintf('%02i', sdsindex), '.tif', sep = ''))

      freqframe <- crosstab(hidraster, sdsraster, long = TRUE)
      freqframe$HID <- sprintf('%i', freqframe[, 1])
      freqframe$Percent <- sprintf('%i', freqframe[, 2])
      freqframe$Count <- sprintf('%i', freqframe[, 3])

      write.table(freqframe[, c('HID', 'Percent', 'Count')],
                  file = tabletext,
                  quote = FALSE, sep = '\t', row.names = FALSE)
    }
  }
}