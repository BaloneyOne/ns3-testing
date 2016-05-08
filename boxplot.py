#!/usr/bin/python3.5
import pandas as pd
import glob
import matplotlib.pyplot as plt
import argparse
import batch as b


configs = dict()


def gen_title(conf: b.Config) -> str:
    """
    Those are "B"ytes !
    """
    return "{0.client_stack.value}/{0.window:>4}B".format(conf)

def boxplot1():
    return b.run_ns_1("*") + b.run_linux_1("*")


def boxplot2():
    return b.run_ns_2("*") + b.run_linux_2("*")

configs[2] = boxplot2()
configs[1] = boxplot1()

# print(two_paths)
# TODO reprendre les configs qui sont dans le batch
# def gen_config():
#     def gen_title(stack, window):
#         return "{stack}/{window:>3}".format(stack=stack.value, window)
#     return {"file": gen_filename(), "title": client_stack.value}

# configs[2] = [
#     {"file": "linux_linux_2nRtrs_f30b30_f30b30_w40K_lia_default-run*.csv",  "title": "Linux/ 40KB"},
#     {"file": "linux_linux_2nRtrs_f30b30_f30b30_w60K_lia_default-run*.csv",  "title": "Linux/ 60KB"},
#     {"file": "linux_linux_2nRtrs_f30b30_f30b30_w80K_lia_default-run*.csv",  "title": "Linux/ 80KB"},
#     {"file": "linux_linux_2nRtrs_f30b30_f30b30_w140K_lia_default-run*.csv", "title": "Linux/140KB"},
#     {"file": "ns_ns_2nRtrs_f30b30_f30b30_w40K_lia_default-run*.csv",  "title": "ns/ 40KB"},
#     {"file": "ns_ns_2nRtrs_f30b30_f30b30_w60K_lia_default-run*.csv",  "title": "ns/ 60KB"},
#     {"file": "ns_ns_2nRtrs_f30b30_f30b30_w80K_lia_default-run*.csv",  "title": "ns/ 80KB"},
#     {"file": "ns_ns_2nRtrs_f30b30_f30b30_w140K_lia_default-run*.csv", "title": "ns/140KB"},

#   # list(file="ns_2rtrs_f30b30_f30b30_w40K_lia.csv", title="ns/2/40KB"),
#   # list(file="ns_2rtrs_f30b30_f30b30_w60K_lia.csv", title="ns/2/60KB"),
#   # list(file="ns_2rtrs_f30b30_f30b30_w80K_lia.csv", title="ns/2/80KB"),
#   # list(file="ns_2rtrs_f30b30_f30b30_w140K_lia.csv", title="ns/2/140KB")
# ]

# configs[1] = [
#   {"file":"linux_1rtrs_f30b30_f30b30_w40K_lia-run*.csv", "title":"Linux/40KB"},
#   {"file":"linux_1rtrs_f30b30_f30b30_w80K_lia-run*.csv", "title":"Linux/80KB"},
#   {"file":"linux_1rtrs_f30b30_f30b30_w140K_lia-run*.csv", "title":"Linux/140KB"},

#   # {"file":"ns_1rtrs_f30b30_f30b30_w40K_lia-run*.csv", "title":"ns/1/40KB"},
#   # {"file":"ns_1rtrs_f30b30_f30b30_w80K_lia-run*.csv", "title":"ns/1/80KB"},
#   # {"file":"ns_1rtrs_f30b30_f30b30_w140K_lia-run*.csv", "title":"ns/1/140KB"}
# ]


parser = argparse.ArgumentParser(description='Generate boxplots for MPTCP simulations')
parser.add_argument('nb_subflows', type=int, action="store", choices=configs.keys())
#range(1, len(configs)))

args = parser.parse_args()
# Best way to load several similar csv files:
# http://stackoverflow.com/questions/25210819/speeding-up-data-import-function-pandas-and-appending-to-dataframe
frames = []

# print(b.run_ns_1("*"))
# print (configs[2])
for config in configs[args.nb_subflows]:
    # print("config: %s " % (config))
    # load all the 
    for filename in glob.glob("/home/teto/ns3testing/results/" + b.gen_filename(config) + ".csv"):
        print("loading %s" % filename)
        df = pd.read_csv(filename)
        # TODO generer le titre
        df["title"] = gen_title(config)
        frames.append(df,)
# print(frames)
result = pd.concat(frames,
                   ignore_index=True 
                   )
# print(result)

# fig = plt.figure()
# result.groupby("title").bits_per_second.boxplot(by="title") # kind="box")
ax = result.boxplot(
    column="bits_per_second", 
    by="title",
    # title="Throughput comparison between the linux and ns3 implementations", 
    # xlabel=""
    rot=45 
)
fig = ax.get_figure()
# plt.suptitle("Throughput comparison between the linux and ns3 implementations")
# get rid of the automatic 'Boxplot grouped by group_by_column_name' title

plt.suptitle("")
plt.title("")
# plt.annotate("")
ax.set_xlabel("")
ax.set_ylabel("Bits per second")
output = "boxplot_%d.png" % args.nb_subflows
fig.savefig(output)

print(output)
