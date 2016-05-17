#!/bin/sh
# folder=""
set -x

prefix="$HOME/ns3off2/multi-${node}"

echo "nb= $#"
if [ $# -ge 1 ]; then
	# echo "Accepting parameter from cli"
	prefix="$1"
fi

# for node in  $(seq 0 1)
# do
# 	echo $node
# mergecap mptcp-multi-${node}-*.pcap -w $prefix.pcap

	# then use mptcpanalyzer to generate some statistics
	mptcpanalyzer -l$prefix plot misc 0 dsn --title "DSN" --out $prefix.dsn.png
	# mptcpanalyzer -l$prefix plot misc 0 dss_dsn --title "DSS DSN" --out $prefix.dss_dsn.png
	# mptcpanalyzer -l$prefix plot misc 0 dack --title "DSS ACK" --out $prefix.dack.png
# done
