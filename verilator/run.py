#!/usr/bin/env python3
"""Build the DSPPC603's Verilator model and replay a real chip's golden vectors.

    python verilator/run.py                 the DSPPC603 against the 603e run
    python verilator/run.py --only int      integer vectors only
    python verilator/run.py --name FMADD    one instruction (all its variants)
    python verilator/run.py --show 20       print more failures per instruction
    python verilator/run.py --csv x.csv     another vector file (see fpmodel.py)

It builds rtl/DSPPC603 and replays cputest/runs/results_603e_6300_run1.csv.
Other options are passed on to the test bench; `--help` lists them.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_ENV = "PIPPIN_BUILD"
# the real chip's results the model is checked against by default
DEFAULT_CSV = os.path.join(HERE, "..", "cputest", "runs", "results_603e_6300_run1.csv")


def build_dir():
    """Where the benches are built."""
    root = os.environ.get(BUILD_ENV) or os.path.join(
        os.path.expanduser("~"), ".cache", "applepippin", "verilator")
    return os.path.join(root, "cpu603")


def main():
    args = sys.argv[1:]
    args = [os.path.abspath(a) if os.path.isfile(a) else a for a in args]
    if "--csv" not in args and "--help" not in args and "-h" not in args:
        args += ["--csv", os.path.abspath(DEFAULT_CSV)]
    build = build_dir()
    os.makedirs(build, exist_ok=True)
    rc = subprocess.call(["make", "-s", "-C", HERE, "BUILD=" + build])
    if rc:
        print("build failed")
        return rc
    os.chdir(HERE)
    sys.stdout.flush()
    return subprocess.call([os.path.join(build, "vector_tb")] + args)


if __name__ == "__main__":
    sys.exit(main())
