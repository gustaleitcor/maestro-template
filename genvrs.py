"""Computes lines of parameters; enable it with `generator` in maestro.toml.

Maestro calls genvrs() once, when it builds the image. It can use Python's
standard library and read this repo's files, not what requirements.txt
installs.
"""

from collections.abc import Generator


class Config:
    """Optional: what each line runs with. None is maestro.toml's value. Set
    an attribute before a yield to change it for the lines that follow."""

    outputs: list[str] | None = None
    cpus: int | None = None
    memory: int | None = None
    env: dict[str, str] | None = None
    time: str | None = None
    retries: int | None = None


def genvrs() -> Generator[str]:
    for seconds in (10, 20, 30):
        yield f"-t {seconds} out.txt"
