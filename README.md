# maestro-template: stress

A stress test of Maestro's scheduler, on whatever machines it has. Its
containers do no useful work: each takes up the CPUs and memory it asked for
(or only reserves them) for a while, and writes `report.json` with what it
used. What it tests is how Maestro places, queues and interleaves a thousand
lines of very different sizes.

| File | What it is |
| --- | --- |
| `Dockerfile` | Builds the image: Python and `main.py`, nothing to install |
| `maestro.toml` | One line of `parameters` per mode, the default `cpus`, `memory`, `time`, `retries`, `env` and `outputs` |
| `genvrs.py` | Computes 996 more lines, which makes 1000. Each gets a shape, a mode and a time, drawn from a fixed seed, and its own `cpus`, `memory`, `env` and `outputs` through `Config` |
| `main.py` | The program: `sleep`, `burn`, `hold` or `mix` for some seconds |

The lines run on any machine. The largest asks for 10 cores and 10 GB.
Maestro refuses a run when one of its lines is larger than what every
machine has for lines. On smaller machines, make the shapes in `genvrs.py`
smaller and send it with `maestro run <build> -g genvrs.py`, with no new
build.

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
minutes of 120 cores, were they packed perfectly. One in ten runs with
`--samples` and also keeps `samples.csv`; every hundredth ends with
`--exit-code 3`, so that a run has failed lines to show. Every line may run for 10 minutes (`time`). A line
whose machine is lost goes back to the queue, up to twice (`retries`), so
restarting a machine in the middle of a run loses none of its lines.

```sh
maestro build <your fork> --watch     # build, run once, and follow it
maestro run <build>                   # again: 9 more for 10 000 containers
maestro queue                         # the user, dispatcher and machine queues
maestro top                           # the machines, as they fill
maestro runs show <run> --failed      # the lines that didn't succeed
maestro runs retry <run>              # run those again
maestro runs cancel <run> --line 7    # stop one line and leave the rest
maestro runs get <run>                # the reports and logs
```

Each run is 1000 lines, so the 10 000 containers are ten runs of the same
build. Maestro takes up to 5000 lines in a run, but ten runs show more of how
the queue takes turns. Every run of a build is the same lines; a different
`SEED` in `genvrs.py` draws others, with no new build: `maestro run <build>
-g genvrs.py` sends it from here, and `-c` a `maestro.toml` with, say, only some
of the machines.

On the machines whose Podman can't limit CPU, `burn` uses only the cores it
asked for, but nothing stops it from using more: Maestro still counts only
those.
