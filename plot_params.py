#!/usr/bin/python3.5
import os
import collections
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import glob
import shlex, subprocess
import logging


from typing import Callable


log = logging.getLogger("mptcpanalyzer")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

attributes = {
        "txNext" : "{type} Tx Next",
        "highestSeq" : "{type} Highest seq",
        "unackSeq" : "{type} SND.UNA",
    "rxNext": "",
    "rxAvailable": "",
    "rxTotal" : " rxtotal",
    "cwnd": "{type} cwnd",
    "rWnd": "RWnd",
    "ssThresh": "{type} SS Thresh",
    "state": "State",
    }

prefixes = [
  "meta",
  # "subflow0",
  # "subflow1",
]


Config = collections.namedtuple("Config", "pattern, type")
# tx_configs = [
  # Config("meta_TxNext.csv", "newNextTxSequence", "Meta Tx Next"),
  # Config("meta_TxUnack.csv", "newUnackSequence", "Meta Tx Unack"),
# ]

# rwnd_configs = [
  # Config("meta_rwnd.csv", "newRwnd", "Meta Rcv window"),
  # # Config("subflow0_rwnd.csv", "newRwnd", "Subflow 1 Rcv window"),
# ]

# cwnd_configs = [
  # Config("meta_cwnd.csv", "newCwnd", "Meta wnd"),
  # Config("subflow0_cwnd.csv", "newCwnd", "Subflow 1 wnd"),
  # Config("subflow1_cwnd.csv", "newCwnd", "Subflow 2 wnd"),
# ]

# rx_configs = [
  # Config("meta_RxAvailable.csv", "newRxAvailable", "RxAvailable (no out of order)"),
  # Config("meta_RxNext.csv", "newRxNext", "RxNext"),
  # Config("meta_RxTotal.csv", "newRxTotal", "RxTotal (out of order included)"),
# ]

def gen_rwnd_config(prefix: str) -> list:
  return [   
      Config("%s_rwnd.csv" %prefix, "newRwnd", "Rcv window of %s" % prefix),

  ]

# def gen_tx_config(prefix: str) -> list:
#   return [   
#     Config("%s_TxNext.csv" % prefix, "newNextTxSequence", "%s Tx Next" % prefix),
#     Config("%s_TxUnack.csv" % prefix, "newUnackSequence", "%s Tx Unack" % prefix),
#   ]

def gen_configs(with_meta: bool, gen_conf: Callable[[str], list]) -> list:
  """
  """
  # def gen_tx_config(prefix: str) -> list:
    # return [   Config("meta_TxNext.csv" % prefix, "newNextTxSequence", "Meta Tx Next"),
              # Config("%s_TxUnack.csv" % prefix, "newUnackSequence", "Meta Tx Unack"),
             # ]
  
  configs = []
  if with_meta:
    configs += gen_conf("meta")

  for i in range(nb_of_subflows):
    configs += gen_conf("subflow%d" % i)

  return configs

def gen_cwnd_config(prefix: str) -> list:
  return [  Config("%s_cwnd.csv" % prefix, "newCwnd", "%s wnd" % prefix) ]


# def gen_cwnd_configs(nb_of_subflows: int, with_meta: bool) -> list:
  # """
  # """
  # def gen_cwnd_config(prefix: str) -> list:
    # return [  Config("%s_cwnd.csv" % prefix, "newCwnd", "%s wnd" % prefix) ]
  
  # cwnd_configs = []
  # if with_meta:
    # cwnd_configs += gen_cwnd_config("meta")

  # for i in range(nb_of_subflows):
    # cwnd_configs += gen_cwnd_config("subflow%d" % i)

  # return cwnd_configs

def gen_rx_config(prefix: str) -> list:
  return [Config("%s_RxAvailable.csv" % prefix, "newRxAvailable", "RxAvailable (no out of order)"),
          Config("%s_RxNext.csv"% prefix, "newRxNext", "RxNext"),
          Config("%s_RxTotal.csv"% prefix, "newRxTotal", "RxTotal (out of order included)"),
          ]


