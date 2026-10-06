# maestro-template

A starting point for a repo that Maestro builds and runs. Fork it, replace
`main.py` with your program, and adjust `maestro.toml`.

- `Dockerfile`: builds the image. Your program is the `ENTRYPOINT`.
- `maestro.toml`: how runs use the image: on which machines, one container
  per line of `parameters`, and which `outputs` to keep from each.
- `main.py`: a stand-in program that takes `-t <seconds> <output file>`.
- `requirements.txt`: your program's Python dependencies.

```sh
maestro build <your fork>    # builds the image; prints its build number
maestro run <build>          # one container per line of parameters
maestro runs show <run>      # where each line ran and how it ended
maestro runs get <run>       # downloads the outputs and logs
```

Each run's files are also on the Maestro page, under "My runs and their
files", as `<run>/<line>/<file>`.

Without a `maestro.toml`, Maestro runs the image's own `CMD` once, on any
machine, and keeps only what it prints.
