#!/bin/sh

# Call
# For scheduler, you can only choose 'default' or 'roundrobin'
# for congestion control, only lia is available
# 
export NS_GLOBAL_VALUE="ChecksumEnabled=1"
#./unit_test.sh "linux_2rtrs_f30b30_f10b30_lia" --nRtrs=2 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=10 --backwardDelay1=30 --scheduler="default" --window="40K"


# LINUX 1 router 

./unit_test.sh "linux_1rtrs_f30b30_f30b30_w40K_lia" --nRtrs=1 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="40K"
./unit_test.sh "linux_1rtrs_f30b30_f30b30_w60K_lia" --nRtrs=1 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="60K"
./unit_test.sh "linux_1rtrs_f30b30_f30b30_w80K_lia" --nRtrs=1 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="80K"
./unit_test.sh "linux_1rtrs_f30b30_f30b30_w140K_lia" --nRtrs=1 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="140K"
#./unit_test.sh "linux_1rtrs_f30b30_f30b30_w180K_lia" --nRtrs=1 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="180K"
#./unit_test.sh "linux_1rtrs_f30b30_f30b30_w200K_lia" --nRtrs=1 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="200K"
#./unit_test.sh "linux_1rtrs_f30b30_f30b30_w400K_lia" --nRtrs=1 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="400K"
#./unit_test.sh "linux_1rtrs_f30b30_f30b30_w800K_lia" --nRtrs=1 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="800K"



# NS 2 routers
./unit_test.sh "ns_1rtrs_f30b30_f30b30_w40K_lia" --nRtrs=1 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="40K"
./unit_test.sh "ns_1rtrs_f30b30_f30b30_w60K_lia" --nRtrs=1 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="60K"
./unit_test.sh "ns_1rtrs_f30b30_f30b30_w80K_lia" --nRtrs=1 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="80K"
./unit_test.sh "ns_1rtrs_f30b30_f30b30_w140K_lia" --nRtrs=1 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="140K"


# NS 2 routers
#./unit_test.sh "ns_2rtrs_f30b30_f30b30_w80K_lia" --nRtrs=2 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30  --ChecksumEnabled=1 --window="80K"



# Linux 2 routers
#./unit_test.sh "linux_2rtrs_f30b30_f30b30_w80K_lia" --nRtrs=2 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="80K"
#./unit_test.sh "linux_2rtrs_f30b30_f50b30_lia" --nRtrs=2 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=50 --backwardDelay1=30 
#./unit_test.sh "linux_2rtrs_f30b30_f70b30_lia" --nRtrs=2 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=70 --backwardDelay1=30 
#./unit_test.sh "linux_2rtrs_f30b30_f1900b30_lia" --nRtrs=2 --clientStack=linux --serverStack=linux --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=90 --backwardDelay1=30 
#./unit_test.sh "ns_2rtrs_f30b30_f1900b30_lia" --nRtrs=2 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=90 --backwardDelay1=30 
#./unit_test.sh "ns_2rtrs_f30b30_f30b30_lia" --nRtrs=2 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 
