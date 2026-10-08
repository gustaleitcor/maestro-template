# maestro-template

A repo that Maestro builds and runs. Fork it, replace `main.py` with your
program, and adjust `maestro.toml`. The `knapsack` branch is a fuller
example: real problems, solved with a solver, their lines computed.

| File | What it is |
| --- | --- |
| `Dockerfile` | Builds the image; your program is its `ENTRYPOINT` |
| `maestro.toml` | Which machines, one container per line of `parameters`, which `outputs` to keep |
| `genvrs.py` | Optional: computes more lines instead of writing them out |
| `main.py` | A stand-in program: `-t <seconds> <output file>` |
| `requirements.txt` | Your program's Python dependencies |

```sh
maestro build <your fork> --watch   # build, run, and follow until it ends
maestro runs get <run>              # download the outputs and logs
```

Or step by step: `maestro build <your fork>`, then `maestro run <build>` and
`maestro runs show <run>`. A public repo needs no forge token; add one with
`maestro forges add` for private repos.

Without a `maestro.toml`, Maestro runs the image's own `CMD` once, on any
machine, and keeps only what it prints.
