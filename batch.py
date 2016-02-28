#!/usr/bin/python3.5
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import subprocess
import os
import argparse
import logging
import collections
import typing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

from enum import Enum


class Stack(Enum):
    ns = "ns"
    linux = "linux"


# Config = collections.namedtuple(
#     "Config", "client_stack server_stack window run forward0 backward0 forward1 backward1 cc scheduler  nb_rtrs"
# )

# http://stackoverflow.com/questions/11351032/named-tuple-and-optional-keyword-arguments
# Config.__new__.__defaults__ = {"client_stack":None}

# import collections
# TODO use typing.NamedTuple to check for types :
# Stack
def namedtuple_with_defaults(typename, field_names, default_values=[]):
    T = collections.namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, collections.Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T

Config = namedtuple_with_defaults(
    "Config", 
    "client_stack server_stack window run forward0 backward0 forward1 backward1 cc scheduler  nb_rtrs",
    { 
        'scheduler': 'roundrobin',
        # "run": "*",
        "nb_rtrs": 2,
        "cc": "lia",
        "forward0": 30,
        "forward1": 30,
        "backward0": 30,
        "backward1": 30,
    }
)


# utiliser python3.5 avec des type hints pour le named tuple
def gen_filename(
    # client_stack, server_stack, window, run="*", cc="lia", scheduler="roundrobin", nb_rtrs=2,
    # forward0="*", backward0="*",
    # forward1="*", backward1="*"
    conf: Config
) -> str:
    prefix = "{c.client_stack.value}_{c.server_stack.value}_{c.nb_rtrs}nbRtrs_f{c.forward0}b{c.backward0}_f{c.forward1}b{c.backward1}_w{c.window}_{c.cc}_{c.scheduler}-run{c.run}".format(
        c=conf
        # ._asdict()
        # client_stack=client_stack.value,
        # server_stack=server_stack.value,
        # forward0=forward0,
        # forward1=forward1,
        # backward0=backward0,
        # backward1=backward1,
        # cc=cc,
        # window=window,
        # nb_rtrs=nb_rtrs,
        # run=run,
        # scheduler=scheduler,
    )
    return prefix


def run_unit_test(
    # client_stack, server_stack, window, run, cc="lia", scheduler="roundrobin", nb_rtrs=2,
    # forward0=30, backward0=30,
    # forward1=30, backward1=30
    conf: Config
):
    """
    default = FastestRttFirst
    """
    # assert isinstance(client_stack, Stack)
    # assert isinstance(server_stack, Stack)
    # conf = Config(client_stack, server_stack, window, run, cc, scheduler, nb_rtrs, forward0, backward0, forward1, backward1)

    print(dir(conf))
    print(conf.client_stack)
    print(conf._asdict())
    # todo check the export of NS_RUN is correct ?
    # prefix = gen_filename(client_stack, server_stack, window, run, cc, scheduler, nb_rtrs, forward0, backward0, forward1, backward1)
    prefix = gen_filename(conf)

  # RngRun=
  # os.environ['NS_RUN'] = str(run)
  # os.environ['NS_GLOBAL_VALUE'] = "ChecksumEnabled=1"

    cmd = [
        "./unit_test.sh", prefix, 
        "--nRtrs=%d" % conf.nb_rtrs, 
        "--client_stack=%s" % conf.client_stack.value, 
        "--server_stack=%s" % conf.server_stack.value, 
        "--forwardDelay0=%d" % conf.forward0, "--forwardDelay1=%d" % conf.forward1,
        "--backwardDelay0=%d" % conf.backward0, "--backwardDelay1=%d" % conf.backward1,
        "--scheduler=%s" % conf.scheduler,
        "--window=%s" % conf.window,
        # these functions require the script to have a CmdParser else you need to export to the env
        "--ChecksumEnabled=1",
        "--RngRun=%d" % conf.run,
    ]
    cmd = ' '.join(cmd)
    print("command= %s\n" % cmd)
    # env = {'NS_GLOBAL_VALUE': "ChecksumEnabled=1", }
    proc = subprocess.call(cmd, shell=True)
    # os.system("./unit_test.sh"

# windows_small = ["10K","20K", "30K", "40K", "50K", "60K", "200K"]
windows_small = ["10K", "30K", "60K", "400K"]
windows_big = ["40K","60K", "80K", "140K", "400K", "1M" ]

