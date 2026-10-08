# maestro-template

A repo that Maestro builds and runs, with a small real job in it: knapsack
problems solved with [mip](https://www.python-mip.com), one container per
instance and capacity. Fork it, replace `main.py` with your program, and
adjust `maestro.toml`.

| File | What it is |
| --- | --- |
| `Dockerfile` | Builds the image; your program is its `ENTRYPOINT` |
| `maestro.toml` | Which machines, one container per line of `parameters`, which `outputs` to keep |
| `genvrs.py` | Computes more lines: every instance in `instances/`, at three capacities |
| `main.py` | The program: solves one instance and writes `solution.json` |
| `knapsack.py` | Reads the instances; used by both of the above |
| `instances/` | The problems, one file each |
| `requirements.txt` | The program's Python dependencies |

```sh
maestro build <your fork> --watch   # build, run, and follow until it ends
maestro runs get <run>              # download the outputs and logs
```

Or step by step: `maestro build <your fork>`, then `maestro run <build>` and
`maestro runs show <run>`. A public repo needs no forge token; add one with
`maestro forges add` for private repos.

Without a `maestro.toml`, Maestro runs the image's own `CMD` once, on any
machine, and keeps only what it prints.
