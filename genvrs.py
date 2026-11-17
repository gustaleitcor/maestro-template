"""Computes the stress test's lines: a thousand containers of many sizes.

Maestro calls genvrs() once, when it builds the image, and starts a container
per string it yields. Each line gets a shape, the cpus and memory it asks
for, from SHAPES; a mode, what main.py does with them; and how long. They are
drawn at random, from a fixed seed, so every build of a commit gives the
same lines.

The largest line asks for 10 cores and 10240 MB. Maestro refuses a run
whole when one of its lines is larger than what every machine leaves for
lines, so on smaller machines make SHAPES smaller, and send this file with
`maestro run <build> -g genvrs.py`.
"""

import random
from collections.abc import Generator
from typing import NamedTuple

# With maestro.toml's 4 lines of parameters, a run of 1000. Maestro takes up
# to 5000, but ten runs show more of the queue than two.
LINES = 996
SEED = 2026


class Shape(NamedTuple):
    name: str
    # None is maestro.toml's: 1 core and 512 MB.
    cpus: int | None
    memory: int | None
    # How often it is drawn, against the others'.
    weight: int


SHAPES: tuple[Shape, ...] = (
    Shape("tiny", 1, 64, 15),
    Shape("default", None, None, 20),
    Shape("small", 1, 256, 10),
    Shape("medium", 2, 1024, 15),
    Shape("wide", 6, 512, 8),  # many cores, little memory
    Shape("tall", 1, 6144, 8),  # one core, much memory
    Shape("large", 4, 4096, 10),
    Shape("xlarge", 6, 8192, 6),
    Shape("half", 5, 5120, 4),
    Shape("whole", 10, 10240, 1),  # the largest
)

# What main.py does with them, and how often.
MODES: dict[str, int] = {"sleep": 40, "burn": 20, "hold": 20, "mix": 20}

# Every this many lines, one fails on purpose.
FAIL_EVERY = 100


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
    rng = random.Random(SEED)
    counts: dict[str, int] = {}
    for n in range(1, LINES + 1):
        shape = rng.choices(SHAPES, weights=[s.weight for s in SHAPES])[0]
        mode = rng.choices(list(MODES), weights=list(MODES.values()))[0]
        # Mostly short, some long; the largest shapes stay longer.
        seconds = rng.choice((10, 20, 30, 45, 60, 90, 120))
        if shape.name in ("half", "whole"):
            seconds *= 2

        Config.cpus = shape.cpus
        Config.memory = shape.memory
        Config.env = {"STRESS_LINE": str(n), "STRESS_SHAPE": shape.name}

        line = f"{mode} {seconds}"
        if mode in ("hold", "mix"):
            line += f" --fraction {rng.choice((0.3, 0.5, 0.7, 0.85))}"
        # One in ten also keeps its samples: an output maestro.toml lacks.
        if rng.random() < 0.1:
            line += " --samples"
            Config.outputs = ["report.json", "samples.csv"]
        else:
            Config.outputs = None
        if n % FAIL_EVERY == 0:
            line += " --exit-code 3"

        counts[shape.name] = counts.get(shape.name, 0) + 1
        yield line

    # Printed lines go to the build log.
    for shape in SHAPES:
        print(f"{shape.name:8} {shape.cpus or 1:>2} CPUs {shape.memory or 512:>6} MB: {counts.get(shape.name, 0)} lines")
