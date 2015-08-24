#!/bin/bash
#http://unix.stackexchange.com/questions/20035/how-to-add-newlines-into-variables-in-bash-script
read -r -d '' ns_log<<EOF
*=error|warn|prefix_node|prefix_func
:MpTcpTestSuite
:MpTcpSchedulerRoundRobin
:Config
:TcpSocket
:MpTcpSubflow:MpTcpSocketBase
:TcpSocketBase
:MpTcpCrypto
:TcpTestSuite
:TcpRxBuffer
:TcpTxBuffer
:TcpHeader=*
:TcpL4Protocol
:TcpTraceHelper
:Socket
:MpTcpMapping
:MpTcpMappingTestSuite
EOF
#:TraceHelper:PointToPointHelper
#:ClockTest
#:ClockPerfect
#:Clock
#:PointToPointNetDevice
#:PointToPointChannel
#:DropTailQueue
#:Node
#NS_LOG += ":AttributeValue"
#NS_LOG += ":MpTcpSchedulerRoundRobin"
# NS_LOG += ":SimpleNetDevice"
# NS_LOG=":TcpOptionMpTcp=*"
# NS_LOG=":MpTcpOptionsTestSuite=*"
# NS_LOG += ":Config"
# NS_LOG += ":TypeId" # to look for AddTraceSource
#NS_LOG += ":MpTcpMapping"
# NS_LOG += ":PcapFile"
#prefix_func:Socket=*"
#NS_LOG += ":Ipv4EndPoint"
# NS_LOG += ":Ipv4EndPointDemux"
#NS_LOG="*"

ns_log=${ns_log//[[:space:]]/}
printf "%s" "$ns_log"
export NS_LOG="$ns_log"
python3 ./test_ns3.py $@
