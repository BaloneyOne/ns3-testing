#!/bin/sh
mkdir -p files-1/tmp/ files-0/tmp/
DCE_FOLDER="$HOME/dce" $HOME/ns3testing/test_ns3.py example dce-iperf 
