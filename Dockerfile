FROM docker.io/library/python:3.12-slim

# main.py needs only Python's standard library: nothing to install. No .pyc
# files, and printed lines reach the log as they are printed.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Relative `outputs` (report.json, samples.csv) are looked for here.
WORKDIR /work

COPY main.py /app/main.py

# The program. Each line of `parameters` replaces CMD and reaches it as
# arguments.
ENTRYPOINT ["python", "/app/main.py"]

# Used when maestro.toml has no lines: ten seconds of sleep.
CMD ["sleep", "10"]
