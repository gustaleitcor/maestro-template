"""Computes lines of parameters: every instance, with tighter and looser sacks.

Maestro calls genvrs() once, when it builds the image, and starts a container
per string it yields. It runs with Python's standard library and this repo's
files, so it reads instances/ itself.
"""

from collections.abc import Generator
from pathlib import Path

INSTANCES = Path(__file__).parent / "instances"

# Each instance is solved again with its capacity scaled by these.
SCALES: tuple[float, ...] = (0.25, 0.5, 2)


def genvrs() -> Generator[str]:
    for path in sorted(INSTANCES.glob("*.txt")):
        # The first line is `<items> <capacity>`; the items aren't needed here.
        with path.open() as f:
            items, capacity = map(int, f.readline().split())
        # Bigger instances get longer to prove their answer is the best.
        seconds = 10 if items <= 30 else 60
        for scale in SCALES:
            yield f"{path.stem} --capacity {round(capacity * scale)} --time-limit {seconds}"
        # Printed lines go to the build log.
        print(f"{path.stem}: {items} items, capacity {capacity}")
