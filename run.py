import argparse
import sys
import os
import subprocess
from subprocess import CalledProcessError
from testtools import success, fail

parser=argparse.ArgumentParser(description="Run test cases for Spawn Grid Optimization Project")
parser.add_argument('repo',help="Repository to test")
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