# def gen_rx_configs(nb_of_subflows: int, with_meta: bool) -> list:
  # def gen_rx_config(prefix):
    # return [Config("%s_RxAvailable.csv" % prefix, "newRxAvailable", "RxAvailable (no out of order)"),
            # Config("%s_RxNext.csv"% prefix, "newRxNext", "RxNext"),
            # Config("%s_RxTotal.csv"% prefix, "newRxTotal", "RxTotal (out of order included)"),
            # ]
  
  # rx_configs = [] 
  # if with_meta:
    # rx_configs += gen_rx_config("meta")

  # for i in range(nb_of_subflows):
      # rx_configs += gen_rx_config( "subflow%d" % i)
  # return rx_configs

# slow start plot
ss_plots = [

]

def plot(node, attribute, with_meta : bool, with_subflows : bool, output ):
    """
    Plot column "attribute" to "output" file (*.png)


    """
    fig = plt.figure(figsize=(8,8))
    ax = fig.gca()
    legends = []
    configs = []

    if with_meta:
        log.debug ("With meta")
        configs.append ( Config(str(node) + "*meta*.csv"), "meta")

    if with_subflows:

        log.debug ("With subflows")
        configs.append ( Config(str(node) + "*subflow*.csv"), "Subflow")


    for config in configs:

        matches = glob.glob(config.pattern)
        if matches is None:
            raise Exception("No meta file found")
        d = pd.read_csv(filename , index_col="Time")
        print(d)
# TODO augmenter la police
        ax = d[ attributes[attribute] ].plot.line(ax=ax, grid=True, lw=3)
# ax = d2["newUnackSequence"].plot.line(ax=ax)
        # TODO retrieve legend from attributes + type
        legends.append( "toto")

    plt.legend(legends)
    fig.savefig(output)



def main():
    """
    Everytime generate for both nodes right ?
    """
    parser = argparse.ArgumentParser(description="Plots various ns parameters")
# type=argparse.FileType(mode=) 
    # parser.add_argument("folder", help="Choose client or server folder")
    parser.add_argument("attribute", choices=attributes, help="Choose client or server folder")
    parser.add_argument("--out","-o", action="store", type=str, default=None, help="Create a choose output filename")
    parser.add_argument("--display", "-d", action="store_true", default=False, help="Display picture")
    parser.add_argument("--meta", "-m", action="store_true", default=False, help="Plot meta along")
    parser.add_argument("--subflows", "-s", action="store_true", default=False, help="Plot subflows along")

    args, unknown = parser.parse_known_args()

    output = args.out

    for node in [0,1]:

        if not args.out:
            output = args.attribute + str(node) + ".png"

        log.info("Output set to %s" % output)

             
        plot (node, args.attribute, args.meta, args.subflows, output)
# plt.title("Highest Tx vs NextTx")
# plot_tx(args.folder, gen_configs(2, False, gen_cwnd_config), "subflows_cwnd.png")
# plot_tx(args.folder, gen_configs(0, True, gen_cwnd_config), "meta_cwnd.png")

# # RWND
# plot_tx(args.folder, gen_configs(0, True, gen_rwnd_config), "meta_rwnd.png")

# # Rx
# plot_tx(args.folder, gen_configs(2, False, gen_rx_config), "subflows_rx.png")
# plot_tx(args.folder, gen_configs(0, True, gen_rx_config), "meta_rx.png")

# TX plots
# plot_tx(args.folder, gen_configs(0, True, gen_tx_config), "tx_meta.png")

    if args.out:
# todo generate montage and plot it ?!
# move outside !
#   glob all pngs and count them to generate -tile
        cmd = "montage tx_meta.png tx_subflows.png meta_rx.png subflows_rx.png meta_cwnd.png subflows_cwnd.png meta_rwnd.png -tile 2x4 -geometry +1+1 %s" % (args.out)
        subprocess.call( shlex.split(cmd),)

        if args.display:
            os.system("sxiv %s" % args.out)
# montage for both nodes
# montage server_recap.png source_recap.png -tile 2x1 -geometry +1+1 all.png 




if __name__ == "__main__":
    main()

