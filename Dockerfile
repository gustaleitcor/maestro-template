FROM docker.io/library/python:3.12-slim

# Relative `outputs` are looked for here.
WORKDIR /work

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app

# Your program. Each line of `parameters` replaces CMD and reaches it as
# arguments; -u prints as it goes, so logs can be followed.
ENTRYPOINT ["python", "-u", "/app/main.py"]

# Used when maestro.toml has no lines.
CMD ["-t", "1", "out.txt"]
