# could be handy sometime setwd(choose.dir())

setwd(choose.dir())
data = read.csv("data\\latestData.csv", header = TRUE)
# some sanity checks
sprintf("The total number of infected is: %i", sum(data$numberInfected))
sprintf("The total number of cured is: %i", sum(data$numberCured))
sprintf("The total number of deceased is: %i", sum(data$numberDeceased))

# length(data_frame) gets the number of variables or ncol(data_frame) - number of columns
# nrow(data_frame) gets the number of rows (observations)

# columns 15:56 are the countyInfectionsNumbers
max_county <- which.max(data[nrow(data), 15:56])
sprintf("The county with the most infections is: %s with %i infections", names(data)[max_county + 14], data[nrow(data), max_county + 14])
