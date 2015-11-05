#!/bin/bash
#NB_RTR=2
#BUFFER_SIZE=4
SUITE="dce-iperf-mptcp-mixed"
#SCHEDULER=""
echo $@
echo $0
echo $1
SUFFIX="$1"
shift 1
PARAMS="$@"
# clean results folder
resFolder="results"
#rm -Rf "$resFolder"

mkdir -p "$resFolder"


#if [ -z "$NS_RUN" ]; then

	#print "\$NS_RUN not set"
	#exit 1
#fi


#export NS_GLOBAL_VALUE="ChecksumEnabled=1;RngRun=$NS_RUN"
#SUFFIX="${SUFFIX}-run${NS_RUN}"
#echo "NS_GLOBAL_VALUE=$NS_GLOBAL_VALUE"
echo "SUFFIX=$SUFFIX"
echo "PARAMS=$PARAMS"
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

python3 ~/ns3testing/test_ns3.py example $SUITE --clean --load-log="ns_log.txt" --out="xp_$SUFFIX.log" $PARAMS 

if [ $? -ne 0 ]; then
	echo "Program failed with exit value '$?'"
	exit 1
fi

# backup the results
filename=$(get_iperf_results_dir)
copy_iperf_result "$filename" "$resFolder/$SUFFIX.csv"
mergecap $DCE_FOLDER/iperf-mptcp-0-*.pcap -w "$resFolder/iperf-client-$SUFFIX.pcap"

#exit 0

# need to find under which PID ran
#ag -l iperf files-0 -G cmdline

#python3 ~/ns3testing/test_ns3.py example $SUITE --clean --load-log=ns_log.txt --out=xp.log --nRtrs=$NB_RTR --ChecksumEnabled=1 --clientStack=ns --serverStack=ns

#filename=$(get_iperf_results_dir)
#copy_iperf_result "$filename" "$resFolder/ns3.csv"
#mergecap "$DCE_FOLDER/iperf-mptcp-0-*.pcap" -w "iperf-client-ns3.pcap"


## Finally we plot a graph comparing linux to ns3
#cmd="Rscript iperf.r $resFolder/linux.csv $resFolder/ns3.csv"
#echo $cmd
