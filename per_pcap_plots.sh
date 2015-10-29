#!/bin/sh

singlePathFilter="results/*.pcap"
multiPathFilter="results/*2rtrs*.pcap"
#mkdir -p "results_img"
for file in $multiPathFilter
do
	echo "$file"
	panda.py $file --regen plot TimeVsDsn 0 "$file.png"
done

# requires imagemagick
montage "results/*.png" -geometry +1+1 all.png
