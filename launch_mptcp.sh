#!/bin/bash
#http://unix.stackexchange.com/questions/20035/how-to-add-newlines-into-variables-in-bash-script
read -r -d '' ns_log<<EOF
*=error|warn|prefix_node|prefix_func
:PointToPointNetDevice
:ClockTest
:ClockPerfect
:Clock
:Node
:PointToPointChannel
:DropTailQueue
:MpTcpMultiSuite
:MpTcpSchedulerRoundRobin
:Config
:TcpSocket
:MpTcpSubflow:MpTcpSocketBase
:MpTcpCrypto
:TcpTestSuite
:TcpRxBuffer
:TcpTxBuffer
:TcpHeader=*
:TcpL4Protocol
:TraceHelper:PointToPointHelper
EOF
#NS_LOG += ":AttributeValue"
#NS_LOG += ":MpTcpSchedulerRoundRobin"
# NS_LOG += ":SimpleNetDevice"
# NS_LOG=":TcpOptionMpTcp=*"
# NS_LOG=":MpTcpOptionsTestSuite=*"
# NS_LOG += ":Config"
# NS_LOG += ":TypeId" # to look for AddTraceSource
#NS_LOG += ":MpTcpMapping"
# NS_LOG += ":PcapFile"
# NS_LOG=":MpTcpTestSuite=*|prefix_func:Socket=*"
#NS_LOG += ":Ipv4EndPoint"
# NS_LOG += ":Ipv4EndPointDemux"
#NS_LOG="*"

ns_log=${ns_log//[[:space:]]/}
printf "%s" "$ns_log"
export NS_LOG="$ns_log"
python3 ./test_ns3.py $@
