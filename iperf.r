#!/usr/bin/Rscript
# draw boxplots
# TODO générer le graphe pour les 2 fichiers
# ggplot2 a l'air cool sinon http://stackoverflow.com/questions/14604439/plot-multiple-boxplot-in-one-graph
args <- commandArgs(trailingOnly = TRUE)

#linuxFile <- args[1]
#nsFile <- args[2]

print(linuxFile)
print("toto")
print(nsFile)

png(filename = "outfile.png", width = 800, height = 500)

linuxDat <- read.csv(linuxFile, header = TRUE,row.names=NULL)
nsDat <- read.csv(nsFile, header = TRUE,row.names=NULL)


# list of entries with each entry describing the dataset (os/delay)
# os/buffsize
# os
iperf_results <-  list(
	#list(file="res1/linux", title="Linux/2/4M"),
	#list(file="", buffsize=, nRtrs=2),

)

# 
for (i in 1:length(iperf_results)) {

}

# 
boxplot(data.frame(linuxDat['bits_per_second'], nsDat['bits_per_second']),
		#1*linuxDat['bits_per_second'],
		col=(c("gold","darkgreen")),
		main="Tooth Growth",
		names=c("Linux", "Ns3"),
		
		xlab="Download speed (linux vs ns3)") 

# necessary to flush the png 
dev.off()
