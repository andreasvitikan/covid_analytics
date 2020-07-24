data = read.csv("data\\latestData.csv", header = TRUE)
# some sanity checks
sum(data$numberInfected)
sum(data$numberCured)
sum(data$numberDeceased)
