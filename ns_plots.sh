#!/bin/sh
# Use mptcpanalyzer and imagemagick to generate a global overview of a connection
# Typically you would run
# NS3_FOLDER="$HOME/"$FOLDER"" $HOME/ns3testing/test_ns3.py test mptcp-multi --verbose --load-log=$HOME/ns3testing/ns_mptcp.txt > temp 2>&$NODE
set -x
# list of attributes highestSeq,rxAvailable,rxTotal,state,cwnd,unackSeq,rxNext,ssThresh,txNext,rWnd,Time
FOLDER="$HOME/ns3off2"

for NODE in $(seq 0 1)
do
	echo $NODE
	# Server => Node 0 
	# Client => node 1
	name="client"
	if [ $NODE -eq 0 ]; then
		name="server"
	fi
	# mptcpanalyzer plot ns3 --meta ~/"$FOLDER" $NODE cwnd  --out meta_cwnd_$NODE.png
	mptcpanalyzer plot ns3 --title "Mixed congestion window" --subflows --meta "$FOLDER" $NODE cwnd  --out cwnd_$NODE.png 
	mptcpanalyzer plot ns3 --subflows --meta "$FOLDER" $NODE rWnd  --out meta_rwnd_$NODE.png --title "Meta RWND"
	mptcpanalyzer plot ns3 --meta "$FOLDER" $NODE txNext unackSeq  --out tx_meta_$NODE.png --title "Meta Tx state"
	mptcpanalyzer plot ns3 --subflows "$FOLDER" $NODE txNext unackSeq  --out tx_subflows_$NODE.png --title "Subflow Tx state"
	mptcpanalyzer plot ns3 --meta "$FOLDER" $NODE rWnd unackSeq  --out meta_rwnd_$NODE.png --title="Meta Rwnd + SND.UNA" 
	mptcpanalyzer plot ns3 --subflows "$FOLDER" $NODE rxNext  --out rx_subflows_$NODE.png  --title="RxNext of subflows"
	mptcpanalyzer plot ns3 --meta "$FOLDER" $NODE rxNext  --out rx_meta_$NODE.png --title="RxNext for meta"

	montage \
		tx_meta_$NODE.png tx_subflows_$NODE.png \
		rx_meta_$NODE.png rx_subflows_$NODE.png \
		cwnd_$NODE.png meta_rwnd_$NODE.png \
		-tile 2x3 -geometry +1+1 global_$NODE.png
done

montage global_0.png global_1.png -tile 2x1 -geometry +1+1 all.png 

# gcc sxiv all.png

# montage tx_meta.png tx_subflows.png meta_rx.png subflows_rx.png meta_cwnd.png subflows_cwnd.png meta_rwnd.png -tile 2x4 -geometry +$NODE+$NODE %s

# todo generate montage and plot it ?!
# move outside !
#   glob all pngs and count them to generate -tile
	# cmd = "montage tx_meta.png tx_subflows.png meta_rx.png subflows_rx.png meta_cwnd.png subflows_cwnd.png meta_rwnd.png -tile 2x4 -geometry +$NODE+$NODE %s" % (args.out)
	# subprocess.call( shlex.split(cmd),)

# montage for both nodes
