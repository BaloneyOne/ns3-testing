#!/usr/bin/python
import subprocess
import argparse
import logging
import os
import glob
import shutil

# parser = argparse.ArgumentParser()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
#log.addHandler(logging.StreamHandler())
log.addHandler(logging.FileHandler("test.log", mode="w"))

class DefaultTest:
    """
    Allow to run preprocess and postprocess scripts automatically
    """

    parser = None

    def __init__(self, working_directory, 
            type
            ):

        self.wd = working_directory
        self.type = type

        parser = argparse.ArgumentParser(description="Helper to debug mptcp")

        # parser.add_argument("program", choices=available_programs, help="Launch gdb")
        parser.add_argument("program", type=str, help="Launch gdb")
        parser.add_argument("--debug", '-d', action="store_true", help="Launch gdb")
        parser.add_argument("--out", "-o", default="", nargs='?', help="redirect ns3 results output to a file")
        # parser.add_argument("--load-log", "-l", default="", nargs='1', help="Load log from file")

        parser.add_argument("--clean", "-c", action="store_const", const=True,  help="Remove files that could be misinterpreted")
        # parser.add_argument("--verbose", "-v", action="store_const", default="", const="--verbose", help="to enable more output")
        self.parser = parser
        log.info("created instance of %r" % self) 
        self.init()

    def init(self):
        pass

    @staticmethod
    def is_dce():
        return True

    def get_type(self):
        """ Is it a "test" or an "example" """
        return self.get_type


    def get_root_folder(self):
        """
        Returns ns3testing folder
        """
        root=os.path.dirname(os.path.abspath(__file__))
        root=os.path.join(root, "../")
        return root

    def setup(self, *args, **kw):
        """
        Pre hooks, executed before the running command
        """
        log.debug('setup called with parameters %r' % kw)
        if kw.get('clean'):
            self.clean()

    def postprocess(self, *args, **kwargs):
        """
        Operations run after the test (post-hooks)
        """
        pass

    def clean_pcaps(self):
        log.info('removing pcap files')
        for pcap in glob.glob(os.path.join(self.get_waf_directory(), "*.pcap" )):
            log.debug("Removing pcap %s" % pcap)
            os.remove(pcap)


    def clean(self):
        log.info('Cleaning')
        self.clean_pcaps()

    @staticmethod
    def _convert_args_into_dict(args):
        return vars(args)


    def run(self, cli_args):
        """
        cli_args are then passed to the argument parser, should be a list
        """
        timeout = None

        # args = self.parser.parse_args(cli_args)
        args, unknown_args = self.parser.parse_known_args(cli_args)

        args_dict = self._convert_args_into_dict(args)
        print(args_dict)
        log.debug("Just before running setup")
        self.setup(**args_dict)
        extra_params = "--suite=%s" % args.program if self.type == "test" else ""
        extra_params += ' '.join(list(unknown_args))
# TODO the verbose could be removed
# --fullness={fullness} is not supported in some cases
        if args.debug:
            cmd = "./waf --run {program} --command-template=\"gdb -ex 'run {extra_params} {verbose} {tofile}' --args %s \" "
        else:
            timeout = 200
            cmd = "./waf --run \"{program} {extra_params} {verbose} \" {tofile}"

        # TODO replace verbose with "unknown"
        tofile = " > %s 2>&1" % args.out if args.out else ""
        cmd = cmd.format(
                extra_params=extra_params,
                # 
                program="test-runner" if self.type == "test" else args.program,
                verbose="", # args.verbose,
                # out=
                tofile=tofile,
                fullness="QUICK",
                )
        log.debug("Changing working directory to %s" % (self.get_waf_directory()))
        log.info(cmd)
        print("Executed Command:\n%s" % cmd)
        ret = 0
        try:
            # cmd="pwd > xp.txt 2>&1"
            # cmd="./waf"
            # proc = subprocess.Popen(cmd, shell=True, cwd=wd)
            ret = subprocess.call(cmd, shell=True, cwd=self.get_waf_directory(), timeout=timeout if timeout else None)

            self.postprocess(**args_dict)
            # proc.wait(timeout=timeout if timeout else None)
        except subprocess.TimeoutExpired:
            log.error ("Timeout expired. try setting a longer timeout")
        except Exception as e:
            log.error (e)
        finally:
            # will be done whatever the results
            #os.system("./mergepcaps.sh")
            # os.system("mergecap -w source.pcap test-1-1.pcap test-1-2.pcap")

            pass

        if ret:
            print("ERROR: command returned error code %d" % ret)
            # os.system("truncate --size=100000 %s" % (args.out,))
            # exit(1)


        print("Executed Command:\n%s" % cmd)

    def get_waf_directory(self):
        """
        Return the directory in which waf is and hence the working directory from where
        waf should be run
        """
        return self.wd


# class Ns3DefaultTest(DefaultTest):

class DceDefaultTest(DefaultTest):
    """

    """

    def init(self):
        pass
    
    @staticmethod
    def is_dce():
        return True

    def clean_dce_folders(self):
        """
        Remove files-* folders
        """
        pattern = os.path.join(self.get_waf_directory(), "files-*" )
        log.debug("Removing dce files with pattern [%s]" % pattern)
        for dirname in glob.glob(pattern):
            log.debug("Removing directory %s" % dirname)
            # os.rmdir(dirname) # won,'t work when empty
            shutil.rmtree(dirname)

    def clean(self):
        """
        Will remove files-*
        """
        super().clean()
        self.clean_dce_folders()
