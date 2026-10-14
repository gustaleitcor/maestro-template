"""The knapsack instances in instances/, as main.py loads them to solve one.

A file is `<items> <capacity>` on its first line, then `<value> <weight>` per item.
"""

from pathlib import Path
from typing import NamedTuple

FOLDER = Path(__file__).parent / "instances"


class Instance(NamedTuple):
    name: str
    capacity: int
    values: list[int]
    weights: list[int]


def names() -> list[str]:
    return sorted(path.stem for path in FOLDER.glob("*.txt"))


def load(name: str) -> Instance:
    rows = [line.split() for line in (FOLDER / f"{name}.txt").read_text().splitlines() if line.strip()]
    count, capacity = map(int, rows[0])
    items = [(int(value), int(weight)) for value, weight in rows[1:]]
    if len(items) != count:
        raise ValueError(f"{name}: {count} items announced, {len(items)} found")
    return Instance(name, capacity, [v for v, _ in items], [w for _, w in items])
