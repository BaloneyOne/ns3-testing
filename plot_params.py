#!/usr/bin/python3.5
import os
import collections
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import glob
import shlex, subprocess
from typing import Callable


prefixes = [
  "meta",
  # "subflow0",
  # "subflow1",
]


Config = collections.namedtuple("Config", "filename, field, legend")
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

def gen_tx_config(prefix: str) -> list:
  return [   
    Config("%s_TxNext.csv" % prefix, "newNextTxSequence", "%s Tx Next" % prefix),
    Config("%s_TxUnack.csv" % prefix, "newUnackSequence", "%s Tx Unack" % prefix),
  ]

def gen_configs(nb_of_subflows: int, with_meta: bool, gen_conf: Callable[[str], list]) -> list:
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

def plot_tx(folder, configs: list, output ):
  """
  Plt TxNext and TxUnack
  """
  fig = plt.figure(figsize=(8,8))
  ax = fig.gca()
  legends = []
  for config in configs:
    filename = os.path.join(folder, config.filename)
    d = pd.read_csv(filename , index_col="Time")
    # d2 = pd.read_csv(txUnackFilename, index_col="Time")
    
    # TODO augmenter la police
    ax = d[config.field].plot.line(ax=ax, grid=True, lw=3)
    # ax = d2["newUnackSequence"].plot.line(ax=ax)
    legends.append( config.legend)

  plt.legend(legends)
  fig.savefig(output)



def main():
  parser = argparse.ArgumentParser(description="Plots various ns parameters")
# type=argparse.FileType(mode=) 
  parser.add_argument("folder", help="Choose client or server folder")
  parser.add_argument("--out","-o", action="store", type=str, help="Create a choose output filename")
  parser.add_argument("--display", "-d", action="store_true", default=False, help="Display picture")

  args = parser.parse_args()
  i = 0
  # plt.title("Highest Tx vs NextTx")
  plot_tx(args.folder, gen_configs(2, False, gen_cwnd_config), "subflows_cwnd.png")
  plot_tx(args.folder, gen_configs(0, True, gen_cwnd_config), "meta_cwnd.png")
  
  # RWND
  plot_tx(args.folder, gen_configs(0, True, gen_rwnd_config), "meta_rwnd.png")

  # Rx
  plot_tx(args.folder, gen_configs(2, False, gen_rx_config), "subflows_rx.png")
  plot_tx(args.folder, gen_configs(0, True, gen_rx_config), "meta_rx.png")

  # TX plots
  plot_tx(args.folder, gen_configs(2, False, gen_tx_config), "tx_subflows.png")
  plot_tx(args.folder, gen_configs(0, True, gen_tx_config), "tx_meta.png")

  if args.out:
    # todo generate montage and plot it ?!
    cmd = "montage tx_meta.png tx_subflows.png meta_rx.png subflows_rx.png meta_cwnd.png subflows_cwnd.png meta_rwnd.png -tile 2x4 -geometry +1+1 %s" % (args.out)
    subprocess.call( shlex.split(cmd),)
    if args.display:
      os.system("sxiv %s" % args.out)
  # montage for both nodes
  # montage server_recap.png source_recap.png -tile 2x1 -geometry +1+1 all.png 

if __name__ == "__main__":
    main()
    
