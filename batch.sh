#!/bin/sh

# Call
# For scheduler, you can only choose 'default' or 'roundrobin'
# for congestion control, only lia is available
# 

./unit_test.sh "linux_2rtrs_f30b30_f10b30_lia" --nRtrs=2 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=10 --backwardDelay1=30 --scheduler="default" --window="4M"
#./unit_test.sh "linux_2rtrs_f30b30_f30b30_lia" --nRtrs=2 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 
#./unit_test.sh "ns_2rtrs_f30b30_f30b30_lia" --nRtrs=2 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 
