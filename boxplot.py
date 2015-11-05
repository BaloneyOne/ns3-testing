#!/usr/bin/python3
import pandas as pd
import glob
import matplotlib.pyplot as plt
import argparse

configs = dict()

configs[2] = [
    {"file": "linux_linux_2nRtrs_f30b30_f30b30_w40K_lia_default-run*.csv",  "title": "Linux/40KB"},
    {"file": "linux_linux_2nRtrs_f30b30_f30b30_w60K_lia_default-run*.csv",  "title": "Linux/60KB"},
    {"file": "linux_linux_2nRtrs_f30b30_f30b30_w80K_lia_default-run*.csv",  "title": "Linux/80KB"},
    {"file": "linux_linux_2nRtrs_f30b30_f30b30_w140K_lia_default-run*.csv", "title": "Linux/140KB"},
    {"file": "ns_ns_2nRtrs_f30b30_f30b30_w40K_lia_default-run*.csv",  "title": "ns/40KB"},
    {"file": "ns_ns_2nRtrs_f30b30_f30b30_w60K_lia_default-run*.csv",  "title": "ns/60KB"},
    {"file": "ns_ns_2nRtrs_f30b30_f30b30_w80K_lia_default-run*.csv",  "title": "ns/80KB"},
    {"file": "ns_ns_2nRtrs_f30b30_f30b30_w140K_lia_default-run*.csv", "title": "ns/140KB"},

  # list(file="ns_2rtrs_f30b30_f30b30_w40K_lia.csv", title="ns/2/40KB"),
  # list(file="ns_2rtrs_f30b30_f30b30_w60K_lia.csv", title="ns/2/60KB"),
  # list(file="ns_2rtrs_f30b30_f30b30_w80K_lia.csv", title="ns/2/80KB"),
  # list(file="ns_2rtrs_f30b30_f30b30_w140K_lia.csv", title="ns/2/140KB")
]

configs[1] = [
  {"file":"linux_1rtrs_f30b30_f30b30_w40K_lia-run*.csv", "title":"Linux/40KB"},
  {"file":"linux_1rtrs_f30b30_f30b30_w80K_lia-run*.csv", "title":"Linux/80KB"},
  {"file":"linux_1rtrs_f30b30_f30b30_w140K_lia-run*.csv", "title":"Linux/140KB"},

  # {"file":"ns_1rtrs_f30b30_f30b30_w40K_lia-run*.csv", "title":"ns/1/40KB"},
  # {"file":"ns_1rtrs_f30b30_f30b30_w80K_lia-run*.csv", "title":"ns/1/80KB"},
  # {"file":"ns_1rtrs_f30b30_f30b30_w140K_lia-run*.csv", "title":"ns/1/140KB"}
]


parser = argparse.ArgumentParser(description='Generate boxplots for MPTCP simulations')
parser.add_argument('nb_subflows', type=int, action="store", choices=configs.keys() )
#range(1, len(configs)))

args = parser.parse_args()
# Best way to load several similar csv files:
# http://stackoverflow.com/questions/25210819/speeding-up-data-import-function-pandas-and-appending-to-dataframe
frames = []

for config in configs[args.nb_subflows]:
    print("config: %s / %s" % (config["title"], config["file"]))
    # load all the 
    for filename in glob.glob("/home/teto/ns3testing/results/" + config["file"]):
        print("loading %s" % filename)
        df = pd.read_csv(filename)
        df["title"] = config["title"]
        frames.append(df,)
# print(frames)
result = pd.concat(frames,
                   ignore_index=True 
                   )
# print(result)

# fig = plt.figure()
# result.groupby("title").bits_per_second.boxplot(by="title") # kind="box")
ax = result.boxplot(column="bits_per_second", by="title", rot=45 )
fig = ax.get_figure()
output = "boxplot_%d.png" % args.nb_subflows
fig.savefig(output)

print(output)
