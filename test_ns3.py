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
dce_folder="/home/teto/dce"


parser = argparse.ArgumentParser(description="Helper to debug ns3/dce programs")

# parser.add_argument("suite", choices=available_suites, help="Launch gdb")
parser.add_argument("project", type=str, choices=["dce", "ns3"], help="To which project does the test/example belong")
# here it should be able to find on its own the type normally
parser.add_argument("type", type=str, choices=["test", "example"], help="What kind of program do we have to launch")
parser.add_argument("program", type=str, help="Name of the suite or exemple to run")

args, unknown_args = parser.parse_known_args()

working_directory = ns3folder if args.project == "ns3" else dce_folder

suite = args.program
suite = suite.replace('-', '_')

# mod = importlib.import_module('tests.mptcp_tcp')
from tests.mptcp_tcp import Test
# mod = __import__('tests.mptcp-tcp')
# test = DefaultTest()
# todo it later
# todo get root folder
if os.path.exists("tests/%s" % suite):
    # import tests.(args.suite).
    test = DefaultTest(working_directory, args.type)
else:
    test = Test(working_directory, args.type)

# assuming there are more
# test.run(ns3folder, sys.argv[1:])
# print(sys.argv)
test.run(working_directory, [args.program] + unknown_args)
