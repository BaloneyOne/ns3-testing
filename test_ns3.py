import sys
import os
import argparse
import subprocess
import importlib

available_suites = [
    "tcp",
    "tcp-header",
    "callback",
    "traced-callback",
    #"ns3-tcp-state",
    "mptcp-tcp",
    "mptcp-multi",
    "tcp-option-mptcp",
    "mptcp-crypto",
    "clock",
    "node-scheduling",
    "mptcp-mapping",
    "time"
]


# type=argparse.FileType('w'),
# parser = argparse.ArgumentParser(description="Helper to debug mptcp")

# parser.add_argument("suite", choices=available_suites, help="Launch gdb")
# args, unknown_args = parser.parse_known_args()

ns3folder="/home/teto/ns3off"
suite = sys.argv[1]
suite = suite.replace('-', '_')

print("Suite=%s"% suite)
# mod = importlib.import_module('tests.mptcp_tcp')
from tests.mptcp_tcp import Test
# mod = __import__('tests.mptcp-tcp')
# test = DefaultTest()
# todo it later
if os.path.exists("tests/%s" % suite):
    # import tests.(args.suite).
    test = DefaultTest()
else:
    test = Test()

# assuming there are more
# test.run(ns3folder, sys.argv[1:])
print(sys.argv)
test.run(ns3folder, sys.argv[1:])
# timeout = None

# if args.debug:
    # cmd = "./waf --run test-runner --command-template=\"gdb -ex 'run --suite={suite} {verbose} {tofile}' --args %s \" "
# else:
    # timeout = 200
    # cmd = "./waf --run \"test-runner --suite={suite} --fullness={fullness} {verbose} \" {tofile}"


# tofile = " > %s 2>&1" % args.out if args.out else ""
# # tofile = " > xp.txt 2>&1"

# cmd = cmd.format(
    # suite=args.suite,
    # verbose=args.verbose,
    # # out=
    # tofile=tofile,
    # fullness="QUICK",
# )

# os.environ['NS_LOG'] = NS_LOG


# provoked prompts in sublimetext, annoying
# os.system("rm source/*")
# os.system("rm server/*")

# remove output folders and recreate them 

# os.system(cmd)


# , timeout=timeout
# try:
    # ret = subprocess.call(cmd, shell=True, timeout=timeout if timeout else None)
# except subprocess.TimeoutExpired:
    # print("Timeout expired. try setting a longer timeout")
# finally:
    # # will be done whatever the results
    # #os.system("./mergepcaps.sh")
    # # os.system("mergecap -w source.pcap test-1-1.pcap test-1-2.pcap")
    # pass

# # print("Exported:\n%s" % NS_LOG)
# # print("Executed Command:\n%s" % cmd)

# if ret:
    # print("ERROR: command returned error code %d" % (ret))
    # # os.system("truncate --size=100000 %s" % (args.out,))
    # exit(1)

# if args.graph:
    # # 
    # os.system("mptcpexporter pcap2sql source.pcapng")
    # os.system("mptcpgraph ")

# for mptcp tests only
#for i in ['server', 'source']:
    #print("Content of folder '%s':" % (i,))
    #os.system("ls -l %s" % (i,))

# print("Content of folder 'server':")
# os.system("./draw_plots.sh")
