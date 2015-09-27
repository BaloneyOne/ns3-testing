#!/usr/bin/Rscript
# draw boxplots
# TODO générer le graphe pour les 2 fichiers
# ggplot2 a l'air cool sinon http://stackoverflow.com/questions/14604439/plot-multiple-boxplot-in-one-graph
args <- commandArgs(trailingOnly = TRUE)

#linuxFile <- args[1]
#nsFile <- args[2]

# print(linuxFile)
# print("toto")
# print(nsFile)

resultsFolder= "/home/teto/ns3testing"
png_filename= paste(resultsFolder, "out.png", sep="/")
png(filename = png_filename, width = 800, height = 500)

# linuxDat <- read.csv(linuxFile, header = TRUE,row.names=NULL)
# nsDat <- read.csv(nsFile, header = TRUE,row.names=NULL)


# list of entries with each entry describing the dataset (os/delay)
# os/buffsize
# os
iperf_results <- list(
	list(file="results/linux_2rtrs_f30b30_f10b30_lia.csv", title="Linux/2/4M"),
	list(file="results/linux_2rtrs_f30b30_f30b30_lia.csv", title="Linux/1/4M"),
	list(file="results/linux_2rtrs_f30b30_f30b30_lia.csv", title="Linux/1/4M")
	
	#list(file="", buffsize=, nRtrs=2),

)

titles <- lapply(iperf_results, `[[`, "title")
print(str(titles))

# list of datasets
dat = list()
for (i in 1:length(iperf_results)) {
  filename = iperf_results[[i]][["file"]]
  filename = paste(resultsFolder, filename, sep="/")
  print(filename)
  # append to dat
  dat[[length(dat)+1]] <- read.csv( filename, header = TRUE,row.names=NULL)

}
data <- lapply(dat, `[`, "bits_per_second")
print(str(data))

# http://stackoverflow.com/questions/17840323/multiple-boxplots-on-one-graph
# /1000 to put in kbps
# to get names apply http://r.789695.n4.nabble.com/Selecting-elements-from-all-items-in-a-list-td4387045.html
# dataframe or list
# print(dat[0,1]['bits_per_second'])

boxplot(data.frame(data),
        #1*linuxDat['bits_per_second'],
        col=(c("gold","darkgreen")),
        main="Tooth Growth",
        names=as.vector(titles),
        xlab="Download speed (linux vs ns3)") 

# necessary to flush the png 
dev.off()
