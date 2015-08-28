#!/usr/bin/python
import os
import subprocess
import argparse
from . import test




class Test(test.DefaultTest):
    
    def init(self):
        self.parser.add_argument("--graph", "-g", action="store_true", help="Convert pcap to sqlite db and then plot")

    
    # def setup(self, graph, **kwargs):
        # if graph:
            # # TODO check it's ok
            # cmd= "%s/clean.sh" % self.get_root_folder()
            # subprocess.call(cmd, cwd=self.get_waf_directory())
            # # os.rmdir("%s/source" % self.get_waf_directory())
            # # os.rmdir("%s/source" % self.get_waf_directory())
            # #os.remove() #same as unlink

    # # def run(self):


    def postprocess(self, **kwargs):


        def print_result(folder):
            os.system("./dump_folder.sh %s" % (folder,))

        if kwargs.get('graph'):
            print("\n\n=== Outputs of node 0 (client) ===")
            print_result("~/dce/files-0/var/log/*")

            print("\n\n=== Outputs of node 1 (server) ===")
            print_result("~/dce/files-1/var/log/*")
        # if graph:
            # cwd= self.get_waf_directory() 
            # ns3testing=self.get_root_folder()
            # plot_folder=os.path.join(ns3testing, "./plots")
            # # plot_folder=ns3testipppng
            # os.environ["GNUPLOT_LIB"] = plot_folder
            # cmd=os.path.join(ns3testing ,"./draw_plots.sh")
            # ret = subprocess.call(cmd, cwd=cwd)
            
            # print("Launched command \n:%s\nFrom working directory %s" % (cmd, cwd))
