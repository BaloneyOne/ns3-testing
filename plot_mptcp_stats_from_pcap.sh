#!/bin/sh
# folder=""
set -x

prefix="$HOME/ns3off2/multi-${node}"

echo "nb= $#"
if [ $# -lt 1 ]; then
	echo "Use: $0 <pcap>"
	exit 1
	# echo "Accepting parameter from cli"
fi

prefix="$1"

# for node in  $(seq 0 1)
# do
# 	echo $node
# mergecap mptcp-multi-${node}-*.pcap -w $prefix.pcap
PARAMS=""
	# then use mptcpanalyzer to generate some statistics
	mptcpanalyzer -l$prefix plot misc 0 toserver dsn --title "Data Sequence Number" --out $prefix.dsn.png --style red_o \
		--skip 1 --skip 3  
	# mptcpanalyzer -l$prefix plot misc 0 toserver dss_dsn --title "DSS DSN" --out $prefix.dss_dsn.png
	mptcpanalyzer -l$prefix plot misc 0 toclient dack --title "MPTCP level ACKs" --out $prefix.dack.png
# done
