#!/bin/bash
NB_RTR=1
SUITE="dce-iperf-mptcp-mixed"

# clean results folder
resFolder="res${NB_RTR}"
rm -Rf "$resFolder"

mkdir "$resFolder"


# expects source/destination
copy_iperf_result ()
{

	echo "timestamp,source_address,source_port,destination_address,destination_port,interval,transferred_bytes,bits_per_second" > "$2"
	cat "$1" >> "$2" 
}

get_iperf_results_dir()
{
	dir="$(dirname $(ag -l iperf "$DCE_FOLDER/files-0" -G cmdline))"
	echo "$dir/stdout"
}

python3 ~/ns3testing/test_ns3.py example $SUITE --clean --load-log=ns_log.txt --out=xp.log --nRtrs=$NB_RTR --ChecksumEnabled=1 --clientStack=linux --serverStack=linux

# backup the results
filename=$(get_iperf_results_dir)
copy_iperf_result "$filename" "$resFolder/linux.csv"

#exit 0

# need to find under which PID ran
#ag -l iperf files-0 -G cmdline

python3 ~/ns3testing/test_ns3.py example $SUITE --clean --load-log=ns_log.txt --out=xp.log --nRtrs=$NB_RTR --ChecksumEnabled=1 --clientStack=ns --serverStack=ns

filename=$(get_iperf_results_dir)
copy_iperf_result "$filename" "$resFolder/ns3.csv"


# Finally we plot a graph comparing linux to ns3
cmd="Rscript iperf.r $resFolder/linux.csv $resFolder/ns3.csv"
echo $cmd
