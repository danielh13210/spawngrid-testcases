import argparse
import sys
import os
import subprocess
from subprocess import CalledProcessError
from testtools import success, fail

parser=argparse.ArgumentParser(description="Run test cases for Spawn Grid Optimization Project")
parser.add_argument('repo',help="Repository to test")
parser.add_argument('testfile')
parser.add_argument("--build",'-b',help="Path to build.sh (default: ./build.sh)",default="./build.sh")
args=parser.parse_args()
os.chdir(args.repo)
print(f"Compiling program: run {args.build}")
try:
  subprocess.run(['/bin/bash',args.build],check=True)
  success("build successful")
except CalledProcessError:
  fail("cannot build",fatal=True)
if os.path.isfile('spawn_sim'):
  success("spawn_sim found")
else:
  fail("spawn_sim not found",fatal=True)
if os.access('spawn_sim',os.X_OK):
  success("spawn_sim is an executable file")
else:
  fail("spawn_sim is not executable",fatal=True)
try:
  out=subprocess.check_output(['readelf', '-h', 'spawn_sim'], text=True)
  out=out.splitlines()
  out=[[ part.strip() for part in line.strip().split(':')] for line in out] # strip and split
  for line in out:
    if line[0]=="Machine" and line[1]=="AArch64":
      success("AArch64 executable detected")
      aarch=True
      break
  if not aarch:
    fail("Executable not AArch64",fatal=True)
except CalledProcessError:
  fail("spawn_sim is not an ELF",fatal=True)


for testline in args.testfile.split(','):
  testfile,expectfile,repeats=testline.split(':')
  times=[]
  print(f"testing {testfile}")
  for i in range(int(repeats)):
    print(f"Iteration {i+1}")
    proc=subprocess.run(["./spawn_sim",testfile,"/dev/stderr"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    time=proc.stdout.decode('utf-8')
    time,unit=time.split()
    time=float(time)
    if unit=='ms':
      success("Unit is ms")
    else:
      fail("Wrong unit detected")
    print(time,'ms')
    out=proc.stderr
    expect=open(expectfile,'rb').read()
    if out==expect:
      success("Output correct")
    else:
      fail("Output incorrect")
    times.append(time)
  print("Mean:",sum(times)/len(times))