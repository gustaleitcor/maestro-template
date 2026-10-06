# Maestro builds this image as is. Two conventions are all it asks:
#   - ENTRYPOINT is your program. Each line of `parameters` in maestro.toml
#     replaces CMD, so it reaches the program as its arguments.
#   - What you want kept goes to the paths listed under `outputs`.

FROM docker.io/library/python:3.12-slim

# Relative outputs are looked for here once the container ends.
WORKDIR /work

# Dependencies first, so editing the code doesn't reinstall them.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Absolute outputs must exist for the program to write to.
RUN mkdir -p /var/log/app

# -u prints as it goes, so `maestro runs logs` follows a running line.
ENTRYPOINT ["python", "-u", "/app/main.py"]

# Used when maestro.toml has no `parameters`.
CMD ["-t", "1", "out.txt"]
