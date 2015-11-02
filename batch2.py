#!/usr/bin/python3.4
import subprocess
import os
import argparse

from enum import Enum

class Stack(Enum):
  ns = "ns"
  linux= "linux"

def run_unit_test(
    clientStack, serverStack, window, run, cc="lia", scheduler="default", nRtrs=2,
                  forward0=30, backward0=30,
                  forward1=30, backward1=30
):
  """
  default = FastestRttFirst
  """
  assert isinstance(clientStack, Stack)
  # todo check the export of NS_RUN is correct ?
  prefix= "{clientStack}_{serverStack}_{nRtrs}nRtrs_f{forward0}b{backward0}_f{forward1}b{backward1}_w{window}_{cc}_{scheduler}-run{run}".format(
          clientStack=clientStack.value,
    serverStack=serverStack.value,
    forward0=forward0,
    forward1=forward1,
    backward0=backward0,
    backward1=backward1,
    cc=cc,
    window=window,
    nRtrs=nRtrs,
    run=run,
    scheduler=scheduler,
  )

  cmd = [ "./unit_test.sh", prefix, "--nRtrs=%d" % nRtrs, "--clientStack=%s" % clientStack.value, "--serverStack=%s" % serverStack.value, 
         "--forwardDelay0=%d" % forward0, "--forwardDelay1=%d" % forward1,
         "--backwardDelay0=%d" % backward0, "--backwardDelay1=%d" % backward1,
         "--scheduler=%s" % scheduler,
         "--window=%s" % window,
         ]
  cmd = ' '.join(cmd)
  print("command= %s\n"% cmd)
  os.environ['NS_RUN'] = str(run)
  os.environ['NS_GLOBAL_VALUE'] = "ChecksumEnabled=1"

  # env = {'NS_GLOBAL_VALUE': "ChecksumEnabled=1", }
  proc = subprocess.call(cmd, shell=True)
  # os.system("./unit_test.sh"



def run_test1(run):
  run_unit_test(run=run, nRtrs=1, clientStack=Stack.ns, serverStack=Stack.ns, window="40K")
  run_unit_test(run=run, nRtrs=1, clientStack=Stack.ns, serverStack=Stack.ns, window="60K")
  run_unit_test(run=run, nRtrs=1, clientStack=Stack.ns, serverStack=Stack.ns, window="80K")
  run_unit_test(run=run, nRtrs=1, clientStack=Stack.ns, serverStack=Stack.ns, window="140K")

def run_test2(run):
  run_unit_test(run=run, clientStack=Stack.ns, serverStack=Stack.ns, window="40K")
  run_unit_test(run=run, clientStack=Stack.ns, serverStack=Stack.ns, window="60K")
  run_unit_test(run=run, clientStack=Stack.ns, serverStack=Stack.ns, window="80K")
  run_unit_test(run=run, clientStack=Stack.ns, serverStack=Stack.ns, window="140K")


def run_test3(run):
  run_unit_test(run=run, nRtrs=1, clientStack=Stack.linux, serverStack=Stack.linux, window="40K")
  run_unit_test(run=run, nRtrs=1, clientStack=Stack.linux, serverStack=Stack.linux, window="60K")
  run_unit_test(run=run, nRtrs=1, clientStack=Stack.linux, serverStack=Stack.linux, window="80K")
  run_unit_test(run=run, nRtrs=1, clientStack=Stack.linux, serverStack=Stack.linux, window="140K")

def run_test4(run):
  run_unit_test(run=run, clientStack=Stack.linux, serverStack=Stack.linux, window="40K")
  run_unit_test(run=run, clientStack=Stack.linux, serverStack=Stack.linux, window="60K")
  run_unit_test(run=run, clientStack=Stack.linux, serverStack=Stack.linux, window="80K")
  run_unit_test(run=run, clientStack=Stack.linux, serverStack=Stack.linux, window="140K")

def run_test5(run):
  # run_unit_test(run=run, clientStack=Stack.ns, serverStack=Stack.ns, window="40K")
  run_unit_test(run=run, clientStack=Stack.linux, serverStack=Stack.linux, window="40K")
    # Hybrid
  # run_unit_test(run=run, clientStack=Stack.ns, serverStack=Stack.linux, window="40K")


# list available generating functions
tests = {
  'ns2': run_test2,
  'ns': run_test1,
  'linux': run_test3,
  'linux2': run_test4,
  'test': run_test5,
}


def main():
  parser = argparse.ArgumentParser(description="To run xp")
  parser.add_argument('mode', choices=tests.keys())
  # parser.add_argument('--seed')

  args = parser.parse_args()
  # nb_of_runs
  for run in range(1):
    # os.environ['NS_RUN'] = str(run)
    tests[args.mode](run)




# ./unit_test.sh "ns_2rtrs_f30b30_f30b30_w40K_lia" --nRtrs=2 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="40K"
# ./unit_test.sh "ns_2rtrs_f30b30_f30b30_w60K_lia" --nRtrs=2 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="60K"
# ./unit_test.sh "ns_2rtrs_f30b30_f30b30_w80K_lia" --nRtrs=2 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="80K"
# ./unit_test.sh "ns_2rtrs_f30b30_f30b30_w140K_lia" --nRtrs=2 --clientStack=ns --serverStack=ns --forwardDelay0=30 --backwardDelay0=30 --forwardDelay1=30 --backwardDelay1=30 --window="140K"



if __name__ == '__main__':
  main()
