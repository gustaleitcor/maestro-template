"""Stand-in for your program: waits, then writes a result.

Its arguments are one line of `parameters` from maestro.toml.
"""

import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-t", type=int, required=True, help="seconds to wait")
parser.add_argument("--label", default="run", help="a name for this run")
parser.add_argument("output", help="file to write the result to")
args = parser.parse_args()

print(f"{args.label}: waiting {args.t}s")
time.sleep(args.t)

with open(args.output, "w") as f:
    f.write(f"{args.label}: done after {args.t}s\n")
print("done")
