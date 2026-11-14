# maestro-template: stress

A stress test of Maestro's scheduler, for the machines q1 to q12. Its
containers do no useful work: each takes up the CPUs and memory it asked for
(or only reserves them) for a while, and writes `report.json` with what it
used. What it tests is how Maestro places, queues and interleaves a thousand
lines of very different sizes.

| File | What it is |
| --- | --- |
| `Dockerfile` | Builds the image: Python and `main.py`, nothing to install |
| `maestro.toml` | Only q1 to q12, one line of `parameters` per mode, the default `cpus`, `memory`, `env` and `outputs` |
| `genvrs.py` | Computes 996 more lines, which makes 1000, a run's most. Each gets a shape, a mode and a time, drawn from a fixed seed, and its own `cpus`, `memory`, `env` and `outputs` through `Config` |
| `main.py` | The program: `sleep`, `burn`, `hold` or `mix` for some seconds |

The shapes, for machines of 20 cores and about 15 GB of which 10 cores and
4 GB are kept back: 10 cores and 11065 MB left for lines on the smallest. orq
refuses a run with a line larger than that, so none is.

| Shape | CPUs | Memory | Lines |
| --- | ---: | ---: | ---: |
| tiny | 1 | 64 MB | 153 |
| default | 1 | 512 MB | 221 + 4 |
| small | 1 | 256 MB | 92 |
| medium | 2 | 1 GB | 143 |
| wide | 6 | 512 MB | 83 |
| tall | 1 | 6 GB | 71 |
| large | 4 | 4 GB | 107 |
| xlarge | 6 | 8 GB | 62 |
| half | 5 | 5 GB | 55 |
| whole | 10 | 10 GB | 9 |

And the modes, what `main.py` does with them:

- `sleep` holds nothing: the line only keeps its cpus and memory from others.
- `burn` keeps every core it was given busy.
- `hold` fills `--fraction` of its memory and touches it every second.
- `mix` does both.

Lines last 10 s to 2 min, the `half` and `whole` ones twice that: about 21
minutes of the 120 cores the twelve machines leave for lines, were they
packed perfectly. One in ten runs with `--samples` and also keeps
`samples.csv`; every hundredth ends with `--exit-code 3`, so that a run has
failed lines to show.

```sh
maestro build <your fork> --watch     # build, run once, and follow it
maestro run <build>                   # again: 9 more for 10 000 containers
maestro queue                         # where the lines wait
maestro top q1                        # one machine, as it fills
maestro runs get <run>                # the reports and logs
```

A run has at most 1000 lines, so the 10 000 containers are ten runs of the
same build. Every run of a build is the same lines; a different `SEED` in
`genvrs.py` draws others, with no new build: `maestro run <build> -g
genvrs.py` sends it from here, and `-c` a `maestro.toml` with, say, other
machines.

On the machines whose Podman can't limit CPU, `burn` uses only the cores it
asked for, but nothing stops it from using more: Maestro still counts only
those.
