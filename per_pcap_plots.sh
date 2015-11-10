#!/bin/sh

singlePathFilter="results/*1nbRtrs*.pcap"
multiPathFilter="results/*2nbRtrs*.pcap"
#mkdir -p "results_img"
for file in $multiPathFilter
do
	echo "$file"
	panda.py $file --regen plot TimeVsDsn 0 "$file.png"
done

# requires imagemagick
montage "results/*.png" -geometry +1+1 all.png
