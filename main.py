"""Solves one knapsack instance with mip and writes solution.json.

Its arguments are one line of `parameters` from maestro.toml, or one that
genvrs.py yielded: `small`, `large --capacity 300 --time-limit 60`.
"""

import argparse
import json
import os
import sys
from numbers import Real
from typing import cast

import knapsack
from mip import BINARY, Model, OptimizationStatus, maximize, xsum


def real(n: int) -> Real:
    """n as mip's annotations ask for it: numbers.Real, which an int is when
    the program runs, but not to a type checker."""
    return cast(Real, n)


parser = argparse.ArgumentParser()
parser.add_argument("instance", choices=knapsack.names())
parser.add_argument("--capacity", type=int, help="instead of the instance's own")
parser.add_argument("--time-limit", type=int, default=10, help="seconds to search")
args = parser.parse_args()

instance = knapsack.load(args.instance)
capacity: int = instance.capacity if args.capacity is None else args.capacity
items = range(len(instance.values))

model = Model("knapsack")
model.verbose = 0
# As many threads as the container has cores; outside Maestro, 0 lets the
# solver choose.
model.threads = int(os.environ.get("MAESTRO_CPUS", "0"))
take = [model.add_var(var_type=BINARY) for _ in items]
model.objective = maximize(xsum(take[i] * real(instance.values[i]) for i in items))
model += xsum(take[i] * real(instance.weights[i]) for i in items) <= real(capacity)

status = model.optimize(max_seconds=args.time_limit)
if status not in (OptimizationStatus.OPTIMAL, OptimizationStatus.FEASIBLE):
    sys.exit(f"{args.instance}: no solution ({status.name})")

# x is None only without a solution, which exited above.
taken = [i for i in items if float(take[i].x or 0) >= 0.99]
solution: dict[str, object] = {
    "instance": args.instance,
    "capacity": capacity,
    "optimal": status == OptimizationStatus.OPTIMAL,
    "value": sum(instance.values[i] for i in taken),
    "weight": sum(instance.weights[i] for i in taken),
    "items": taken,
}
with open("solution.json", "w") as f:
    json.dump(solution, f, indent=2)

# Printed lines are kept as the container's log.
print(
    f"{args.instance}: value {solution['value']} with {len(taken)} items, weight {solution['weight']}/{capacity}"
)
