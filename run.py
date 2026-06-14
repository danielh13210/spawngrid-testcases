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
