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


class Config:
    """How each line runs: the keys of maestro.toml but machines, parameters
    and generator. None is maestro.toml's value, or its default; anything
    else overrides it. Each line runs with what the class holds when genvrs
    yields it."""

    # Files copied out of each container when it ends. Default: none.
    outputs: list[str] | None = None
    # Whole cores per container, at least 1. Default: 1.
    cpus: int | None = None
    # MB per container, at least 6. Default: 512.
    memory: int | None = None
    # Variables of each container's environment. Default: none.
    env: dict[str, str] | None = None
    # The longest the line may run, such as "90m". Default: the server's.
    time: str | None = None
    # Times the line goes back to the queue if its machine is lost, 0 to 5.
    # Default: 0.
    retries: int | None = None


def genvrs() -> Generator[str]:
    for path in sorted(INSTANCES.glob("*.txt")):
        # The first line is `<items> <capacity>`.
        with path.open() as f:
            items, capacity = map(int, f.readline().split())

        # Bigger instances get longer to prove their answer is the best.
        seconds = 10 if items <= 30 else 60

        # And more memory for the solver's search tree than maestro.toml's,
        # and two cores, which main.py gives the solver as threads.
        Config.memory = None if items <= 30 else 1024
        Config.cpus = None if items <= 30 else 2
        Config.env = {"ITEMS": str(items)}

        for scale in SCALES:
            yield f"{path.stem} --capacity {round(capacity * scale)} --time-limit {seconds}"

        # Printed lines go to the build log.
        print(f"{path.stem}: {items} items, capacity {capacity}")