def run_ns_1(run):
    # confs = [
        # Config(run=run, nb_rtrs=1, client_stack=Stack.ns, server_stack=Stack.ns, window="40K"),
        # Config(run=run, nb_rtrs=1, client_stack=Stack.ns, server_stack=Stack.ns, window="60K"),
        # Config(run=run, nb_rtrs=1, client_stack=Stack.ns, server_stack=Stack.ns, window="80K"),
        # Config(run=run,  client_stack=Stack.ns, server_stack=Stack.ns, window="140K")
    # ]
    confs = [ Config(run=run, nb_rtrs=1, client_stack=Stack.ns, server_stack=Stack.ns, window=X) for X in windows_small ]
    return confs


def run_ns_2(run):
    # return [
        # Config(run=run, client_stack=Stack.ns, server_stack=Stack.ns, window="40K"),
        # Config(run=run, client_stack=Stack.ns, server_stack=Stack.ns, window="60K"),
        # Config(run=run, client_stack=Stack.ns, server_stack=Stack.ns, window="80K"),
        # Config(run=run, client_stack=Stack.ns, server_stack=Stack.ns, window="140K"),
        # Config(run=run, client_stack=Stack.ns, server_stack=Stack.ns, window="400K"),
        # Config(run=run, client_stack=Stack.ns, server_stack=Stack.ns, window="1M"),
    # ]

  return [ Config(run=run, client_stack=Stack.ns, server_stack=Stack.ns, window=X) for X in windows_small ]


def run_linux_1(run):
    return [ Config(run=run, nb_rtrs=1, client_stack=Stack.linux, server_stack=Stack.linux, window=X) for X in windows_small ]
    # return [
        # Config(run=run, nb_rtrs=1, client_stack=Stack.linux, server_stack=Stack.linux, window="40K"),
        # Config(run=run, nb_rtrs=1, client_stack=Stack.linux, server_stack=Stack.linux, window="60K"),
        # Config(run=run, nb_rtrs=1, client_stack=Stack.linux, server_stack=Stack.linux, window="80K"),
        # Config(run=run, nb_rtrs=1, client_stack=Stack.linux, server_stack=Stack.linux, window="140K")
    # ]


def run_linux_2(run):
  # windows = ["40K","60K"]
  return [ Config(run=run, client_stack=Stack.linux, server_stack=Stack.linux, window=X) for X in windows_small ]

    # return [
        # Config(run=run, client_stack=Stack.linux, server_stack=Stack.linux, window="40K"),
        # Config(run=run, client_stack=Stack.linux, server_stack=Stack.linux, window="60K"),
        # Config(run=run, client_stack=Stack.linux, server_stack=Stack.linux, window="80K"),
        # Config(run=run, client_stack=Stack.linux, server_stack=Stack.linux, window="140K"),
        # Config(run=run, client_stack=Stack.linux, server_stack=Stack.linux, window="400K"),
        # Config(run=run, client_stack=Stack.linux, server_stack=Stack.linux, window="1M"),
    # ]


def run_basic_linux(run, nb=1):
  # run_unit_test(run=run, client_stack=Stack.ns, server_stack=Stack.ns, window="40K")
    return [
        Config(run=run, nb_rtrs=nb, client_stack=Stack.linux, server_stack=Stack.linux, window="400K")
    ]


def run_basic_ns(run, nb=1):
    return [
        Config(run=run, nb_rtrs=nb, client_stack=Stack.ns, server_stack=Stack.ns, window="400K")
    ]


def run_hybrid1(run) -> list:
    return [
        Config(run=run, nb_rtrs=1, client_stack=Stack.ns, server_stack=Stack.linux, window="40K"),
        Config(run=run, nb_rtrs=1, client_stack=Stack.linux, server_stack=Stack.ns, window="40K"),
    ]


def run_hybrid2(run):
    return [
        Config(run=run, client_stack=Stack.ns, server_stack=Stack.linux, window="40K"),
        Config(run=run, client_stack=Stack.linux, server_stack=Stack.ns, window="40K")
    ]


# list available generating functions
tests = {
    'ns2': run_ns_2,
    'ns': run_ns_1,
    'linux': run_linux_1,
    'linux2': run_linux_2,
    'basic_linux': run_basic_linux,
    'basic_ns': run_basic_ns,
    'hybrid1': run_hybrid1,
    'hybrid2': run_hybrid2,
}


def main():
  parser = argparse.ArgumentParser(description="To run xp")
  parser.add_argument('mode', choices=tests.keys())
  # parser.add_argument('--seed')
  argcomplete.autocomplete(parser)
  args = parser.parse_args()
  # nb_of_runs
  for run in range(1):
    # os.environ['NS_RUN'] = str(run)
    for config in tests[args.mode](run):
        run_unit_test(config)


if __name__ == '__main__':
    main()
