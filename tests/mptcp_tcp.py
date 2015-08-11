#!/usr/bin/python
import os
import subprocess
import argparse


parser = argparse.ArgumentParser()


class DefaultTest:

    parser = None

    def __init__(self):
        parser = argparse.ArgumentParser(description="Helper to debug mptcp")

        # parser.add_argument("suite", choices=available_suites, help="Launch gdb")
        parser.add_argument("suite", type=str, help="Launch gdb")
        parser.add_argument("--debug", '-d', action="store_true", help="Launch gdb")
        parser.add_argument("--out", "-o", default="", nargs='?', help="redirect ns3 results output to a file")
        parser.add_argument("--verbose", "-v", action="store_const", default="", const="--verbose", help="to enable more output")
        self.parser = parser
        self.init()

    def init(self):
        pass

    def setup(self, args):
        """
        Pre hooks, executed before the running command
        """
        pass

    def postprocess(self, *args, **kwargs):
        pass

    def run(self, ns3folder, cli_args):
        """
        cli_args are then passed to 
        """
        timeout = None
        
        args = self.parser.parse_args(cli_args)
        args, unknown = self.parser.parse_known_args(cli_args)

        # os.path.exists("%s/waf" % (ns3folder))
        if args.debug:
            cmd = "./waf --run test-runner --command-template=\"gdb -ex 'run --suite={suite} {verbose} {tofile}' --args %s \" "
        else:
            timeout = 200
            cmd = "./waf --run \"test-runner --suite={suite} --fullness={fullness} {verbose} \" {tofile}"

        # TODO replace verbose with "unknown"
        tofile = " > %s 2>&1" % args.out if args.out else ""
        cmd = cmd.format(
                # ns3folder=ns3folder,
            suite=args.suite,
            verbose=args.verbose,
            # out=
            tofile=tofile,
            fullness="QUICK",
        )
        print("Changing working directory to %s" % (ns3folder))
        print("Executed Command:\n%s" % cmd)
        ret = 0
        try:
            # cmd="pwd > xp.txt 2>&1"
            # cmd="./waf"
            # proc = subprocess.Popen(cmd, shell=True, cwd=ns3folder)
            ret = subprocess.call(cmd, shell=True, cwd="/home/teto/ns3off", timeout=timeout if timeout else None)

            # proc.wait(timeout=timeout if timeout else None)
        except subprocess.TimeoutExpired:
            print("Timeout expired. try setting a longer timeout")
        except Exception as e:
            print (e)
        finally:
            # will be done whatever the results
            #os.system("./mergepcaps.sh")
            # os.system("mergecap -w source.pcap test-1-1.pcap test-1-2.pcap")

            pass

        if ret:
            print("ERROR: command returned error code %d" % ret)
            # os.system("truncate --size=100000 %s" % (args.out,))
            exit(1)

        self.postprocess(args)

        print("Executed Command:\n%s" % cmd)

class Test(DefaultTest):
    
    def init(self):
        self.parser.add_argument("--graph", "-g", action="store_true", help="Convert pcap to sqlite db and then plot")


    def setup(self, graph, **kwargs):
        if graph:
            # TODO check it's ok
            os.system("./clean.sh")

    # def run(self):


    def postprocess(self, graph, **kwargs):
        pass

# Test test

# __all__ = [
        # 'test'
        # ]
