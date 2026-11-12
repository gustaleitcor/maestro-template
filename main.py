"""Takes up a container's CPUs and memory for a while, and writes report.json.

It does no useful work: it is a stress test of Maestro's scheduler. Its
arguments are one line of `parameters` from maestro.toml, or one that
genvrs.py yielded: `sleep 30`, `mix 90 --fraction 0.7 --samples`.

  sleep  waits, holding nothing: the line only reserves its cpus and memory
  burn   keeps every core it was given busy
  hold   fills part of its memory and keeps touching it
  mix    burn and hold at once
"""

import argparse
import json
import multiprocessing
import os
import resource
import sys
import time
from multiprocessing.process import BaseProcess

# What Python itself takes before hold allocates anything, in MB.
OVERHEAD_MB = 32
PAGE = 4096

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["sleep", "burn", "hold", "mix"])
parser.add_argument("seconds", type=float, help="how long to keep at it")
parser.add_argument("--fraction", type=float, default=0.6, help="of MAESTRO_MEMORY that hold fills")
parser.add_argument("--samples", action="store_true", help="also write samples.csv, one row a second")
parser.add_argument("--exit-code", type=int, default=0, help="end with it, so that a line fails on purpose")
args = parser.parse_args()

# orq sets these to the line's cpus and memory; outside Maestro, a core and
# 512 MB.
cpus = int(os.environ.get("MAESTRO_CPUS", "1"))
memory = int(os.environ.get("MAESTRO_MEMORY", "512"))
deadline = time.monotonic() + args.seconds


def spin(until: float) -> None:
    """Keeps a core busy until the monotonic clock reaches until."""
    n = 0
    while time.monotonic() < until:
        for _ in range(100_000):
            n += 1


# The workers are started before hold allocates, so that none of them holds
# a copy of its memory.
workers: list[BaseProcess] = []
if args.mode in ("burn", "mix"):
    # One a core: this process spins too, so cpus - 1 more.
    for _ in range(cpus - 1):
        # Forked, not spawned: a spawned one would run this script again.
        p = multiprocessing.get_context("fork").Process(target=spin, args=(deadline,))
        p.start()
        workers.append(p)

held = bytearray()
if args.mode in ("hold", "mix"):
    mb = max(0, int(memory * args.fraction) - OVERHEAD_MB)
    held = bytearray(mb * 1024 * 1024)

print(f"{args.mode} for {args.seconds:g}s with {cpus} CPUs, holding {len(held) >> 20} of {memory} MB", flush=True)

rows: list[str] = ["second,cpu_seconds,max_rss_mb"]
start = time.monotonic()
while (left := deadline - time.monotonic()) > 0:
    tick = min(1.0, left)
    if args.mode in ("burn", "mix"):
        spin(time.monotonic() + tick)
    else:
        time.sleep(tick)
    # Touched again every second, so that the pages stay in memory.
    for i in range(0, len(held), PAGE):
        held[i] = (held[i] + 1) & 0xFF
    if args.samples:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        rows.append(f"{time.monotonic() - start:.0f},{usage.ru_utime + usage.ru_stime:.2f},{usage.ru_maxrss // 1024}")

for p in workers:
    p.join()

me = resource.getrusage(resource.RUSAGE_SELF)
children = resource.getrusage(resource.RUSAGE_CHILDREN)
report = {
    "mode": args.mode,
    "seconds": args.seconds,
    "cpus": cpus,
    "memory": memory,
    "held_mb": len(held) >> 20,
    "cpu_seconds": round(me.ru_utime + me.ru_stime + children.ru_utime + children.ru_stime, 2),
    "max_rss_mb": me.ru_maxrss // 1024,
    "wall_seconds": round(time.monotonic() - start, 2),
    "env": {k: v for k, v in os.environ.items() if k.startswith(("MAESTRO_", "STRESS_"))},
}
with open("report.json", "w") as f:
    json.dump(report, f, indent=2)
if args.samples:
    with open("samples.csv", "w") as f:
        f.write("\n".join(rows) + "\n")

# Printed lines are kept as the container's log.
print(f"done: {report['cpu_seconds']} CPU seconds in {report['wall_seconds']}s, peak {report['max_rss_mb']} MB", flush=True)
sys.exit(args.exit_code)
