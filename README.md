# maestro-template

A repo that Maestro builds and runs, with a small real job in it: knapsack
problems solved with [mip](https://www.python-mip.com), one container per
instance and capacity. Fork it, replace `main.py` with your program, and
adjust `maestro.toml`.

| File | What it is |
| --- | --- |
| `Dockerfile` | Builds the image; your program is its `ENTRYPOINT` |
| `maestro.toml` | Which machines, one container per line of `parameters`, the `cpus`, `memory` and `env` of each, which `outputs` to keep |
| `genvrs.py` | Computes more lines: every instance in `instances/`, at three capacities, giving the big ones more memory through `Config` |
| `main.py` | The program: solves one instance and writes `solution.json` |
| `knapsack.py` | Reads the instances for `main.py` |
| `instances/` | The problems, one file each |
| `requirements.txt` | The program's Python dependencies |

```sh
maestro build <your fork> --watch   # build, run, and follow until it ends
maestro runs get <run>              # download the outputs and logs
```

Or step by step: `maestro build <your fork>`, then `maestro run <build>` and
`maestro runs show <run>`. A public repo needs no forge token; add one with
`maestro forges add` for private repos.

Lines wait in a queue before they start, and those of different users are
interleaved as the Maestro administrator set the scheduler up, so a large
run doesn't hold everyone else back. A line starts once a machine has its
`cpus` and `memory` free: asking for what your program needs, and no more,
starts it sooner. `maestro queue` shows where your lines wait and your share
of the machines; `maestro usage`, what they used.

Without a `maestro.toml`, Maestro runs the image's own `CMD` once, on any
machine, and keeps only what it prints.
