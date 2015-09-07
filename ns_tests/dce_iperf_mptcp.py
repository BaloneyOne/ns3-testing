#!/usr/bin/python
import os
import subprocess
import argparse
from . import test


class Test(test.DceDefaultTest):

    def get_parser(self):
        parser = self.get_default_parser()
        parser.add_argument("--graph", "-g", action="store_true", help="Convert pcap to sqlite db and then plot")
        parser.add_argument("--merge", action="store_true", help="Merge pcap")
        return parser

    @staticmethod
    def cover_tests():
        return [
            "dce-iperf-mptcp", 
            "dce-iperf-mptcp-mixed"
        ]

    def clean(self):
        super().clean()

    def _setup(self, **kwargs):
        super()._setup(**kwargs)
        if kwargs.get('graph'):
            # TODO check it's ok
            cmd = "%s/clean.sh" % self.get_root_folder()
            subprocess.call(cmd, cwd=self.get_waf_directory())
            # os.rmdir("%s/source" % self.get_waf_directory())
            # os.rmdir("%s/source" % self.get_waf_directory())
            # os.remove() #same as unlink

    # def run(self):

    def _postprocess(self, *args, **kwargs):
        super()._postprocess(args, kwargs)

        if kwargs.get('graph'):
            cwd = self.get_waf_directory() 
            ns3testing = self.get_root_folder()
            plot_folder = os.path.join(ns3testing, "./plots")
            # plot_folder=ns3testipppng
            os.environ["GNUPLOT_LIB"] = plot_folder
            cmd = os.path.join(ns3testing, "./draw_plots.sh")
            ret = subprocess.call(cmd, cwd=cwd)

            print("Launched command \n:%s\nFrom working directory %s" % (cmd, cwd))

        if kwargs.get('merge'):
            cmd = "mergecap -w {out} {input}".format(
                out=os.path.join(self.get_waf_directory(), "dce_iperf_mptcp.pcap"),
                input=os.path.join(self.get_waf_directory(), "iperf-mptcp-0-*.pcap")
            )
            # print('command=%s' % cmd)
            res = self.run_program(cmd, shell=True)

# Test test

# __all__ = [
        # 'test'
        # ]
