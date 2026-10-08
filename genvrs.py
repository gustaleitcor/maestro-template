"""Computes lines of parameters: every instance, with tighter and looser sacks.

Maestro calls genvrs() once, when it builds the image, and starts a container
per string it yields. It runs with Python's standard library and this repo's
files, so it can import knapsack and read instances/, but not mip.
"""

import knapsack

# Each instance is solved again with its capacity scaled by these.
SCALES = (0.25, 0.5, 2)


def genvrs():
    for name in knapsack.names():
        instance = knapsack.load(name)
        # Bigger instances get longer to prove their answer is the best.
        seconds = 10 if len(instance.values) <= 30 else 60
        for scale in SCALES:
            yield f"{name} --capacity {round(instance.capacity * scale)} --time-limit {seconds}"
        # Printed lines go to the build log.
        print(f"{name}: {len(instance.values)} items, capacity {instance.capacity}")
