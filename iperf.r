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
	# list(file="results/linux_2rtrs_f30b30_f10b30_lia.csv", title="Linux/2/4M"),
	# list(file="results/linux_2rtrs_f30b30_f30b30_lia.csv", title="Linux/1/60ms/60ms/4M"),
# 	list(file="results/linux_2rtrs_f30b30_f50b30_lia.csv", title="Linux/1/4M"),
# 	list(file="results/linux_2rtrs_f30b30_f70b30_lia.csv", title="Linux/1/4M"),
# 	list(file="results/linux_2rtrs_f30b30_f90b30_lia.csv", title="Linux/1/4M"),

# list(file="results/ns_2rtrs_f30b30_f30b30_w80K_lia.csv", title="ns3/2/80K"),
# list(file="results/linux_2rtrs_f30b30_f30b30_w80K_lia.csv", title="linux/2/80K")
# list(file="results/linux_1rtrs_f30b30_f30b30_w200K_lia.csv", title="Linux/1/200K"),  
# list(file="results/linux_1rtrs_f30b30_f30b30_w400K_lia.csv", title="Linux/1/400K"),
# list(file="results/linux_1rtrs_f30b30_f30b30_w800K_lia.csv", title="Linux/1/800K")
	#list(file="", buffsize=, nRtrs=2),

  list(file="results/linux_2rtrs_f30b30_f30b30_w40K_lia.csv", title="Linux/2/40KB"),
  list(file="results/linux_2rtrs_f30b30_f30b30_w60K_lia.csv", title="Linux/2/60KB"),
  list(file="results/linux_2rtrs_f30b30_f30b30_w80K_lia.csv", title="Linux/2/80KB"),
  list(file="results/linux_2rtrs_f30b30_f30b30_w140K_lia.csv", title="Linux/2/140KB"),
  
  list(file="results/ns_2rtrs_f30b30_f30b30_w40K_lia.csv", title="ns/2/40KB"),
  list(file="results/ns_2rtrs_f30b30_f30b30_w60K_lia.csv", title="ns/2/60KB"),
  list(file="results/ns_2rtrs_f30b30_f30b30_w80K_lia.csv", title="ns/2/80KB"),
  list(file="results/ns_2rtrs_f30b30_f30b30_w140K_lia.csv", title="ns/2/140KB")
)

# results for 1 path to check that buffer is taking into account and correct regarding BDP
# iperf_results <- list(
#   list(file="results/linux_1rtrs_f30b30_f30b30_w40K_lia.csv", title="Linux/1/40KB"),
#   list(file="results/linux_1rtrs_f30b30_f30b30_w80K_lia.csv", title="Linux/1/80KB"),
#   list(file="results/linux_1rtrs_f30b30_f30b30_w140K_lia.csv", title="Linux/1/140KB"),
# 
#   list(file="results/ns_1rtrs_f30b30_f30b30_w40K_lia.csv", title="ns/1/40KB"),
#   list(file="results/ns_1rtrs_f30b30_f30b30_w80K_lia.csv", title="ns/1/80KB"),
#   list(file="results/ns_1rtrs_f30b30_f30b30_w140K_lia.csv", title="ns/1/140KB")
# )


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
# l <-append(l,data)
print(str(data))

# http://stackoverflow.com/questions/17840323/multiple-boxplots-on-one-graph
# /1000 to put in kbps
# to get names apply http://r.789695.n4.nabble.com/Selecting-elements-from-all-items-in-a-list-td4387045.html
# dataframe or list
# print(dat[0,1]['bits_per_second'])

# without that xlabels are out of the picture
# http://stackoverflow.com/questions/24511818/r-vertical-x-labels-out-of-plot
par(mar=c(8, 4, 2, 2) + 0.1)
boxplot(
  data.frame(data),
  # list(data),
  # dat[["bits_per_second"]],
  
  #1*linuxDat['bits_per_second'],
  # main="Iperf",
  names=as.vector(titles),
  #xlab="Download speed (linux vs ns3)",
  ylab="Throughput (bps)",
  las=3 # To put vertical labels
) 

# necessary to flush the png 
dev.off()
