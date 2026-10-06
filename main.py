"""Stand-in for your program.

Maestro passes it one line of `parameters` from maestro.toml as arguments,
e.g. `-t 10 out.txt`. Replace it with your own code, and keep writing results
to the paths maestro.toml lists under `outputs`.
"""

import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-t", type=int, required=True, help="seconds to simulate")
parser.add_argument("--label", default="run", help="a name for this run")
parser.add_argument("output", help="file to write the result to")
args = parser.parse_args()

# Printed output is kept as the line's log.
print(f"simulating {args.t}s ({args.label})")
time.sleep(args.t)

with open(args.output, "w") as f:
    f.write(f"{args.label}: result after {args.t}s\n")
with open("/var/log/app/main.log", "a") as f:
    f.write(f"wrote {args.output}\n")

print("done")
