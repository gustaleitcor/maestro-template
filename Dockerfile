FROM docker.io/python:3.12-slim

WORKDIR /app
COPY main.py .

# Runs at build time, so you can watch it stream through your endpoint
RUN python -u main.py build

# Runs when someone starts a container from the image
CMD ["python", "-u", "main.py", "run"]
