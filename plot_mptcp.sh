#!/bin/sh

singlePathFilter="results/*1nbRtrs*.pcap"
multiPathFilter="results/*2nbRtrs*.pcap"
#mkdir -p "results_img"
for file in $multiPathFilter
do
	echo "$file"
	mptcpanalyzer "$file" --regen plot TimeVsDsn 0 "${file}_dsn.png"
	mptcpanalyzer "$file" --regen plot LatencyHistogram 0 "${file}_latency.png"
	# requires imagemagick
	montage ${file}*.png -geometry +1+1 "${file}_all.png"
done

