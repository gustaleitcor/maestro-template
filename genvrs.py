"""Computes lines of parameters; enable it with `generator` in maestro.toml.

Maestro calls genvrs() once, when it builds the image. It can use Python's
standard library and read this repo's files, not what requirements.txt
installs.
"""


def genvrs():
    for seconds in (10, 20, 30):
        yield f"-t {seconds} out.txt"
