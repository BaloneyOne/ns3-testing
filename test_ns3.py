#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import importlib
import logging
# from tests import Test
# import ns_tests.test as toto
from ns_tests import *

log = logging.getLogger("ns_tests.test")
# logging.getLogger()
log.setLevel(logging.DEBUG)
# log.addHandler(logging.StreamHandler())
log.addHandler(logging.FileHandler("test.log", mode="w"))

# this serves just as a helper for me to remember what I am working on
# can be removed anytime
available_suites = [
    "tcp",
    "tcp-header",
    "callback",
    "traced-callback",
    "ipv4-forwarding",
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


# "/home/teto/ns3off"
# "/home/teto/dce"

# You need to define these environement variables else the program will crash
ns3folder = os.environ["NS3_FOLDER"]
dce_folder = os.environ["DCE_FOLDER"]


def list_specialized_tests():
    f = {}
    for g in DefaultTest.__subclasses__(): 
        # print("subclass=", g)
        for test in g.cover_tests():
            # f.extend() to extend a list
            f.update({test: g})
    return f


def choose_correct_class(suite):
    """
    """

    available = list_specialized_tests()
    print(available)
    if suite in available:
        return available[suite]

    if suite.startswith('dce'):
        return DceDefaultTest 

    return DefaultTest


def main():
    parser = argparse.ArgumentParser(description="Helper to debug ns3/dce programs")

    # parser.add_argument("suite", choices=available_suites, help="Launch gdb")

    # parser.add_argument("project", type=str, choices=["dce", "ns3"], help="To which project does the test/example belong")
    # project and type could be set via namedtuples in cover_tests 
    # instead of setting it manually here
    parser.add_argument("type", type=str, choices=["test", "example"], help="What kind of program do we have to launch")
    parser.add_argument("program", type=str, help="Name of the suite or exemple to run")
    parser.add_argument("--debug", '-d', action="store_true", help="Launch gdb")
    parser.add_argument("--out", "-o", default="", action="store", help="redirect ns3 results output to a file")
    parser.add_argument("--load-log", "-l", action="store", help="Load log from file")

    args, unknown_args = parser.parse_known_args()

    # maybe not needed anymore
    suite = args.program
    # suite = suite.replace('-', '_')

    """
    Now we get to choose what kind of test to launch
    if example/test starts with 'dce' then it's a DCE test.
    if we can find a file with a name matching the program to launch, then we load it
    """

    test_class = choose_correct_class(suite)

    working_directory = dce_folder if test_class.is_dce() else ns3folder 

    print("test_class", test_class)
    print("working_directory", working_directory)
    test = test_class(working_directory, args.type)
    # assuming there are more
    # test.run(ns3folder, sys.argv[1:])
    # print(sys.argv)

    if args.load_log:
        ns_log = DefaultTest.load_log(args.load_log)
        log.info("Setting NS_LOG to:\n%s" % ns_log)
        os.environ['NS_LOG'] = ns_log

    result = test.run(args.debug, args.out, [args.program] + unknown_args)

    print("log written to [%s]" % "test.log")

    if result:
        print("Program failed with result=%d" % result)
        sys.exit(result)



if __name__ == '__main__':
    main()
