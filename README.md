# maestro-template

A repo that Maestro builds and runs. Fork it, replace `main.py` with your
program, and adjust `maestro.toml`. Two branches are fuller examples:
`knapsack` solves real problems with a solver, and `stress` runs a thousand
lines of many sizes to test the queue.

| File | What it is |
| --- | --- |
| `Dockerfile` | Builds the image; your program is its `ENTRYPOINT` |
| `maestro.toml` | Which machines, one container per line of `parameters`, which `outputs` to keep, and the other keys commented out |
| `genvrs.py` | Optional: computes more lines instead of writing them out |
| `main.py` | A stand-in program: `-t <seconds> <output file>` |
| `requirements.txt` | Your program's Python dependencies |

```sh
maestro build <your fork> --watch   # build, run, and follow until it ends
maestro runs logs <run> 2 -f        # follow what line 2 prints
maestro runs get <run>              # download the outputs and logs
maestro runs retry <run>            # run the lines that failed again
maestro runs cancel <run> --line 2  # stop one line and leave the rest
maestro runs keep <run>             # keep a run from expiring
```

To try other parameters without pushing, send a `maestro.toml` or a
generator from your computer: `maestro run <build> -c my.toml` or `-g
genvrs.py`.

Or step by step: `maestro build <your fork>`, then `maestro run <build>` and
`maestro runs show <run>`. A public repo needs no forge token; add one with
`maestro forges add` for private repos.

Without a `maestro.toml`, Maestro runs the image's own `CMD` once, on any
machine, and keeps only what it prints.
