#!/usr/bin/python
import subprocess
import argparse
import logging
import os
import glob
import shutil

# parser = argparse.ArgumentParser()

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)
print("__name__", __name__)
log.addHandler(logging.NullHandler())
# log.addHandler(logging.FileHandler("test.log", mode="w"))


class DefaultTest:
    """
    Allow to run preprocess and postprocess scripts automatically
    """

    # parser = None

    def __init__(self, working_directory, type):

        self.wd = working_directory
        self.type = type
        # self.parser = parser
        log.info("created instance of %r" % self) 
        self.init()

    def init(self):
        pass

    @staticmethod
    def cover_tests():
        """
        Returns a list of tests for which this is valid
        """
        return []

    @staticmethod
    def get_default_parser():

        parser = argparse.ArgumentParser(description="Helper to debug mptcp")
#  nargs='?',
        # parser.add_argument("program", choices=available_programs, help="Launch gdb")
        parser.add_argument("program", type=str, help="Launch gdb")

        parser.add_argument("--clean", "-c", action="store_const", const=True, help="Remove files that could be misinterpreted")
        return parser

    def get_parser(self):
        """
        """
        return self.get_default_parser()

    @staticmethod
    def load_log(filename):
        """
        Load NS_LOG from a file, return parsed value
        """
        ns_log = ''
        with open(filename, 'r') as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                ns_log += line.strip()
        return ns_log

    @staticmethod
    def is_dce():
        return False

    def get_type(self):
        """ Is it a "test" or an "example" """
        return self.get_type

    def get_root_folder(self):
        """
        Returns ns3testing folder
        """
        root = os.path.dirname(os.path.abspath(__file__))
        root = os.path.join(root, "../")
        return root

    def _setup(self, *args, **kw):
        """
        Pre hooks, executed before the running command
        """
        log.debug('setup called with parameters %r' % kw)
        if kw.get('clean'):
            self.clean()

    def _postprocess(self, *args, **kwargs):
        """
        Operations run after the test (post-hooks)
        """
        log.info("Starting Postprocessing with parameters %s and %s" % (args, kwargs) )

    @staticmethod
    def clean_pcaps(directory):
        log.info('removing pcap files')
        for pcap in glob.glob(os.path.join(directory, "*.pcap")):
            log.debug("Removing pcap %s" % pcap)
            os.remove(pcap)

    def clean(self):
        log.info('Cleaning')
        self.clean_pcaps(self.get_waf_directory())

    @staticmethod
    def _convert_args_into_dict(args):
        return vars(args)

    def run_program(self, cmd, **kwargs):
        """
        TODO return a named tuple ret/stdout/stderr
        """

        log.info(cmd)
        print("Running external program:\n%s" % cmd)
        ret = 0
        try:
            # cwd=self.get_waf_directory(), timeout=timeout if timeout else None
            ret = subprocess.call(cmd, kwargs)

            # proc.wait(timeout=timeout if timeout else None)

        except subprocess.TimeoutExpired:
            log.error("Timeout expired. try setting a longer timeout")
            ret = -1
        except Exception as e:
            log.error(e)
            ret = -1
        finally:
            # will be done whatever the results
            pass
        return ret

    def run(self, debug, redirect, cli_args):
        """
        cli_args are then passed to the argument parser, should be a list
        """
        log.debug("Run with debug=%s" % (debug))
        timeout = None

        parser = self.get_parser()
        # args = parser.parse_args(cli_args)
        args, unknown_args = parser.parse_known_args(cli_args)

        args_dict = self._convert_args_into_dict(args)
        print(args_dict)
        # if args.load_log:
        #     ns_log = self.load_log(args.load_log)
        #     log.info("Setting NS_LOG to:\n%s" % ns_log)
        #     os.environ['NS_LOG'] = ns_log

        log.debug("Just before running setup")
        self._setup(**args_dict)

        extra_params = "--suite=%s " % args.program if self.type == "test" else ""
        extra_params += ' '.join(list(unknown_args))

        if debug:
            cmd = "./waf --run {program} --command-template=\"gdb -ex 'run {extra_params} {tofile}' --args %s \" "
        else:
            timeout = 200
            cmd = "./waf --run \"{program} {extra_params} \" {tofile}"

        tofile = " > %s 2>&1" % redirect if redirect else ""
        cmd = cmd.format(
            extra_params=extra_params,
            program="test-runner" if self.type == "test" else args.program,
            tofile=tofile,
            fullness="QUICK",
        )

        log.debug("Changing working directory to %s" % (self.get_waf_directory()))
        log.info(cmd)
        print("Executed Command:\n%s" % cmd)
        ret = 0
        try:

            ret = subprocess.call(cmd, shell=True, cwd=self.get_waf_directory(), timeout=timeout if timeout else None)

            if ret == 0:
                log.info("Command successful, moving on to postprocessing....")
                self._postprocess(**args_dict)
            else:
                log.info("Command failed with errcode %d" % ret)
            # proc.wait(timeout=timeout if timeout else None)
        except subprocess.TimeoutExpired:
            log.error("Timeout expired. try setting a longer timeout")
        except Exception as e:
            log.error(e)
        finally:
            # will be done whatever the results
            pass

        print("Executed Command:\n%s" % cmd)
        return ret

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

    @staticmethod
    def clean_dce_folders(directory):
        """
        Remove files-* folders
        """
        pattern = os.path.join(directory, "files-*")
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
        self.clean_dce_folders(self.get_waf_directory())
